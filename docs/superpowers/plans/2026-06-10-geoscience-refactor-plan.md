# Geoscience Refactor Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Transform AdvisorScout from ECE/CS professor finder into a global Geoscience advisor discovery tool with Chinese/English i18n.

**Architecture:** Data layer extracted from code into `universities.json`. Keywords replaced in `config.py`. `main.py` reads targets from JSON. `html_report.py` embeds JS i18n with `data-i18n` attribute pattern.

**Tech Stack:** Python 3.8+, BeautifulSoup4, requests, JSON, vanilla JS (no framework)

---

### Task 0: Prepare worktree isolation

**Files:**
- Create: git worktree on branch `feat/geoscience-refactor`

- [ ] **Step 1: Create worktree**

```bash
git worktree add -b feat/geoscience-refactor ../AdvisorScout-geo main
```

Expected: new worktree at `../AdvisorScout-geo` on branch `feat/geoscience-refactor`

---

### Task 1: Create universities.json with ~30 core universities

**Files:**
- Create: `AdvisorScout/universities.json`

- [ ] **Step 1: Create universities.json**

Write file at `AdvisorScout/universities.json`:

```json
{
  "regions": {
    "uk_ireland": { "name": "UK & Ireland", "name_zh": "英国与爱尔兰", "enabled": true },
    "europe_mainland": { "name": "Mainland Europe", "name_zh": "欧洲大陆", "enabled": true },
    "usa_canada": { "name": "USA & Canada", "name_zh": "美国与加拿大", "enabled": true },
    "australia_nz": { "name": "Australia & New Zealand", "name_zh": "澳大利亚与新西兰", "enabled": true },
    "singapore_hongkong": { "name": "Singapore & Hong Kong", "name_zh": "新加坡与香港", "enabled": true },
    "east_asia": { "name": "East Asia", "name_zh": "东亚", "enabled": false },
    "southeast_asia": { "name": "Southeast Asia", "name_zh": "东南亚", "enabled": false },
    "middle_east": { "name": "Middle East", "name_zh": "中东", "enabled": false },
    "south_asia": { "name": "South Asia", "name_zh": "南亚", "enabled": false },
    "south_america": { "name": "South America", "name_zh": "南美", "enabled": false },
    "africa": { "name": "Africa", "name_zh": "非洲", "enabled": false }
  },
  "universities": [
    { "name": "University of Cambridge", "region": "uk_ireland", "country": "UK", "country_zh": "英国", "department": "Earth Sciences", "department_zh": "地球科学系", "faculty_url": "https://www.esc.cam.ac.uk/people/academic-staff", "qs_subject_rank": "Top 10", "notes": "Strong in seismology", "status": "pending" },
    { "name": "University of Oxford", "region": "uk_ireland", "country": "UK", "country_zh": "英国", "department": "Earth Sciences", "department_zh": "地球科学系", "faculty_url": "https://www.earth.ox.ac.uk/people/", "qs_subject_rank": "Top 10", "notes": "", "status": "pending" },
    { "name": "Imperial College London", "region": "uk_ireland", "country": "UK", "country_zh": "英国", "department": "Earth Science & Engineering", "department_zh": "地球科学与工程系", "faculty_url": "https://www.imperial.ac.uk/earth-science/people/academic-staff/", "qs_subject_rank": "Top 20", "notes": "", "status": "pending" },
    { "name": "University of Edinburgh", "region": "uk_ireland", "country": "UK", "country_zh": "英国", "department": "GeoSciences", "department_zh": "地球科学学院", "faculty_url": "https://www.geos.ed.ac.uk/people", "qs_subject_rank": "Top 20", "notes": "", "status": "pending" },
    { "name": "University of Southampton", "region": "uk_ireland", "country": "UK", "country_zh": "英国", "department": "Ocean and Earth Science", "department_zh": "海洋与地球科学系", "faculty_url": "https://www.southampton.ac.uk/oes/about/staff.page", "qs_subject_rank": "Top 30", "notes": "Marine seismology strong", "status": "pending" },
    { "name": "University of Bristol", "region": "uk_ireland", "country": "UK", "country_zh": "英国", "department": "Earth Sciences", "department_zh": "地球科学系", "faculty_url": "https://www.bristol.ac.uk/earthsciences/people/", "qs_subject_rank": "Top 30", "notes": "", "status": "pending" },
    { "name": "ETH Zürich", "region": "europe_mainland", "country": "Switzerland", "country_zh": "瑞士", "department": "Earth Sciences", "department_zh": "地球科学系", "faculty_url": "https://erdw.ethz.ch/en/people/professors.html", "qs_subject_rank": "Top 5", "notes": "Top geophysics", "status": "pending" },
    { "name": "Utrecht University", "region": "europe_mainland", "country": "Netherlands", "country_zh": "荷兰", "department": "Earth Sciences", "department_zh": "地球科学系", "faculty_url": "https://www.uu.nl/en/research/department-of-earth-sciences/people", "qs_subject_rank": "Top 30", "notes": "", "status": "pending" },
    { "name": "LMU München", "region": "europe_mainland", "country": "Germany", "country_zh": "德国", "department": "Earth and Environmental Sciences", "department_zh": "地球与环境科学系", "faculty_url": "https://www.geophysik.uni-muenchen.de/people", "qs_subject_rank": "Top 30", "notes": "Geophysics", "status": "pending" },
    { "name": "University of Bergen", "region": "europe_mainland", "country": "Norway", "country_zh": "挪威", "department": "Earth Science", "department_zh": "地球科学系", "faculty_url": "https://www.uib.no/en/geo/people", "qs_subject_rank": "Top 50", "notes": "Marine geoscience", "status": "pending" },
    { "name": "Université Grenoble Alpes", "region": "europe_mainland", "country": "France", "country_zh": "法国", "department": "Earth Sciences", "department_zh": "地球科学系", "faculty_url": "https://www.isterre.fr/en/the-institute/organization/", "qs_subject_rank": "Top 50", "notes": "", "status": "pending" },
    { "name": "University of Bologna", "region": "europe_mainland", "country": "Italy", "country_zh": "意大利", "department": "Physics and Astronomy", "department_zh": "物理与天文学系", "faculty_url": "https://fisica-astronomia.unibo.it/en/people", "qs_subject_rank": "Top 100", "notes": "Geophysics group", "status": "pending" },
    { "name": "MIT", "region": "usa_canada", "country": "US", "country_zh": "美国", "department": "EAPS", "department_zh": "地球大气与行星科学系", "faculty_url": "https://eapsweb.mit.edu/people/faculty/", "qs_subject_rank": "Top 5", "notes": "Strong seismology", "status": "pending" },
    { "name": "Caltech", "region": "usa_canada", "country": "US", "country_zh": "美国", "department": "GPS / Seismolab", "department_zh": "地质与行星科学系", "faculty_url": "https://www.gps.caltech.edu/people/faculty", "qs_subject_rank": "Top 5", "notes": "Top seismology globally", "status": "pending" },
    { "name": "Stanford University", "region": "usa_canada", "country": "US", "country_zh": "美国", "department": "Earth & Planetary Sciences", "department_zh": "地球与行星科学系", "faculty_url": "https://earth.stanford.edu/people/faculty", "qs_subject_rank": "Top 10", "notes": "", "status": "pending" },
    { "name": "UC San Diego / Scripps", "region": "usa_canada", "country": "US", "country_zh": "美国", "department": "Scripps Institution of Oceanography", "department_zh": "斯克里普斯海洋研究所", "faculty_url": "https://scripps.ucsd.edu/people/faculty", "qs_subject_rank": "Top 10", "notes": "Key target for OBS", "status": "pending" },
    { "name": "Columbia University / Lamont", "region": "usa_canada", "country": "US", "country_zh": "美国", "department": "Lamont-Doherty Earth Observatory", "department_zh": "拉蒙特-多爾蒂地球觀測站", "faculty_url": "https://lamont.columbia.edu/directory/people", "qs_subject_rank": "Top 10", "notes": "", "status": "pending" },
    { "name": "University of Washington", "region": "usa_canada", "country": "US", "country_zh": "美国", "department": "Earth & Space Sciences", "department_zh": "地球与空间科学系", "faculty_url": "https://www.ess.washington.edu/people/", "qs_subject_rank": "Top 20", "notes": "", "status": "pending" },
    { "name": "UT Austin", "region": "usa_canada", "country": "US", "country_zh": "美国", "department": "Jackson School of Geosciences", "department_zh": "杰克逊地球科学学院", "faculty_url": "https://www.jsg.utexas.edu/people/", "qs_subject_rank": "Top 20", "notes": "", "status": "pending" },
    { "name": "CU Boulder", "region": "usa_canada", "country": "US", "country_zh": "美国", "department": "Geological Sciences", "department_zh": "地质科学系", "faculty_url": "https://www.colorado.edu/geologicalsciences/people/faculty", "qs_subject_rank": "Top 30", "notes": "", "status": "pending" },
    { "name": "UBC", "region": "usa_canada", "country": "Canada", "country_zh": "加拿大", "department": "EOAS", "department_zh": "地球海洋与大气科学系", "faculty_url": "https://www.eoas.ubc.ca/people/faculty", "qs_subject_rank": "Top 20", "notes": "Strong seismology", "status": "pending" },
    { "name": "University of Toronto", "region": "usa_canada", "country": "Canada", "country_zh": "加拿大", "department": "Earth Sciences", "department_zh": "地球科学系", "faculty_url": "https://www.es.utoronto.ca/people/faculty/", "qs_subject_rank": "Top 30", "notes": "", "status": "pending" },
    { "name": "University of Victoria", "region": "usa_canada", "country": "Canada", "country_zh": "加拿大", "department": "Earth and Ocean Sciences", "department_zh": "地球与海洋科学系", "faculty_url": "https://www.uvic.ca/science/seos/people/faculty/index.php", "qs_subject_rank": "Top 100", "notes": "Marine seismology", "status": "pending" },
    { "name": "McGill University", "region": "usa_canada", "country": "Canada", "country_zh": "加拿大", "department": "Earth & Planetary Sciences", "department_zh": "地球与行星科学系", "faculty_url": "https://www.mcgill.ca/eps/people/faculty", "qs_subject_rank": "Top 50", "notes": "", "status": "pending" },
    { "name": "ANU", "region": "australia_nz", "country": "Australia", "country_zh": "澳大利亚", "department": "Research School of Earth Sciences", "department_zh": "地球科学研究院", "faculty_url": "https://earthsciences.anu.edu.au/people/academics", "qs_subject_rank": "Top 10", "notes": "Top globally", "status": "pending" },
    { "name": "University of Melbourne", "region": "australia_nz", "country": "Australia", "country_zh": "澳大利亚", "department": "Geography, Earth and Atmospheric Sciences", "department_zh": "地理地球与大气科学系", "faculty_url": "https://sgeas.unimelb.edu.au/people", "qs_subject_rank": "Top 30", "notes": "", "status": "pending" },
    { "name": "Victoria University of Wellington", "region": "australia_nz", "country": "New Zealand", "country_zh": "新西兰", "department": "Geography, Environment and Earth Sciences", "department_zh": "地理环境与地球科学系", "faculty_url": "https://www.wgtn.ac.nz/sgees/about/staff", "qs_subject_rank": "Top 100", "notes": "Home of GeoNet", "status": "pending" },
    { "name": "NTU", "region": "singapore_hongkong", "country": "Singapore", "country_zh": "新加坡", "department": "Earth Observatory of Singapore", "department_zh": "新加坡地球观测站", "faculty_url": "https://earthobservatory.sg/people", "qs_subject_rank": "Top 30", "notes": "Strong seismology", "status": "pending" },
    { "name": "NUS", "region": "singapore_hongkong", "country": "Singapore", "country_zh": "新加坡", "department": "Earth Sciences", "department_zh": "地球科学系", "faculty_url": "https://www.nus.edu.sg/ees/people/", "qs_subject_rank": "Top 50", "notes": "", "status": "pending" },
    { "name": "HKU", "region": "singapore_hongkong", "country": "Hong Kong", "country_zh": "香港", "department": "Earth Sciences", "department_zh": "地球科学系", "faculty_url": "https://www.earthsciences.hku.hk/people/academic-staff/", "qs_subject_rank": "Top 50", "notes": "", "status": "pending" }
  ]
}
```

