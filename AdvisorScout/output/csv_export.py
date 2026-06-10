"""
CSV export module.
Exports professor data to a CSV file for easy use in spreadsheets.
"""

import csv
import logging
import os
from typing import List

from models import Professor
import json

_universities_data = None


def _load_universities():
    global _universities_data
    if _universities_data is None:
        path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "universities.json")
        try:
            with open(path, "r", encoding="utf-8") as f:
                _universities_data = json.load(f)
        except Exception:
            _universities_data = {"universities": []}
    return _universities_data


def _get_university_info(university: str):
    """Look up country and region for a university from universities.json."""
    if not university:
        return None
    data = _load_universities()
    for uni in data.get("universities", []):
        if uni.get("name", "").lower() == university.strip().lower():
            return uni
    return None

logger = logging.getLogger(__name__)


def export_csv(professors: List[Professor], output_path: str):
    """
    Export professor data to a CSV file.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    fieldnames = [
        "Name",
        "University",
        "Country",
        "QS Subject Rank",
        "Department",
        "Title",
        "Email",
        "Profile URL",
        "Research Interests",
        "Match Score",
        "Match Level",
        "Matched Keywords",
        "Google Scholar URL",
        "h-index",
        "Total Citations",
        "Lab URL",
        "Recent Papers",
        "Bio (excerpt)",
    ]

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for prof in professors:
            # Format publications
            papers = []
            for pub in prof.publications[:5]:
                paper_str = pub.title
                if pub.year:
                    paper_str += f" ({pub.year})"
                if pub.venue:
                    paper_str += f" — {pub.venue}"
                papers.append(paper_str)

            # Determine country and rank
            info = _get_university_info(prof.university)
            country = info.get("country", _get_country(prof.university)) if info else _get_country(prof.university)
            bracket = info.get("qs_subject_rank", "") if info else ""

            writer.writerow({
                "Name": prof.name,
                "University": prof.university,
                "Country": country,
                "QS Subject Rank": bracket,
                "Department": prof.department,
                "Title": prof.title,
                "Email": prof.email,
                "Profile URL": prof.profile_url,
                "Research Interests": prof.interests_str,
                "Match Score": prof.match_score,
                "Match Level": prof.match_level,
                "Matched Keywords": "; ".join(prof.matched_keywords),
                "Google Scholar URL": prof.scholar_url,
                "h-index": prof.h_index if prof.h_index else "",
                "Total Citations": prof.citations_total if prof.citations_total else "",
                "Lab URL": prof.lab_url,
                "Recent Papers": " | ".join(papers),
                "Bio (excerpt)": prof.bio[:300] if prof.bio else "",
            })

    logger.info(f"CSV exported: {output_path} ({len(professors)} professors)")


def _get_country(university: str) -> str:
    """Determine country based on university name."""
    au_indicators = [
        "australia", "melbourne", "sydney", "unsw", "monash",
        "queensland", "adelaide", "western australia", "anu",
        "macquarie", "curtin", "rmit", "deakin", "griffith",
        "wollongong", "newcastle", "tasmania", "flinders",
        "latrobe", "swinburne", "james cook", "canberra",
        "charles sturt", "southern cross", "edith cowan",
        "murdoch", "charles darwin", "victoria university",
        "bond university", "university of technology sydney", "uts",
    ]
    uni_lower = university.lower()
    for indicator in au_indicators:
        if indicator in uni_lower:
            return "Australia"
    return "US"
