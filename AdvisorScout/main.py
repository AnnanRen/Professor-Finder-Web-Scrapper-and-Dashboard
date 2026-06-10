"""
AdvisorScout - Main Orchestrator (v2)

Since Google Scholar blocks automated access, this version uses a two-step approach:
1. Uses web search to find professors matching our keywords at target universities
2. Scrapes their profile pages for details
3. Generates a beautiful HTML report + CSV

Run: python main.py
"""

import os
import sys
import io
import re
import json
import logging
import time
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional, Tuple
from datetime import datetime

from models import Professor, Publication
from config import (
    SEARCH_KEYWORDS,
    MIN_MATCH_SCORE, REQUEST_DELAY, USER_AGENT, REQUEST_TIMEOUT,
    SCHOLAR_SEARCH_QUERIES, MAX_PUBLICATIONS,
)
from matcher import KeywordMatcher
from output.html_report import generate_html_report
from output.csv_export import export_csv

UNIVERSITIES_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "universities.json")


def load_universities(json_path: str = None) -> List[Tuple[str, str, str]]:
    """Load university targets from universities.json. Returns list of (name, department, url)."""
    if json_path is None:
        json_path = UNIVERSITIES_FILE
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    enabled_regions = {
        k for k, v in data.get("regions", {}).items() if v.get("enabled", False)
    }

    targets = []
    for uni in data.get("universities", []):
        if uni.get("region") not in enabled_regions:
            continue
        if uni.get("status") == "broken":
            continue
        if not uni.get("faculty_url"):
            continue
        targets.append((uni["name"], uni["department"], uni["faculty_url"]))

    return targets


# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("professor_finder.log", encoding="utf-8"),
    ],
)
logger = logging.getLogger(__name__)

RESULTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
CACHE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache.json")
STATUS_FILE = os.path.join(RESULTS_DIR, "status.json")