- [ ] **Step 2: Commit**

```bash
git add AdvisorScout/universities.json
git commit -m "feat: add universities.json with 30 core geoscience departments"
```

---

### Task 2: Create verify_urls.py utility

**Files:**
- Create: `AdvisorScout/verify_urls.py`

- [ ] **Step 1: Write verify_urls.py**

```python
"""Batch URL verification tool for universities.json."""
import requests
import json
import sys
from typing import Optional


def verify_urls(json_path: str = "universities.json", timeout: int = 10) -> int:
    """
    Verify all pending faculty URLs in universities.json.
    Updates status to 'verified' (200) or 'broken' (non-200 / error).
    Returns number of broken URLs.
    """
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    broken_count = 0
    total = 0

    for uni in data["universities"]:
        if uni["status"] not in ("pending", "broken"):
            continue
        total += 1
        name = uni["name"]
        url = uni["faculty_url"]
        try:
            resp = requests.head(url, timeout=timeout, allow_redirects=True,
                                headers={"User-Agent": "Mozilla/5.0"})
            if resp.status_code == 200:
                uni["status"] = "verified"
                print(f"✅ {name}: 200 OK")
            else:
                uni["status"] = "broken"
                broken_count += 1
                print(f"❌ {name}: HTTP {resp.status_code}")
        except requests.exceptions.Timeout:
            uni["status"] = "broken"
            broken_count += 1
            print(f"❌ {name}: Timeout ({timeout}s)")
        except requests.exceptions.ConnectionError:
            uni["status"] = "broken"
            broken_count += 1
            print(f"❌ {name}: Connection refused")
        except Exception as e:
            uni["status"] = "broken"
            broken_count += 1
            print(f"❌ {name}: {str(e)[:80]}")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\nDone: {total} checked, {total - broken_count} verified, {broken_count} broken")
    return broken_count


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "universities.json"
    sys.exit(verify_urls(path))
```

