# 🎓 Global Geoscience Advisor Finder

**Automated PhD Advisor Discovery for Geoscience Researchers | 全球地学导师自动发现工具**

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<details open>
<summary><b>🇬🇧 English</b> (click to collapse / 点击收起)</summary>
<br>

A powerful tool that helps prospective PhD students find academic mentors in geoscience, geophysics, and seismology. Automatically scrapes faculty directories from 150+ universities worldwide, enriches profiles with research data, and ranks them by keyword relevance.

Based on [AdvisorScout](https://github.com/therajpoots/Professor-Finder-Web-Scrapper-and-Dashboard) (MIT License).

### 🚀 Quick Start

```bash
pip install -r requirements.txt
python main.py      # Run pipeline
python app.py       # Launch dashboard → http://localhost:8000
```

### 🌍 Coverage

| Region | Countries | Examples |
|---|---|---|
| UK & Ireland | UK | Cambridge, Oxford, Imperial, Edinburgh, Southampton, Bristol |
| Mainland Europe | CH, NL, DE, NO, FR, IT | ETH Zürich, Utrecht, LMU München, Bergen, Grenoble |
| USA & Canada | US, CA | MIT, Caltech, Stanford, Scripps/UCSD, Columbia/Lamont, UBC |
| Australia & NZ | AU, NZ | ANU, Melbourne, Victoria University of Wellington |
| Singapore & HK | SG, HK | NTU/EOS, NUS, HKU |

### 🏗️ How It Works

1. **Directory Scraping** — Multi-strategy HTML parser discovers faculty from directory pages
2. **Profile Enrichment** — Visits individual profile pages to extract emails, bios, and research interests
3. **Keyword Scoring** — Regex-based matching with category bonuses and interdisciplinary weighting
4. **Report Generation** — Interactive HTML dashboard with filtering, search, and bilingual support

### 📊 Output

- **Interactive HTML Dashboard** — Dark-themed, searchable, filterable by match level, region, contact info. Bilingual (中文/English). Cards collapsed by default — click to expand.
- **Structured CSV** — Spreadsheet-ready with email, h-index, citations, research interests.

### 🌐 Bilingual Dashboard

The generated dashboard supports **中文** and **English**. Click the language toggle (🌐) at the bottom of the sidebar.

</details>

<details>
<summary><b>🇨🇳 中文</b> (点击展开 / click to expand)</summary>
<br>

基于 [AdvisorScout](https://github.com/therajpoots/Professor-Finder-Web-Scrapper-and-Dashboard)（MIT License）改造。帮助准博士生寻找地球科学、地球物理、地震学方向的导师。自动抓取全球 150+ 所大学教员目录，补全个人主页信息，按研究方向关键词匹配评分。

### 🚀 快速开始

```bash
pip install -r requirements.txt
python main.py      # 运行爬取流水线
python app.py       # 启动仪表盘 → http://localhost:8000
```

### 🌍 覆盖区域

| 区域 | 国家 | 示例 |
|---|---|---|
| 英国与爱尔兰 | 英国 | Cambridge, Oxford, Imperial, Edinburgh, Southampton, Bristol |
| 欧洲大陆 | 瑞士、荷兰、德国、挪威、法国、意大利 | ETH Zürich, Utrecht, LMU München, Bergen, Grenoble |
| 美国与加拿大 | 美国、加拿大 | MIT, Caltech, Stanford, Scripps/UCSD, Columbia/Lamont, UBC |
| 澳大利亚与新西兰 | 澳、新 | ANU, Melbourne, Victoria University of Wellington |
| 新加坡与香港 | 新加坡、香港 | NTU/EOS, NUS, HKU |

### 🏗️ 工作原理

1. **目录抓取** — 多策略 HTML 解析
2. **个人页补全** — 提取邮箱、简介、研究方向
3. **关键词评分** — 正则匹配 + 跨类别 + 跨学科加权
4. **报告生成** — 交互式仪表盘 + CSV

### 📊 输出

- **交互式仪表盘**（HTML）— 暗色主题、搜索筛选、卡片折叠、中英文切换。
- **CSV 表格** — 含邮箱、h-index、引用数、研究方向等。

### 🌐 双语切换

仪表盘支持中英文切换，点击侧边栏底部 🌐 按钮即可。

</details>

---

## ⚙️ Configuration / 配置

### Keywords / 关键词

Stored in `keywords.json`. Edit via Web UI (`python app.py` → ⚙️ Configure Keywords) or text editor.

存储在 `keywords.json`，Web 界面或直接编辑均可。

```json
{
  "category_name": ["keyword1", "keyword2"],
  "another_category": ["keyword3"]
}
```

**Scoring / 评分：** Each category +1.0, extra keywords +0.2 each, 2+ categories +0.5, 3+ +1.0.

### Universities / 大学列表

Edit `universities.json`. Run `python verify_urls.py` to verify URLs.

编辑 `universities.json`，运行 `python verify_urls.py` 验证。

### Scraper Settings / 爬虫参数

In `config.py`: `MIN_MATCH_SCORE`, `REQUEST_DELAY`, `MAX_PUBLICATIONS`, `ENABLE_SCHOLAR`.

---

## 📂 Structure / 结构

```
├── keywords.json        ├── models.py
├── universities.json    ├── matcher.py
├── config.py            ├── verify_urls.py
├── main.py              ├── output/
├── app.py               └── results/
```

---

## 📜 License

MIT. Based on [AdvisorScout](https://github.com/therajpoots/Professor-Finder-Web-Scrapper-and-Dashboard).