class ProfessorFinder:
    """Main class that orchestrates the professor discovery pipeline."""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        })
        self.all_professors: Dict[str, Professor] = {}
        self._load_cache()
        self.status = {
            "phase": "Starting",
            "total_urls": 0,
            "current_index": 0,
            "current_university": "",
            "professors_total": len(self.all_professors),
            "start_time": datetime.now().isoformat(),
            "last_update": datetime.now().isoformat()
        }
        self._save_status()

    def _load_cache(self):
        """Load previously found professors from cache."""
        if os.path.exists(CACHE_FILE):
            try:
                with open(CACHE_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for entry in data:
                    prof = Professor(
                        name=entry["name"],
                        university=entry["university"],
                        department=entry.get("department", ""),
                        title=entry.get("title", ""),
                        profile_url=entry.get("profile_url", ""),
                        email=entry.get("email", ""),
                        research_interests=entry.get("research_interests", []),
                        bio=entry.get("bio", ""),
                        scholar_url=entry.get("scholar_url", ""),
                        lab_url=entry.get("lab_url", ""),
                    )
                    for pub_data in entry.get("publications", []):
                        prof.publications.append(Publication(**pub_data))
                    key = f"{prof.name.lower()}|{prof.university.lower()}"
                    self.all_professors[key] = prof
                logger.info(f"Loaded {len(self.all_professors)} professors from cache")
            except Exception as e:
                logger.warning(f"Could not load cache: {e}")

    def _save_cache(self):
        """Save found professors to cache for incremental runs."""
        data = []
        for prof in self.all_professors.values():
            entry = {
                "name": prof.name,
                "university": prof.university,
                "department": prof.department,
                "title": prof.title,
                "profile_url": prof.profile_url,
                "email": prof.email,
                "research_interests": prof.research_interests,
                "bio": prof.bio,
                "scholar_url": prof.scholar_url,
                "lab_url": prof.lab_url,
                "publications": [
                    {"title": p.title, "year": p.year, "authors": p.authors,
                     "venue": p.venue, "url": p.url, "citations": p.citations}
                    for p in prof.publications
                ],
            }
            data.append(entry)
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.info(f"Cache saved: {len(data)} professors")

    def _save_status(self):
        """Save current progress to status.json."""
        os.makedirs(RESULTS_DIR, exist_ok=True)
        self.status["last_update"] = datetime.now().isoformat()
        self.status["professors_total"] = len(self.all_professors)
        with open(STATUS_FILE, "w", encoding="utf-8") as f:
            json.dump(self.status, f, indent=2)

    def update_status(self, **kwargs):
        """Update status and save to file."""
        self.status.update(kwargs)
        self._save_status()

    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """Fetch and parse a web page."""
        time.sleep(REQUEST_DELAY)
        try:
            resp = self.session.get(url, timeout=REQUEST_TIMEOUT)
            resp.raise_for_status()
            return BeautifulSoup(resp.text, "lxml")
        except Exception as e:
            logger.warning(f"Failed to fetch {url}: {e}")
            return None

    def add_professor(self, prof: Professor):
        """Add a professor (deduplicating by name+university)."""
        key = f"{prof.name.lower()}|{prof.university.lower()}"
        if key in self.all_professors:
            existing = self.all_professors[key]
            # Merge data
            if not existing.email and prof.email:
                existing.email = prof.email
            if not existing.profile_url and prof.profile_url:
                existing.profile_url = prof.profile_url
            if not existing.bio and prof.bio:
                existing.bio = prof.bio
            if prof.research_interests:
                existing_set = set(i.lower() for i in existing.research_interests)
                for interest in prof.research_interests:
                    if interest.lower() not in existing_set:
                        existing.research_interests.append(interest)
        else:
            self.all_professors[key] = prof

    # ── Faculty Page Scrapers ──────────────────────────────────

    def scrape_faculty_page(self, url: str, university: str, department: str) -> List[Professor]:
        """Generic faculty page scraper — tries multiple strategies."""
        soup = self.fetch_page(url)
        if not soup:
            return []

        professors = []

        # Strategy 1: Find profile links
        profile_links = []
        for a in soup.find_all("a", href=True):
            href = a["href"]
            text = a.get_text(strip=True)
            # Skip mailto: links — these are NOT profile links
            if href.lower().startswith("mailto:"):
                continue
            # Look for links that are likely faculty profiles
            if not text or len(text) < 4 or len(text) > 80:
                continue
            # Skip names that look like emails
            if "@" in text:
                continue
            # Skip navigation/menu links
            skip_words = ["home", "about", "contact", "news", "event", "apply",
                         "admission", "research", "program", "course", "degree",
                         "faculty directory", "all faculty", "back", "more",
                         "previous", "next", "search", "login", "menu"]
            if any(w in text.lower() for w in skip_words):
                continue
            # Check if href looks like a profile
            profile_patterns = ["/people/", "/faculty/", "/profile/", "/person/",
                               "/staff/", "/directory/bio", "/user/", "~"]
            if any(p in href.lower() for p in profile_patterns):
                from urllib.parse import urljoin
                full_url = urljoin(url, href)
                profile_links.append((text, full_url))

        # Strategy 2: Look for structured cards
        card_selectors = [
            ".faculty-card", ".person-card", ".staff-card", ".people-card",
            ".views-row", ".faculty-member", ".profile-card", ".team-member",
            'article[class*="person"]', 'div[class*="faculty-"]',
            'div[class*="people-"]', 'li[class*="faculty"]',
        ]
        for sel in card_selectors:
            cards = soup.select(sel)
            if cards and len(cards) >= 3:
                for card in cards:
                    name_el = card.select_one("h2 a, h3 a, h4 a, .name a, .title a")
                    if not name_el:
                        # Skip mailto: links when falling back
                        for a_tag in card.find_all("a", href=True):
                            if not a_tag["href"].lower().startswith("mailto:"):
                                name_el = a_tag
                                break
                    if not name_el:
                        continue
                    name = name_el.get_text(strip=True)
                    if len(name) < 4 or len(name) > 80 or "@" in name:
                        continue
                    from urllib.parse import urljoin
                    href = name_el.get("href", "")
                    if href.lower().startswith("mailto:"):
                        continue
                    link = urljoin(url, href) if href else ""
                    email = self._find_email(card)
                    prof = Professor(
                        name=name, university=university,
                        department=department, profile_url=link, email=email,
                    )
                    professors.append(prof)
                break  # Use first selector that works

        # Use profile links if cards didn't work
        if not professors:
            seen = set()
            for name, link in profile_links:
                if name.lower() not in seen and "@" not in name:
                    seen.add(name.lower())
                    professors.append(Professor(
                        name=name, university=university,
                        department=department, profile_url=link,
                    ))

        logger.info(f"  Found {len(professors)} faculty entries from {university}")
        return professors

    def enrich_professor_profile(self, prof: Professor) -> Professor:
        """Visit a professor's profile page to extract details."""
        if not prof.profile_url:
            return prof

        soup = self.fetch_page(prof.profile_url)
        if not soup:
            return prof

        # Extract email
        if not prof.email:
            prof.email = self._find_email(soup)

        # Extract research interests
        if not prof.research_interests:
            for sel in [".research-interests", ".field-research", ".research-areas",
                       '[class*="interest"]', '[class*="research"]', ".expertise"]:
                el = soup.select_one(sel)
                if el:
                    text = el.get_text(strip=True)
                    if text:
                        prof.research_interests = self._parse_interests(text)
                        break

        # Extract bio
        if not prof.bio:
            for sel in [".biography", ".bio", ".about", ".field-body",
                       ".description", '[class*="biography"]', ".profile-body"]:
                el = soup.select_one(sel)
                if el:
                    prof.bio = el.get_text(strip=True)[:1000]
                    break

            # Fallback: look for long paragraphs that could be a bio
            if not prof.bio:
                for p in soup.find_all("p"):
                    text = p.get_text(strip=True)
                    if len(text) > 200 and any(w in text.lower() for w in
                        ["research", "professor", "phd", "lab", "interests"]):
                        prof.bio = text[:1000]
                        break

        # Extract title
        if not prof.title:
            for sel in [".field-title", ".position", '[class*="title"]',
                       '[class*="position"]', ".job-title"]:
                el = soup.select_one(sel)
                if el:
                    text = el.get_text(strip=True)
                    if any(kw in text.lower() for kw in
                          ["professor", "lecturer", "researcher", "director", "fellow"]):
                        prof.title = text
                        break

        # Find Scholar profile link
        if not prof.scholar_url:
            for a in soup.find_all("a", href=True):
                if "scholar.google" in a["href"]:
                    prof.scholar_url = a["href"]
                    break

        return prof

    @staticmethod
    def _find_email(element) -> str:
        """Find email in an HTML element."""
        for a in element.find_all("a", href=True):
            if "mailto:" in a["href"]:
                return a["href"].replace("mailto:", "").split("?")[0].strip()
        text = element.get_text()
        match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
        return match.group(0) if match else ""

    @staticmethod
    def _parse_interests(text: str) -> List[str]:
        """Parse research interests from text."""
        for delim in [";", "|", "\n", ","]:
            if delim in text:
                parts = [p.strip() for p in text.split(delim) if p.strip() and len(p.strip()) > 2]
                if len(parts) > 1:
                    return parts
        return [text] if text and len(text) > 2 else []


def main():
    logger.info("=" * 60)
    logger.info("AdvisorScout v2 - Starting")
    logger.info("=" * 60)
    
    finder = ProfessorFinder()
    targets = load_universities()
    finder.update_status(phase="Phase 1: Scraping Directories", total_urls=len(targets))

    # Phase 1: Scrape faculty directories
    logger.info("PHASE 1: Scraping faculty directories...")
    for i, (uni, dept, url) in enumerate(targets, 1):
        logger.info(f"\n[{i}/{len(targets)}] Scraping: {uni} - {dept}")
        finder.update_status(current_index=i, current_university=uni)
        try:
            profs = finder.scrape_faculty_page(url, uni, dept)
            for prof in profs:
                finder.add_professor(prof)
            finder._save_cache()
        except Exception as e:
            logger.warning(f"  Failed to scrape {uni}: {e}")

    # Phase 2: Enrich ALL professors
    all_profs = list(finder.all_professors.values())
    finder.update_status(phase="Phase 2: Enriching Profiles", current_index=0, total_urls=len(all_profs))
    
    logger.info("\nPHASE 2: Enriching all professors from profile pages...")
    from concurrent.futures import ThreadPoolExecutor
    
    def enrich_wrapper(prof_tuple):
        idx, prof = prof_tuple
        if not prof.bio and not prof.research_interests and prof.profile_url:
            try:
                finder.enrich_professor_profile(prof)
            except Exception:
                pass
        if idx % 10 == 0:
            finder.update_status(current_index=idx, current_university=prof.name)

    with ThreadPoolExecutor(max_workers=20) as executor:
        list(executor.map(enrich_wrapper, enumerate(all_profs, 1)))

    finder._save_cache()

    # Phase 3: Score and Filter
    finder.update_status(phase="Phase 3: Scoring & Filtering")
    logger.info("\nPHASE 3: Scoring by research interest keywords...")
    matcher = KeywordMatcher()
    scored = matcher.filter_professors(all_profs, min_score=MIN_MATCH_SCORE)

    if not scored:
        scored = matcher.filter_professors(all_profs, min_score=0.3)

    # Phase 4: Output
    finder.update_status(phase="Phase 4: Finalizing Reports")
    logger.info("\nPHASE 4: Generating reports...")
    os.makedirs(RESULTS_DIR, exist_ok=True)

    html_path = os.path.join(RESULTS_DIR, "professors_report.html")
    csv_path = os.path.join(RESULTS_DIR, "professors_data.csv")

    generate_html_report(scored, html_path)
    export_csv(scored, csv_path)

    finder.update_status(phase="Completed", current_index=len(targets))
    logger.info("\nDONE!")

    try:
        import webbrowser
        webbrowser.open(f"file:///{html_path.replace(os.sep, '/')}")
    except Exception:
        pass


if __name__ == "__main__":
    main()