- [ ] **Step 2: Run verification**

```bash
cd AdvisorScout && python verify_urls.py
```

Expected: prints ✅/❌ per university, updates universities.json status fields, exits with broken count

- [ ] **Step 3: If broken URLs exist, fix manually**

For each ❌, open the URL in browser. If accessible, set status to "verified". If not found, search the department website for correct faculty URL and update. If none exists, mark "not_found".

- [ ] **Step 4: Commit**

```bash
git add AdvisorScout/verify_urls.py AdvisorScout/universities.json
git commit -m "feat: add verify_urls.py utility and verified university URLs"
```

---

### Task 3: Replace keywords and remove university lists in config.py

**Files:**
- Modify: `AdvisorScout/config.py`

- [ ] **Step 1: Replace DEFAULT_KEYWORDS (lines 13-54)**

Delete the 5 old keyword groups and replace with:

```python
DEFAULT_KEYWORDS = {
    "seismology": [
        "seismology", "earthquake", "seismic",
        "seismic signal processing", "repeating earthquake",
        "repeating signal", "seismic detection",
        "ocean bottom seismometer", "OBS", "OBST", "OBFN",
        "seismic tomography", "seismic imaging",
        "seismic inversion", "bayesian inversion",
        "transdimensional inversion", "rjMCMC",
        "reversible jump MCMC",
        "seismic interferometry", "ambient noise",
        "surface wave", "body wave",
        "earthquake location", "hypocenter",
        "phase picking", "P arrival", "S arrival",
        "seismic phase identification",
        "template matching", "matched filter",
        "cross-correlation", "signal detection",
    ],
    "geophysics": [
        "geophysics", "solid earth geophysics",
        "marine geophysics", "ocean bottom seismology",
        "crustal structure", "mantle structure",
        "subduction zone", "continental margin",
        "seafloor", "marine seismic",
        "South China Sea", "tectonics",
        "geodesy", "GPS geodesy", "InSAR",
    ],
    "signal_processing": [
        "signal processing", "time series analysis",
        "pattern recognition", "machine learning",
        "deep learning", "neural network",
        "convolutional neural network", "transformer",
        "attention mechanism", "autoencoder",
        "transfer learning", "self-supervised learning",
    ],
}
```

