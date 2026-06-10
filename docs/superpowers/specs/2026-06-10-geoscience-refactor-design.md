# Geoscience Refactor Design

## Overview

Transform AdvisorScout from an ECE/CS professor finder (US+Australia) into a global Geoscience advisor discovery tool covering UK, Europe, US, Canada, Australia, NZ, Singapore, and Hong Kong. Add Chinese/English i18n.

## Data Model

### `universities.json` (new file)

Top-level keys:

- `regions` — dict keyed by region slug, each containing `name`, `name_zh`, `enabled`
- `universities` — list of university objects

University object fields: `name`, `region`, `country`, `country_zh`, `department`, `department_zh`, `faculty_url`, `qs_subject_rank` (optional), `notes` (optional), `status` (pending|verified|broken|not_found)

Enabled regions in scope: uk_ireland, europe_mainland, usa_canada, australia_nz, singapore_hongkong. Remaining ~6 regions as disabled placeholders.

## Code Changes

### 1. `config.py` — Keyword & University List Replacement

**Remove:**
- `DEFAULT_KEYWORDS` (5 EE/AI groups, ~55 keywords)
- `SCHOLAR_SEARCH_QUERIES` (20 EE queries)
- `QS_UNIVERSITIES_US` (~150 lines)
- `QS_UNIVERSITIES_AUSTRALIA` (~40 lines)
- `QS_RANK_BRACKETS` (~90 lines)
- `ALL_TARGET_UNIVERSITIES` set
- `get_rank_bracket()` function

**Replace with 3 keyword groups:**
- `seismology` (~25 keywords: seismology, earthquake, seismic tomography, OBS, template matching, etc.)
- `geophysics` (~15 keywords: geophysics, marine geophysics, subduction zone, InSAR, etc.)
- `signal_processing` (~15 keywords: signal processing, deep learning, CNN, transformer, etc.)

**Replace scholar queries** with ~12 geoscience search queries.

**Keep unchanged:** all scraper parameters (REQUEST_DELAY, MAX_PUBLICATIONS, USER_AGENT, etc.), `load_keywords()`, `KEYWORDS_FILE`.

### 2. `main.py` — Data Extraction

**Remove:** `FACULTY_URLS` list (~90 lines of hardcoded tuples).

**Add:** `load_universities(json_path)` function that reads `universities.json`, filters by enabled regions and non-broken status, returns list of (name, department, url) tuples.

**Modify:** `main()` entry to call `load_universities()` instead of iterating `FACULTY_URLS`.

**Keep unchanged:** `ProfessorFinder` class, all scraping/enrichment/matching/output methods.

### 3. `output/html_report.py` — i18n

**Add JavaScript i18n data block** (~30 key pairs, each with `en`/`zh` values).

**Add JS utilities:** `__(key)` translation function, `initLanguage()` (priority: localStorage → browser language → default zh), `toggleLanguage()`.

**Add toggle button** in sidebar footer (🌐 中文/English).

**Modify ~30 static text locations** in HTML template to use `data-i18n="key"` attributes.

**Not translated:** professor names, research interests, bios, university/department names (keep original).

### 4. `verify_urls.py` (new utility)

Standalone script: reads `universities.json`, sends HEAD requests to each `faculty_url` with status `pending`, updates status to `verified` (200) or `broken` (non-200 / error). Prints summary table.

### 5. `csv_export.py` — Adapt to i18n

Use country/region from `universities.json` instead of hardcoded `_get_country()`. Remove `get_rank_bracket()` dependency.

## Execution Order

1. **Step 1 partial** — Generate `universities.json` with ~30 core universities, URLs, verify
2. **Step 2** — `main.py`: extract FACULTY_URLS → load_universities()
3. **Step 3** — `config.py`: replace keywords and remove university lists
4. **Step 4** — `output/html_report.py`: implement i18n
5. Adapt `csv_export.py` to work without old config dependencies
6. **Step 5** — End-to-end test: scrape → score → report → dashboard
7. **Step 6** — README + release prep

## Non-Goals

- European CMS-specific scraper adaptations (deferred)
- Independent research institute support (GFZ, IPGP, etc.) (deferred)
- Batch email sending (deferred)
- Auto-ranking data sync (deferred)
