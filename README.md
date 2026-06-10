# 🎓 Global Geoscience Advisor Finder

**Automated PhD Advisor Discovery for Geoscience Researchers Worldwide**

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A powerful tool that helps prospective PhD students and researchers find academic mentors in geoscience, geophysics, seismology, and related fields. Automatically scrapes faculty directories from 150+ universities worldwide, enriches profiles with research data, and ranks them by keyword relevance.

Based on [AdvisorScout](https://github.com/therajpoots/Professor-Finder-Web-Scrapper-and-Dashboard) (MIT License).

## 🌍 Coverage

- **UK & Ireland**: Cambridge, Oxford, Imperial, Edinburgh, Southampton, Bristol, +
- **Mainland Europe**: ETH Zürich, Utrecht, LMU München, Bergen, Grenoble, Bologna, +
- **USA & Canada**: MIT, Caltech, Stanford, Scripps, Columbia/Lamont, UW, UT Austin, UBC, +
- **Australia & NZ**: ANU, Melbourne, Victoria University of Wellington, +
- **Singapore & Hong Kong**: NTU/EOS, NUS, HKU

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the full pipeline (scrape → enrich → score → report)
python main.py

# Or use the web dashboard
python app.py
# Open http://localhost:8000 in your browser
```

## ⚙️ Configuration

### Universities
Edit `universities.json` to add or modify target universities. The file is organized by region:

```json
{
  "regions": {
    "uk_ireland": { "name": "UK & Ireland", "name_zh": "英国与爱尔兰", "enabled": true },
    ...
  },
  "universities": [
    {
      "name": "University Name",
      "region": "uk_ireland",
      "country": "UK",
      "department": "Earth Sciences",
      "faculty_url": "https://...",
      "status": "verified"
    }
  ]
}
```

Run `python verify_urls.py` to check URL accessibility.

### Keywords
Edit `keywords.json` (auto-created from web UI) or modify `DEFAULT_KEYWORDS` in `config.py`. Default groups:

| Group | Focus |
|---|---|
| Seismology | Earthquake detection, seismic tomography, OBS, template matching |
| Geophysics | Marine geophysics, crustal structure, subduction zones, geodesy |
| Signal Processing | Deep learning, CNN, transformers, time series analysis |

## 🏗️ How It Works

1. **Directory Scraping** — Multi-strategy HTML parser discovers faculty from directory pages
2. **Profile Enrichment** — Visits individual profile pages to extract emails, bios, and research interests
3. **Keyword Scoring** — Regex-based matching with category bonuses and interdisciplinary weighting
4. **Report Generation** — Interactive HTML dashboard with filtering, search, and bilingual support

## 📊 Output

- **Interactive HTML Dashboard** — Dark-themed, searchable, filterable by match level, region, contact info
- **Structured CSV** — Ready for spreadsheet import with columns for email, h-index, citations, research interests

## 🌐 Bilingual Support

The dashboard supports **Chinese** (中文) and **English**. Click the language toggle button in the sidebar to switch. Language preference is saved in localStorage.

## 📂 Project Structure

```
AdvisorScout/
├── universities.json       # University/department configuration
├── config.py               # Keywords, scraper settings
├── main.py                 # Main orchestrator (4-phase pipeline)
├── app.py                  # Web UI server (port 8000)
├── models.py               # Professor/Publication data models
├── matcher.py              # Keyword matching engine
├── verify_urls.py          # URL verification utility
├── output/
│   ├── html_report.py      # HTML dashboard generator (with i18n)
│   └── csv_export.py       # CSV export
├── keywords.json            # Keyword configuration (via web UI)
├── cache.json               # Scraping cache (gitignore)
├── results/                 # Generated reports (gitignore)
└── README.md
```

## 📜 License

MIT License. Based on [AdvisorScout](https://github.com/therajpoots/Professor-Finder-Web-Scrapper-and-Dashboard).

---

*"Finding the right advisor is 50% of the PhD journey. AdvisorScout does the heavy lifting for you."*