- [ ] **Step 2: Replace SCHOLAR_SEARCH_QUERIES (lines 93-114)**

Delete old queries and replace with:

```python
SCHOLAR_SEARCH_QUERIES = [
    "earthquake seismology",
    "seismic tomography",
    "marine geophysics",
    "ambient noise tomography",
    "ocean bottom seismometer",
    "seismic imaging",
    "subduction zone geophysics",
    "earthquake early warning",
    "seismic signal processing",
    "repeating earthquake detection",
    "crustal structure seismology",
    "geodesy InSAR earthquake",
]
```

- [ ] **Step 3: Delete QS_UNIVERSITIES_US (lines 121-257)**

Remove the entire `QS_UNIVERSITIES_US` list.

- [ ] **Step 4: Delete QS_UNIVERSITIES_AUSTRALIA (lines 259-298)**

Remove the entire `QS_UNIVERSITIES_AUSTRALIA` list.

- [ ] **Step 5: Delete QS_RANK_BRACKETS (lines 301-387)**

Remove the entire `QS_RANK_BRACKETS` dict.

- [ ] **Step 6: Delete get_rank_bracket() function (lines 389-391)**

Remove the function.

- [ ] **Step 7: Delete ALL_TARGET_UNIVERSITIES set (lines 394-400)**

Remove the set and the loop that populates it.

- [ ] **Step 8: Verify config.py loads without error**

```bash
cd AdvisorScout && python -c "from config import SEARCH_KEYWORDS, SCHOLAR_SEARCH_QUERIES; print('Keywords loaded:', list(SEARCH_KEYWORDS.keys())); print('Scholar queries:', len(SCHOLAR_SEARCH_QUERIES))"
```

Expected:
```
Keywords loaded: ['seismology', 'geophysics', 'signal_processing']
Scholar queries: 12
```

- [ ] **Step 9: Commit**

```bash
git add AdvisorScout/config.py
git commit -m "feat: replace EE/AI keywords with geoscience keywords, remove hardcoded university lists"
```

---

### Task 4: Add load_universities() to main.py

**Files:**
- Modify: `AdvisorScout/main.py`

- [ ] **Step 1: Add load_universities() function**

Insert after the imports (after line 32) but before the logging setup (line 39):

```python
UNIVERSITIES_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "universities.json")


def load_universities(json_path: str = UNIVERSITIES_FILE) -> List[Tuple[str, str, str]]:
    """Load university targets from universities.json. Returns list of (name, department, url)."""
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
```

