# 🎓 Global Geoscience Advisor Finder / 全球地学导师搜索工具

**Automated PhD Advisor Discovery for Geoscience Researchers Worldwide**
**面向全球地球科学研究者的自动化博士导师发现工具**

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

基于 [AdvisorScout](https://github.com/therajpoots/Professor-Finder-Web-Scrapper-and-Dashboard)（MIT License）改造。

A powerful tool that helps prospective PhD students find academic mentors in geoscience, geophysics, and seismology. Automatically scrapes faculty directories from 150+ universities worldwide, enriches profiles with research data, and ranks them by keyword relevance.

一款帮助准博士生寻找地球科学、地球物理、地震学方向导师的工具。自动抓取全球 150+ 所大学的教员目录，补全个人主页信息，按研究方向关键词匹配评分。

---

## 🚀 Quick Start / 快速开始

```bash
pip install -r requirements.txt
python main.py      # Run pipeline / 运行爬取流水线
python app.py       # Launch dashboard / 启动仪表盘 → http://localhost:8000
```

---

## 🌍 Coverage / 覆盖区域

| Region / 区域 | Countries / 国家 | Examples / 示例 |
|---|---|---|
| UK & Ireland / 英国与爱尔兰 | UK | Cambridge, Oxford, Imperial, Edinburgh, Southampton, Bristol |
| Mainland Europe / 欧洲大陆 | Switzerland, Netherlands, Germany, Norway, France, Italy | ETH Zürich, Utrecht, LMU München, Bergen, Grenoble |
| USA & Canada / 美国与加拿大 | US, Canada | MIT, Caltech, Stanford, Scripps/UCSD, Columbia/Lamont, UBC |
| Australia & NZ / 澳大利亚与新西兰 | Australia, New Zealand | ANU, Melbourne, Victoria University of Wellington |
| Singapore & Hong Kong / 新加坡与香港 | Singapore, Hong Kong | NTU/EOS, NUS, HKU |

---

## 🏗️ How It Works / 工作原理

1. **Directory Scraping / 目录抓取** — Multi-strategy HTML parser discovers faculty from directory pages / 多策略 HTML 解析器从目录页发现教员
2. **Profile Enrichment / 个人页补全** — Visits individual profile pages to extract emails, bios, and research interests / 访问个人主页提取邮箱、简介、研究方向
3. **Keyword Scoring / 关键词评分** — Regex-based matching with category bonuses and interdisciplinary weighting / 正则匹配 + 跨类别加分 + 跨学科加权
4. **Report Generation / 报告生成** — Interactive HTML dashboard with filtering, search, and bilingual support / 交互式 HTML 仪表盘，支持筛选、搜索、中英文切换

---

## 📊 Output / 输出

- **Interactive HTML Dashboard / 交互式仪表盘** — Dark-themed, searchable, filterable by match level, region, contact info. Bilingual (中文/English). Cards collapsed by default — click to expand details.
- **Structured CSV / 结构化 CSV** — Spreadsheet-ready with email, h-index, citations, research interests.

---

## 🌐 Bilingual Support / 双语支持

Dashboard supports **中文** and **English**. Click the language toggle (🌐) button at the bottom of the sidebar. Preference saved in localStorage.

仪表盘支持中英文切换，点击侧边栏底部的语言切换按钮（🌐 中文/English）即可。

---

## ⚙️ Configuration / 配置

### Keywords / 关键词

Keywords are stored in `keywords.json` and can be edited in two ways.

关键词存储在 `keywords.json`，有两种修改方式：

**Method 1: Web UI / 方式一：Web 界面**

```bash
python app.py
```

Open `http://localhost:8000`, click **⚙️ Configure Keywords** in the sidebar. Edit each group's keywords (comma-separated), then click **Save Configuration**. The next `python main.py` run will use the new keywords.

打开浏览器，点击侧边栏 **⚙️ Configure Keywords**，编辑各组关键词（逗号分隔），点击 **Save Configuration**。下次运行 `python main.py` 生效。

**Method 2: Direct edit / 方式二：直接编辑**

Open `keywords.json` with any text editor. Format / 格式：

```json
{
  "category_name": [
    "keyword1", "keyword2", "keyword3"
  ],
  "another_category": [
    "keyword4", "keyword5"
  ]
}
```

### Scoring Logic / 评分逻辑

- Each category matched: **+1.0** / 每命中一个类别：+1.0
- Extra keywords in same category: **+0.2** each / 同一类别内额外关键词：每个 +0.2
- 2+ categories matched: **+0.5** bonus / 跨 2 个类别：+0.5
- 3+ categories matched: **+1.0** bonus / 跨 3+ 类别：+1.0

You can add as many keyword groups as you like. If `keywords.json` doesn't exist, defaults in `config.py` (`DEFAULT_KEYWORDS`) are used.

### Universities / 大学列表

Edit `universities.json` to add or modify target universities. Run `python verify_urls.py` to check URL accessibility.

编辑 `universities.json` 添加大学。运行 `python verify_urls.py` 验证 URL。

### Scraper Settings / 爬虫参数

In `config.py`: `MIN_MATCH_SCORE` (default: `1.0`), `REQUEST_DELAY`, `MAX_PUBLICATIONS`, `ENABLE_SCHOLAR`.

---

## 📂 Project Structure / 项目结构

```
AdvisorScout/
├── keywords.json           # Keyword configuration / 关键词配置
├── universities.json       # University list / 大学列表
├── config.py               # Default keywords, scraper settings
├── main.py                 # Main orchestrator / 主编排器
├── app.py                  # Web UI server (port 8000)
├── models.py               # Data models / 数据模型
├── matcher.py              # Keyword matching engine / 匹配引擎
├── verify_urls.py          # URL verification tool / URL 验证工具
├── output/
│   ├── html_report.py      # Dashboard generator (with i18n)
│   └── csv_export.py       # CSV export
├── cache.json              # Scraping cache / 缓存
└── results/                # Generated reports / 报告输出
```

---

## 📜 License / 许可证

MIT License. Based on [AdvisorScout](https://github.com/therajpoots/Professor-Finder-Web-Scrapper-and-Dashboard).

---

*"Finding the right advisor is 50% of the PhD journey." — 找到合适的导师，PhD 之路就完成了一半。*