Note: requires `from typing import List, Tuple` added to the existing typing import (line 21).

- [ ] **Step 2: Update the typing import in main.py**

Change line 21 from:
```python
from typing import List, Dict, Optional
```
to:
```python
from typing import List, Dict, Optional, Tuple
```

- [ ] **Step 3: Delete FACULTY_URLS list (lines 351-445)**

Remove the entire `FACULTY_URLS` list definition.

- [ ] **Step 4: Update main() to use load_universities()**

In `main()` function, replace:
```python
    finder = ProfessorFinder()
    finder.update_status(phase="Phase 1: Scraping Directories", total_urls=len(FACULTY_URLS))

    # Phase 1: Scrape faculty directories
    logger.info("PHASE 1: Scraping faculty directories...")
    for i, (uni, dept, url) in enumerate(FACULTY_URLS, 1):
```

with:
```python
    finder = ProfessorFinder()
    targets = load_universities()
    finder.update_status(phase="Phase 1: Scraping Directories", total_urls=len(targets))

    # Phase 1: Scrape faculty directories
    logger.info("PHASE 1: Scraping faculty directories...")
    for i, (uni, dept, url) in enumerate(targets, 1):
```

- [ ] **Step 5: Verify main.py loads without error**

```bash
cd AdvisorScout && python -c "from main import load_universities; targets = load_universities(); print(f'Loaded {len(targets)} university targets')"
```

Expected: `Loaded N university targets` (where N = number of verified/enabled universities)

- [ ] **Step 6: Commit**

```bash
git add AdvisorScout/main.py
git commit -m "feat: extract hardcoded FACULTY_URLS to load_universities() reading from universities.json"
```

---

### Task 5: Adapt csv_export.py to remove config dependencies

**Files:**
- Modify: `AdvisorScout/output/csv_export.py`

- [ ] **Step 1: Remove get_rank_bracket import, replace with universities.json lookup**

Replace line 12:
```python
from config import get_rank_bracket
```
with a helper function that reads from universities.json:

```python
import os
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
    data = _load_universities()
    for uni in data.get("universities", []):
        if uni["name"].lower() == university.lower():
            return uni
    return None
```

- [ ] **Step 2: Update the export_csv row writer**

In `export_csv()`, replace the country/bracket lines (lines 59-61):
```python
            country = _get_country(prof.university)
            bracket = get_rank_bracket(prof.university)
```
with:
```python
            info = _get_university_info(prof.university)
            country = info.get("country", _get_country(prof.university)) if info else _get_country(prof.university)
            bracket = info.get("qs_subject_rank", "") if info else ""
```

Also remove `"QS Rank Bracket"` from fieldnames and replace with `"QS Subject Rank"`:
Change in fieldnames list (line 27):
```python
        "QS Rank Bracket",
```
to:
```python
        "QS Subject Rank",
```

And update the column header spelling: `"QS Subject Rank"` in row 27, and update the writerow key (line 63) to match.

- [ ] **Step 3: Verify csv_export loads without error**

```bash
cd AdvisorScout && python -c "from output.csv_export import export_csv; print('csv_export module OK')"
```

Expected: `csv_export module OK`

- [ ] **Step 4: Commit**

```bash
git add AdvisorScout/output/csv_export.py
git commit -m "feat: adapt csv_export to use universities.json instead of hardcoded rank brackets"
```

---

### Task 6: Implement i18n in html_report.py

**Files:**
- Modify: `AdvisorScout/output/html_report.py`

This is the largest task. The generated HTML template needs i18n data and JS logic embedded.

- [ ] **Step 1: Add i18n data block after the `<style>` closing tag**

After the closing `</style>` tag (line 219), insert the i18n JavaScript data:

```javascript
const I18N = {
  'app.title': { en: 'Global Geoscience Advisor Finder', zh: '全球地学导师搜索工具' },
  'app.subtitle': { en: 'Target: 150+ Universities Worldwide', zh: '覆盖：全球150+所大学' },
  'btn.start': { en: 'Start New Scan', zh: '开始新扫描' },
  'btn.start.running': { en: 'Scanning in progress...', zh: '扫描进行中...' },
  'btn.start.done': { en: 'Scan Complete (Click to restart)', zh: '扫描完成（点击重新开始）' },
  'btn.config': { en: 'Configure Keywords', zh: '配置关键词' },
  'status.idle': { en: 'Idle', zh: '空闲' },
  'status.ready': { en: 'Ready to begin', zh: '准备开始' },
  'stat.total': { en: 'Total Professors', zh: '教授总数' },
  'stat.unis': { en: 'Universities', zh: '大学数量' },
  'stat.email': { en: 'With Email', zh: '有邮箱' },
  'filter.search': { en: 'Search name, interest, university...', zh: '搜索姓名、研究方向、大学...' },
  'filter.match': { en: 'Match Level', zh: '匹配等级' },
  'filter.all': { en: 'All Matches', zh: '全部匹配' },
  'filter.high': { en: 'High Match', zh: '高度匹配' },
  'filter.good': { en: 'Good Match', zh: '良好匹配' },
  'filter.partial': { en: 'Partial Match', zh: '部分匹配' },
  'filter.region': { en: 'Region', zh: '地区' },
  'filter.worldwide': { en: 'Worldwide', zh: '全球' },
  'filter.us': { en: 'United States', zh: '美国' },
  'filter.australia': { en: 'Australia', zh: '澳大利亚' },
  'filter.contact': { en: 'Contact', zh: '联系方式' },
  'filter.has_email': { en: 'Has Email', zh: '有邮箱' },
  'card.scholar': { en: 'Scholar', zh: '学术档案' },
  'card.profile': { en: 'Profile', zh: '个人主页' },
  'card.email': { en: 'Email', zh: '邮箱' },
  'card.no_email': { en: 'Email not found', zh: '未找到邮箱' },
  'card.matched_kw': { en: 'Matched Keywords', zh: '匹配关键词' },
  'card.pubs': { en: 'Recent Publications', zh: '近期论文' },
  'card.citations': { en: 'citations', zh: '引用' },
  'card.h_index': { en: 'h-index', zh: 'h指数' },
  'card.citations_total': { en: 'Citations', zh: '总引用' },
  'modal.title': { en: 'Configure Keywords', zh: '配置关键词' },
  'modal.loading': { en: 'Loading keywords...', zh: '加载关键词中...' },
  'modal.fail': { en: 'Failed to load keywords.', zh: '加载关键词失败。' },
  'modal.save': { en: 'Save Configuration', zh: '保存配置' },
  'modal.cancel': { en: 'Cancel', zh: '取消' },
  'modal.saving': { en: 'Saving...', zh: '保存中...' },
  'modal.saved': { en: 'Configuration saved! Next scan will use new keywords.', zh: '配置已保存！下次扫描将使用新关键词。' },
  'modal.save_fail': { en: 'Failed to save configuration.', zh: '保存配置失败。' },
  'footer.generated': { en: 'Generated on', zh: '生成于' },
};

function __(key) {
  const entry = I18N[key];
  if (!entry) return key;
  return entry[currentLang] || entry.en || key;
}

let currentLang = 'en';

function initLanguage() {
  const saved = localStorage.getItem('advisor-scout-lang');
  if (saved && (saved === 'en' || saved === 'zh')) {
    currentLang = saved;
  } else if (navigator.language.startsWith('zh')) {
    currentLang = 'zh';
  } else {
    currentLang = 'en';
  }
  applyLanguage();
  updateLangToggle();
}

function toggleLanguage() {
  currentLang = currentLang === 'en' ? 'zh' : 'en';
  localStorage.setItem('advisor-scout-lang', currentLang);
  applyLanguage();
  updateLangToggle();
}

function applyLanguage() {
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.dataset.i18n;
    const text = __(key);
    if (el.tagName === 'INPUT' && el.type === 'text') {
      el.placeholder = text;
    } else {
      el.textContent = text;
    }
  });
  document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
    el.placeholder = __(el.dataset.i18nPlaceholder);
  });
}

function updateLangToggle() {
  const btn = document.getElementById('lang-toggle');
  if (btn) {
    btn.innerHTML = currentLang === 'en' ? '🌐 中文' : '🌐 English';
  }
}

document.addEventListener('DOMContentLoaded', initLanguage);
```

- [ ] **Step 2: Update the HTML template — sidebar hero**

Replace the hero section (inside .sidebar .hero):
```html
  <div class="hero">
    <h1 data-i18n="app.title">🎓 Global Geoscience Advisor Finder</h1>
    <p data-i18n="app.subtitle">Target: 150+ Universities Worldwide</p>
  </div>
```

- [ ] **Step 3: Update start button text**

```html
    <button class="start-btn" id="start-btn" data-i18n="btn.start">
        🚀 Start New Scan
    </button>
```

- [ ] **Step 4: Update config button text**

```html
    <button class="config-btn" id="config-btn" data-i18n="btn.config">
        ⚙️ Configure Keywords
    </button>
```

- [ ] **Step 5: Update status panel**

```html
    <div class="status-header">
        <span class="status-title" id="status-phase" data-i18n="status.idle">Idle</span>
        <span class="status-percent" id="status-percent">0%</span>
    </div>
    <span class="status-text" id="status-uni" data-i18n="status.ready">Ready to begin</span>
```

- [ ] **Step 6: Update stats labels**

```html
    <div class="stat wide"><div class="num" id="stat-total">{total}</div><div class="label" data-i18n="stat.total">Total Professors</div></div>
    <div class="stat"><div class="num" id="stat-unis">{unis}</div><div class="label" data-i18n="stat.unis">Universities</div></div>
    <div class="stat"><div class="num" id="stat-email">{with_email}</div><div class="label" data-i18n="stat.email">With Email</div></div>
```

- [ ] **Step 7: Update search input**

```html
<input type="text" class="search-box" id="search" data-i18n-placeholder="filter.search" placeholder="🔍 Search name, interest, university...">
```

- [ ] **Step 8: Update filter labels and buttons**

```html
<span class="filter-label" data-i18n="filter.match">Match Level</span>
<button class="filter-btn active" data-filter="all" data-i18n="filter.all">🌐 All Matches <span class="count-badge">{total}</span></button>
<button class="filter-btn" data-filter="high" data-i18n="filter.high">🔥 High Match <span class="count-badge">{high}</span></button>
<button class="filter-btn" data-filter="good" data-i18n="filter.good">⭐ Good Match <span class="count-badge">{good}</span></button>

<span class="filter-label" data-i18n="filter.region">Region</span>
<button class="filter-btn" data-region="all" id="reg-all" data-i18n="filter.worldwide">🌍 Worldwide</button>
<button class="filter-btn" data-region="us" id="reg-us">🇺🇸 <span data-i18n="filter.us">United States</span> <span class="count-badge">{us_count}</span></button>
<button class="filter-btn" data-region="australia" id="reg-au">🇦🇺 <span data-i18n="filter.australia">Australia</span> <span class="count-badge">{au_count}</span></button>

<span class="filter-label" data-i18n="filter.contact">Contact</span>
<button class="filter-btn" data-filter="email" data-i18n="filter.has_email">📧 Has Email <span class="count-badge">{with_email}</span></button>
```

- [ ] **Step 9: Add language toggle button to sidebar footer**

After `</div>` of `.controls` div, before `.footer`:
```html
<div style="text-align:center;padding:1rem 0;">
    <button id="lang-toggle" onclick="toggleLanguage()" style="background:var(--glass);border:1px solid var(--border);border-radius:12px;color:var(--text);padding:0.6rem 1.2rem;cursor:pointer;font-size:0.85rem;font-weight:600;transition:all .2s;width:100%"
        onmouseover="this.style.background='rgba(255,255,255,0.08)'" onmouseout="this.style.background='var(--glass)'">
        🌐 中文
    </button>
</div>
```

- [ ] **Step 10: Update professor card labels**

In the cards_html building loop, update card section labels:

Change `'<h4>📄 Recent Publications</h4>'` → `'<h4>📄 <span data-i18n="card.pubs">Recent Publications</span></h4>'`

Change `'<h4>🎯 Matched Keywords</h4>'` → `'<h4>🎯 <span data-i18n="card.matched_kw">Matched Keywords</span></h4>'`

Update button text:
- Scholar button: `'🎓 <span data-i18n="card.scholar">Scholar</span>'`
- Profile button: `'🔗 <span data-i18n="card.profile">Profile</span>'`
- Email button: `'📧 <span data-i18n="card.email">Email</span>'`
- No email: `'<span data-i18n="card.no_email">Email not found</span>'`

Update metrics:
- `'h-index: {p.h_index}'` → `'<span data-i18n="card.h_index">h-index</span>: {p.h_index}'`
- `'Citations: {p.citations_total:,}'` → `'<span data-i18n="card.citations_total">Citations</span>: {p.citations_total:,}'`
- `'({pub.citations} citations)'` → `'({pub.citations} <span data-i18n="card.citations">citations</span>)'`

Note: all these `data-i18n` elements are inside the Python f-string template for each card — they're literal HTML strings output in the generated report.

- [ ] **Step 11: Update footer**

```html
<div class="footer"><span data-i18n="footer.generated">Generated on</span><br>{datetime.now().strftime("%b %d, %Y at %I:%M %p")}</div>
```

- [ ] **Step 12: Update modal**

- Modal title: `'<h2 data-i18n="modal.title">Configure Keywords</h2>'`
- Loading text: `'<p style="text-align:center;padding:2rem;" data-i18n="modal.loading">Loading keywords...</p>'`
- Failure text: `'<p style="color:var(--red);text-align:center;padding:2rem;" data-i18n="modal.fail">Failed to load keywords.</p>'`
- Save button: `'<button class="btn-save" id="btn-save" data-i18n="modal.save">Save Configuration</button>'`
- Cancel button: `'<button class="btn-cancel" id="btn-cancel" data-i18n="modal.cancel">Cancel</button>'`

- [ ] **Step 13: Update JS alert/confirm messages in the inline script**

Replace hardcoded strings in JS:

In the start button handler:
```javascript
if (confirm(currentLang === 'zh' ? '确认开始全新扫描所有大学？这可能需要10-20分钟。' : 'Start a fresh scan of all universities? This may take 10-20 minutes.')) {
```

In the config save handler:
```javascript
btnSave.innerText = __('modal.saving');
btnSave.disabled = true;
```
and
```javascript
alert(__('modal.saved'));
```
and
```javascript
alert(__('modal.save_fail'));
```

In the pollStatus function, update start button text:
```javascript
startBtn.innerText = __('btn.start.running');
```
and
```javascript
startBtn.innerText = __('btn.start.done');
```

- [ ] **Step 14: Regenerate the HTML report**

```bash
cd AdvisorScout && python -c "
from models import Professor
from output.html_report import generate_html_report
# Test with empty data
generate_html_report([], 'results/test_i18n.html')
print('HTML report generated successfully')
"
```

Expected: `HTML report generated successfully`

- [ ] **Step 15: Commit**

```bash
git add AdvisorScout/output/html_report.py
git commit -m "feat: add Chinese/English i18n to dashboard with language toggle"
```

---

### Task 7: End-to-end test

**Files:**
- None new

- [ ] **Step 1: Verify the complete import chain**

```bash
cd AdvisorScout && python -c "
from config import SEARCH_KEYWORDS, load_keywords
from models import Professor, Publication
from matcher import KeywordMatcher
from main import load_universities, ProfessorFinder
print('All imports OK')
print(f'Universities: {len(load_universities())}')
print(f'Keyword groups: {list(SEARCH_KEYWORDS.keys())}')
"
```

Expected: all imports pass, shows university count and keyword groups

- [ ] **Step 2: Dry-run a single university scrape**

```bash
cd AdvisorScout && python -c "
from main import ProfessorFinder
finder = ProfessorFinder()
# Test with first university only
from main import load_universities
targets = load_universities()
if targets:
    uni, dept, url = targets[0]
    print(f'Testing scrape: {uni} - {dept}')
    profs = finder.scrape_faculty_page(url, uni, dept)
    print(f'Found {len(profs)} professors')
    for p in profs[:3]:
        print(f'  - {p.name}')
"
```

Expected: scrapes one university, prints found professor count, no crashes

- [ ] **Step 3: Verify HTML report generation with sample data**

```bash
cd AdvisorScout && python -c "
from models import Professor, Publication
from matcher import KeywordMatcher
from output.html_report import generate_html_report
from output.csv_export import export_csv

# Create a sample professor
p = Professor(
    name='Test Professor', university='Test University',
    department='Earth Sciences', title='Associate Professor',
    email='test@example.com', profile_url='https://example.com',
    research_interests=['seismology', 'seismic tomography'],
    bio='Research on earthquake detection using deep learning.',
    publications=[Publication(title='Deep Learning for Seismic Detection', year='2024', citations=42)],
    match_score=3.5,
    matched_keywords=['seismology', 'seismic tomography', 'deep learning'],
    h_index=25, citations_total=5000,
)
matcher = KeywordMatcher()
matcher.score_professor(p)

generate_html_report([p], 'results/test_e2e.html')
export_csv([p], 'results/test_e2e.csv')
print('Reports generated successfully')
"
```

Expected: creates `results/test_e2e.html` and `results/test_e2e.csv`

- [ ] **Step 4: Commit**

```bash
git add -A
git commit -m "test: end-to-end verification passes for geoscience refactor"
```

---

### Task 8: Update README.md

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Rewrite README**

Replace current README with geoscience-focused English README covering:
- Project name: Global Geoscience Advisor Finder
- What it does: automated discovery of geoscience PhD advisors worldwide
- Coverage: 150+ universities across UK, Europe, US, Canada, Australia, NZ, Singapore, Hong Kong
- Quick start: `pip install -r requirements.txt && python main.py && python app.py`
- How to configure: edit `universities.json` and `config.py`
- How to add new universities
- Credits to original AdvisorScout project

- [ ] **Step 2: Commit**

```bash
git add README.md
git commit -m "docs: rewrite README for global geoscience advisor finder"
```

---

### Task 9: Cleanup

**Files:**
- Various

- [ ] **Step 1: Add .gitignore entries**

Add to `.gitignore` if not present:
```
.superpowers/
results/
cache.json
*.log
__pycache__/
```

- [ ] **Step 2: Remove stale generated files from git tracking**

```bash
git rm --cached AdvisorScout/cache.json AdvisorScout/results/professors_data.csv AdvisorScout/results/professors_report.html AdvisorScout/results/status.json 2>/dev/null || true
```

- [ ] **Step 3: Commit**

```bash
git add .gitignore
git commit -m "chore: update .gitignore and remove generated files from tracking"
```
