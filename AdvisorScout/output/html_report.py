"""
HTML report generator.
Creates a beautiful, self-contained HTML report of found professors with LIVE progress and START button.
"""

import os
import logging
import json
from typing import List, Dict
from datetime import datetime

from models import Professor
import os, json

_UNI_DATA = None

def _load_uni_data():
    global _UNI_DATA
    if _UNI_DATA is None:
        path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "universities.json")
        try:
            with open(path, "r", encoding="utf-8") as f:
                _UNI_DATA = json.load(f)
        except Exception:
            _UNI_DATA = {"universities": []}
    return _UNI_DATA

def _get_uni_info(university: str):
    """Look up country and QS rank for a university from universities.json."""
    data = _load_uni_data()
    for u in data.get("universities", []):
        if u.get("name", "").lower() == university.lower():
            return u
    return {}

COUNTRY_DISPLAY = {
    "US": "America", "United States": "America",
    "UK": "UK", "United Kingdom": "UK",
    "Australia": "Australia", "Canada": "Canada",
    "New Zealand": "New Zealand", "Singapore": "Singapore",
    "Hong Kong": "Hong Kong", "Switzerland": "Switzerland",
    "Netherlands": "Netherlands", "Germany": "Germany",
    "Norway": "Norway", "France": "France",
    "Italy": "Italy", "Mexico": "Mexico",
    "Denmark": "Denmark", "Sweden": "Sweden",
    "Finland": "Finland", "Iceland": "Iceland",
    "Austria": "Austria", "Belgium": "Belgium",
    "Spain": "Spain", "Ireland": "Ireland",
    "Japan": "Japan", "China": "China",
    "South Korea": "South Korea", "Taiwan": "Taiwan",
}

logger = logging.getLogger(__name__)


def generate_html_report(professors: List[Professor], output_path: str):
    """Generate a stunning self-contained HTML report with live progress tracking."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Flat list sorted by score
    professor_cards = ""
    for i, p in enumerate(sorted(professors, key=lambda x: x.match_score, reverse=True)):
        info = _get_uni_info(p.university)
        country_code = info.get("country", _get_country(p.university))
        country_display = COUNTRY_DISPLAY.get(country_code, country_code)
        qs_rank = info.get("qs_subject_rank", "")
        prof_id = f"prof-{i}"

        # Publications
        pubs_html = ""
        for pub in p.publications[:5]:
            cite = f' <span class="cite">({pub.citations} citations)</span>' if pub.citations else ""
            year = f' <span class="year">{pub.year}</span>' if pub.year else ""
            venue = f' — <em>{pub.venue}</em>' if pub.venue else ""
            link = f'<a href="{pub.url}" target="_blank">' if pub.url else ""
            link_end = "</a>" if pub.url else ""
            pubs_html += f'<li>{link}{_esc(pub.title)}{link_end}{year}{venue}{cite}</li>\n'

        pubs_section = ""
        if pubs_html:
            pubs_section = f'<div class="section"><h4>📄 Recent Publications</h4><ul class="pubs">{pubs_html}</ul></div>'

        interests_html = ""
        if p.research_interests:
            tags = "".join(f'<span class="tag">{_esc(i)}</span>' for i in p.research_interests[:6])
            interests_html = f'<div class="tags">{tags}</div>'

        matched_html = ""
        if p.matched_keywords:
            tags = "".join(f'<span class="tag matched">{_esc(k)}</span>' for k in p.matched_keywords[:10])
            matched_html = f'<div class="section"><h4>🎯 Matched Keywords</h4><div class="tags">{tags}</div></div>'

        email_html = f'<a href="mailto:{_esc(p.email)}" class="btn email-btn">📧 Email</a>' if p.email else '<span class="no-email">Email not found</span>'
        profile_html = f'<a href="{_esc(p.profile_url)}" target="_blank" class="btn profile-btn">🔗 Profile</a>' if p.profile_url else ""
        scholar_html = f'<a href="{_esc(p.scholar_url)}" target="_blank" class="btn scholar-btn">🎓 Scholar</a>' if p.scholar_url else ""

        badge_class = "high" if p.match_score >= 3 else "good" if p.match_score >= 2 else "partial"
        metrics = ""
        if p.h_index or p.citations_total:
            h = f'<span class="metric">h-index: {p.h_index}</span>' if p.h_index else ""
            c = f'<span class="metric">Citations: {p.citations_total:,}</span>' if p.citations_total else ""
            metrics = f'<div class="metrics">{h}{c}</div>'

        bio_html = f'<p class="bio">{_esc(p.bio[:400])}</p>' if p.bio else ""

        professor_cards += f'''
<div class="card" data-score="{p.match_score}" data-name="{_esc(p.name.lower())}" data-uni="{_esc(p.university.lower())}" data-country="{_esc(country_display.lower().replace(' ','-'))}" data-id="{prof_id}">
  <button class="bookmark-btn" id="bm-{prof_id}" onclick="event.stopPropagation();toggleBookmark('{prof_id}')" title="Bookmark">☆</button>
  <div class="card-header" onclick="openDrawer('{prof_id}')">
    <div>
      <h3 class="prof-name">{_esc(p.name)}</h3>
      <p class="prof-title">{country_display} | {_esc(p.university)}{(' (' + qs_rank + ')' if qs_rank else '')}</p>
    </div>
    <span class="badge {badge_class}">{p.match_level} ({p.match_score})</span>
  </div>
</div>

<div class="drawer-overlay" id="drawer-{prof_id}" onclick="if(event.target===this)closeDrawer('{prof_id}')">
  <div class="drawer-panel">
    <button class="drawer-close" onclick="closeDrawer('{prof_id}')">&times;</button>
    <h2>{_esc(p.name)}</h2>
    <p class="prof-title">{_esc(p.title or 'Faculty')} — {_esc(p.university)}</p>
    <span class="badge {badge_class}">{p.match_level} ({p.match_score})</span>
    {metrics}
    <div class="section" style="border-top:none;margin-top:1rem;padding-top:0">
      <h4>🏷️ My Tags</h4>
      <div class="tags" id="bm-tags-{prof_id}"></div>
      <input type="text" class="tag-input" placeholder="Add tag... (Enter)" onkeydown="if(event.key==='Enter')addBookmarkTag('{prof_id}',this)" style="margin-top:.5rem;background:var(--glass);border:1px solid var(--border);border-radius:8px;color:var(--text);padding:.4rem .8rem;font-size:.75rem;width:100%">
    </div>
    <div class="section"><h4>📧 Contact</h4><div class="actions">{email_html} {profile_html} {scholar_html}</div></div>
    {matched_html}
    <div class="section"><h4>📖 Research Interests</h4><div class="tags">{interests_html}</div></div>
    {pubs_section}
    <div class="section">
      <h4>Bio</h4>
      <p style="color:var(--text2);font-size:.85rem;line-height:1.6">{_esc(p.bio) if p.bio else 'N/A'}</p>
    </div>
  </div>
</div>'''

    # Stats
    total = len(professors)
    high = sum(1 for p in professors if p.match_score >= 3)
    good = sum(1 for p in professors if 2 <= p.match_score < 3)
    unis = len(set(p.university for p in professors))
    with_email = sum(1 for p in professors if p.email)
    # Country counts
    countries = {}
    for p in professors:
        c = COUNTRY_DISPLAY.get(_get_country(p.university), _get_country(p.university))
        countries[c] = countries.get(c, 0) + 1

    html = f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>PhD Advisor Dashboard — Live</title>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
:root{{--bg:#050508;--surface:#0e0e15;--card:#151525;--border:rgba(255,255,255,0.08);--text:#ffffff;--text2:#a0a0b8;--accent:#7d5fff;--accent2:#b3a4ff;--green:#00d2ad;--orange:#ff9f43;--red:#ff6b6b;--blue:#48dbfb;--glass:rgba(255,255,255,0.03)}}
body{{font-family:'Outfit',sans-serif;background:var(--bg);color:var(--text);line-height:1.6;height:100vh;display:flex;overflow:hidden;}}
.sidebar{{width:340px;height:100vh;background:linear-gradient(180deg,var(--surface) 0%,var(--bg) 100%);border-right:1px solid var(--border);padding:2rem 1.5rem;display:flex;flex-direction:column;overflow-y:auto;flex-shrink:0}}
.main-content{{flex:1;height:100vh;overflow-y:auto;padding:2.5rem;scroll-behavior:smooth;background:radial-gradient(circle at top right, rgba(125,95,255,0.05), transparent 40%)}}

/* Start Button */
.start-box{{margin-bottom:2rem}}
.start-btn{{width:100%;padding:1.2rem;background:linear-gradient(135deg, var(--green), #00b894);border:none;border-radius:16px;color:white;font-weight:700;font-size:1rem;cursor:pointer;transition:all .3s ease;box-shadow:0 8px 25px rgba(0,210,173,0.3);display:flex;align-items:center;justify-content:center;gap:10px}}
.start-btn:hover{{transform:translateY(-3px);box-shadow:0 12px 30px rgba(0,210,173,0.4)}}
.start-btn:active{{transform:translateY(0)}}
.start-btn.running{{background:var(--orange);box-shadow:0 8px 25px rgba(255,159,67,0.3);cursor:wait}}

/* Config Button */
.config-box{{margin-bottom:2rem}}
.config-btn{{width:100%;padding:1rem;background:rgba(255,255,255,0.05);border:1px solid var(--border);border-radius:16px;color:var(--text);font-weight:600;font-size:0.9rem;cursor:pointer;transition:all .3s ease;display:flex;align-items:center;justify-content:center;gap:10px}}
.config-btn:hover{{background:rgba(255,255,255,0.1);border-color:var(--accent)}}

/* Modal Styles */
.modal-overlay{{position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.8);backdrop-filter:blur(10px);display:none;align-items:center;justify-content:center;z-index:1000}}
.modal-content{{background:var(--surface);border:1px solid var(--border);border-radius:24px;width:90%;max-width:800px;max-height:90vh;overflow-y:auto;padding:2.5rem;box-shadow:0 25px 50px rgba(0,0,0,0.5)}}
.modal-header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:2rem}}
.modal-header h2{{font-size:1.5rem;background:linear-gradient(135deg,var(--accent2),var(--blue));-webkit-background-clip:text;-webkit-text-fill-color:transparent}}
.close-modal{{background:none;border:none;color:var(--text2);font-size:1.5rem;cursor:pointer}}
.kw-group{{margin-bottom:1.5rem;background:var(--glass);padding:1.5rem;border-radius:16px;border:1px solid var(--border)}}
.kw-label{{display:block;font-size:0.8rem;color:var(--accent2);font-weight:700;margin-bottom:0.8rem;text-transform:uppercase;letter-spacing:1px}}
.kw-input{{width:100%;background:var(--bg);border:1px solid var(--border);border-radius:12px;color:var(--text);padding:1rem;font-family:inherit;font-size:0.9rem;min-height:80px;resize:vertical}}
.modal-footer{{display:flex;justify-content:flex-end;gap:1rem;margin-top:2rem;padding-top:1.5rem;border-top:1px solid var(--border)}}
.btn-save{{padding:0.8rem 2rem;background:var(--accent);color:white;border:none;border-radius:12px;font-weight:700;cursor:pointer}}
.btn-cancel{{padding:0.8rem 2rem;background:none;color:var(--text2);border:none;cursor:pointer}}

/* Progress Section */
.live-status{{background:rgba(125,95,255,0.05);border:1px solid rgba(125,95,255,0.2);border-radius:16px;padding:1.2rem;margin-bottom:2rem}}
.status-header{{display:flex;justify-content:space-between;margin-bottom:0.5rem}}
.status-title{{font-size:0.7rem;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:var(--accent2)}}
.status-percent{{font-size:0.8rem;font-weight:700;color:var(--accent2)}}
.progress-bar-bg{{height:8px;background:rgba(255,255,255,0.05);border-radius:4px;overflow:hidden;margin-bottom:0.8rem}}
.progress-bar-fill{{height:100%;background:linear-gradient(90deg, var(--accent), var(--blue));width:0%;transition:width 0.5s ease}}
.status-text{{font-size:0.75rem;color:var(--text2);display:block;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}

.hero h1{{font-size:1.8rem;font-weight:700;background:linear-gradient(135deg,var(--accent2),var(--blue));-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:.5rem;line-height:1.2}}
.hero p{{color:var(--text2);font-size:.85rem;margin-bottom:2rem}}
.stats{{display:grid;grid-template-columns:1fr 1fr;gap:0.75rem;margin-bottom:2rem}}
.stat{{background:var(--glass);border:1px solid var(--border);border-radius:16px;padding:1rem;text-align:center;backdrop-filter:blur(10px)}}
.stat.wide{{grid-column:span 2}}
.stat .num{{font-size:1.6rem;font-weight:700;color:var(--accent2);display:block}}
.stat .label{{font-size:.65rem;color:var(--text2);text-transform:uppercase;letter-spacing:1.5px;font-weight:600}}
.controls{{display:flex;flex-direction:column;gap:0.75rem;margin-bottom:2rem}}
.search-box{{width:100%;padding:0.9rem 1.2rem;background:var(--glass);border:1px solid var(--border);border-radius:12px;color:var(--text);font-size:.9rem;outline:none;transition:all .3s;backdrop-filter:blur(10px)}}
.search-box:focus{{border-color:var(--accent);background:rgba(255,255,255,0.06)}}
.filter-group{{display:flex;flex-direction:column;gap:0.5rem}}
.filter-label{{font-size:.7rem;color:var(--text2);text-transform:uppercase;letter-spacing:1px;margin-bottom:2px;font-weight:700;padding-left:4px}}
.filter-btn{{padding:.75rem 1rem;background:var(--glass);border:1px solid var(--border);border-radius:12px;color:var(--text2);cursor:pointer;font-size:.85rem;transition:all .2s;text-align:left;display:flex;align-items:center;justify-content:space-between;backdrop-filter:blur(10px)}}
.filter-btn:hover{{background:rgba(255,255,255,0.05);color:var(--text)}}
.filter-btn.active{{background:var(--accent);color:white;border-color:var(--accent);box-shadow:0 4px 15px rgba(125,95,255,0.3)}}
.filter-btn .count-badge{{background:rgba(0,0,0,0.2);padding:2px 8px;border-radius:10px;font-size:0.7rem}}
.container{{max-width:1400px;margin:0 auto}}
.uni-group{{margin-bottom:4rem}}
.uni-name{{font-size:1.6rem;font-weight:700;padding:1.2rem 0;border-bottom:1px solid var(--border);position:sticky;top:0;background:rgba(5,5,8,0.85);backdrop-filter:blur(20px);z-index:10;margin-bottom:1.5rem;display:flex;justify-content:space-between;align-items:center}}
.uni-header-main{{display:flex;align-items:center;gap:12px}}
.uni-name .count{{font-size:.85rem;color:var(--text2);font-weight:400}}
.uni-meta{{display:flex;gap:8px}}
.meta-tag{{font-size:0.7rem;padding:4px 10px;border-radius:6px;font-weight:600}}
.country-tag{{background:rgba(72,219,251,0.1);color:var(--blue);border:1px solid rgba(72,219,251,0.2)}}
.rank-tag{{background:rgba(255,159,67,0.1);color:var(--orange);border:1px solid rgba(255,159,67,0.2)}}
.cards-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(420px,1fr));gap:1.5rem}}
.card{{background:var(--card);border:1px solid var(--border);border-radius:20px;padding:1.75rem;transition:all .3s ease;display:flex;flex-direction:column;position:relative;overflow:hidden}}
.card::before{{content:'';position:absolute;top:0;left:0;width:4px;height:0;background:var(--accent);transition:height .3s}}
.card:hover{{transform:translateY(-5px);box-shadow:0 12px 40px rgba(0,0,0,0.4);border-color:rgba(125,95,255,0.3)}}
.card:hover::before{{height:100%}}
.card-header{{display:flex;justify-content:space-between;align-items:flex-start;gap:1rem;margin-bottom:0;cursor:pointer;user-select:none}}
.card:hover{{transform:translateY(-2px);box-shadow:0 8px 30px rgba(0,0,0,0.4);border-color:rgba(125,95,255,0.3)}}
.card:hover::before{{height:100%}}
.card-header .tags{{margin-bottom:0}}

/* Detail Drawer */
.drawer-overlay{{position:fixed;top:0;right:0;width:100%;height:100%;background:rgba(0,0,0,0.6);backdrop-filter:blur(4px);display:none;z-index:1000}}
.drawer-overlay.open{{display:block}}
.drawer-panel{{position:absolute;top:0;right:0;width:580px;max-width:100vw;height:100%;background:var(--surface);border-left:1px solid var(--border);padding:3rem 2.5rem;overflow-y:auto;animation:slideIn .3s ease}}
@keyframes slideIn{{from{{transform:translateX(100%)}}to{{transform:translateX(0)}}}}
.drawer-close{{position:absolute;top:1.5rem;right:1.5rem;background:none;border:none;color:var(--text2);font-size:1.8rem;cursor:pointer;width:40px;height:40px;border-radius:10px;display:flex;align-items:center;justify-content:center}}
.drawer-close:hover{{background:var(--glass);color:var(--text)}}
.drawer-panel h2{{font-size:1.6rem;font-weight:700;margin-bottom:.3rem}}
.drawer-panel .prof-title{{color:var(--text2);font-size:.85rem;margin-bottom:1rem}}
.drawer-panel .section{{margin-top:1.5rem;padding-top:1.5rem;border-top:1px solid var(--border)}}
.drawer-panel .section h4{{font-size:.7rem;color:var(--text2);margin-bottom:.8rem;text-transform:uppercase;letter-spacing:1.5px;font-weight:700}}

/* Interest Tag Filter */
.tag-filter{{cursor:pointer;transition:all .2s}}
.tag-filter:hover{{background:rgba(125,95,255,0.2);border-color:var(--accent);color:var(--text)}}
.tag-filter.active{{background:var(--accent);color:white;border-color:var(--accent)}}

/* Bookmark */
.bookmark-btn{{position:absolute;top:.8rem;left:.8rem;z-index:2;background:none;border:none;font-size:1.3rem;cursor:pointer;color:var(--text2);padding:.2rem;transition:all .2s}}
.bookmark-btn:hover,.bookmark-btn.bookmarked{{color:#f5d442;transform:scale(1.3)}}
.tag-input:focus{{outline:none;border-color:var(--accent)!important}}
.prof-name{{font-size:1.25rem;font-weight:700;letter-spacing:-0.5px}}
.prof-title{{color:var(--text2);font-size:.8rem;margin-top:2px}}
.badge{{padding:.4rem .8rem;border-radius:10px;font-size:.65rem;font-weight:700;white-space:nowrap;flex-shrink:0;text-transform:uppercase;letter-spacing:0.5px}}
.badge.high{{background:rgba(0,210,173,.12);color:var(--green);border:1px solid rgba(0,210,173,.2)}}
.badge.good{{background:rgba(255,159,67,.12);color:var(--orange);border:1px solid rgba(255,159,67,.2)}}
.badge.partial{{background:rgba(72,219,251,.12);color:var(--blue);border:1px solid rgba(72,219,251,.2)}}
.metrics{{display:flex;gap:.6rem;margin-bottom:1rem}}
.metric{{font-size:.7rem;color:var(--accent2);background:rgba(125,95,255,0.1);padding:.3rem .7rem;border-radius:8px;font-weight:600}}
.tags{{display:flex;flex-wrap:wrap;gap:.4rem;margin-bottom:1rem}}
.tag{{font-size:.65rem;padding:.3rem .6rem;background:rgba(255,255,255,0.05);color:var(--text2);border-radius:8px;border:1px solid var(--border)}}
.tag.matched{{background:rgba(0,210,173,.08);color:var(--green);border-color:rgba(0,210,173,.2)}}
.actions{{display:flex;gap:.6rem;flex-wrap:wrap;margin-bottom:1.2rem}}
.btn{{display:inline-flex;align-items:center;gap:.4rem;padding:.5rem .9rem;border-radius:10px;font-size:.75rem;text-decoration:none;transition:all .2s;font-weight:600}}
.email-btn{{background:var(--accent);color:white;box-shadow:0 4px 12px rgba(125,95,255,0.2)}}
.email-btn:hover{{transform:scale(1.02);box-shadow:0 6px 15px rgba(125,95,255,0.3)}}
.profile-btn{{background:rgba(255,255,255,0.05);color:var(--text);border:1px solid var(--border)}}
.profile-btn:hover{{background:rgba(255,255,255,0.1)}}
.scholar-btn{{background:rgba(0,210,173,0.1);color:var(--green);border:1px solid rgba(0,210,173,0.2)}}
.scholar-btn:hover{{background:rgba(0,210,173,0.2)}}
.no-email{{font-size:.75rem;color:var(--text2);font-style:italic;padding:.5rem 0}}
.section{{margin-top:1rem;padding-top:1rem;border-top:1px solid var(--border)}}
.section h4{{font-size:.65rem;color:var(--text2);margin-bottom:.6rem;text-transform:uppercase;letter-spacing:1.5px;font-weight:700}}
.pubs{{list-style:none;padding:0}}
.pubs li{{font-size:.75rem;padding:.5rem 0;border-bottom:1px solid rgba(255,255,255,0.03);color:var(--text2)}}
.pubs li:last-child{{border:none}}
.pubs li a{{color:var(--text);text-decoration:none;font-weight:500}}.pubs li a:hover{{color:var(--accent2);text-decoration:underline}}
.pubs .year{{color:var(--blue);font-weight:700;margin-right:4px}}
.pubs .cite{{color:var(--green);font-size:0.7rem;margin-left:4px}}
.bio{{font-size:.75rem;color:var(--text2);margin-top:.8rem;line-height:1.6;display:-webkit-box;-webkit-box-orient:vertical;overflow:hidden;text-overflow:ellipsis}}
.footer{{margin-top:auto;text-align:center;padding-top:2.5rem;color:var(--text2);font-size:.7rem;opacity:0.6}}
.hidden{{display:none!important}}
::-webkit-scrollbar{{width:8px}}
::-webkit-scrollbar-track{{background:transparent}}
::-webkit-scrollbar-thumb{{background:var(--border);border-radius:10px}}
::-webkit-scrollbar-thumb:hover{{background:rgba(255,255,255,0.15)}}
@media(max-width:900px){{body{{flex-direction:column;overflow:auto}}.sidebar{{width:100%;height:auto;overflow:visible;border-right:none;border-bottom:1px solid var(--border)}}.main-content{{height:auto;overflow:visible;padding:1.5rem}}.cards-grid{{grid-template-columns:1fr}}}}
</style>
<script>
const I18N = {{
  'app.title': {{ en: 'Global Geoscience Advisor Finder', zh: '全球地学导师搜索工具' }},
  'app.subtitle': {{ en: 'Target: 150+ Universities Worldwide', zh: '覆盖：全球150+所大学' }},
  'btn.start': {{ en: 'Start New Scan', zh: '开始新扫描' }},
  'btn.start.running': {{ en: 'Scanning in progress...', zh: '扫描进行中...' }},
  'btn.start.done': {{ en: 'Scan Complete (Click to restart)', zh: '扫描完成（点击重新开始）' }},
  'btn.config': {{ en: 'Configure Keywords', zh: '配置关键词' }},
  'status.idle': {{ en: 'Idle', zh: '空闲' }},
  'status.ready': {{ en: 'Ready to begin', zh: '准备开始' }},
  'stat.total': {{ en: 'Total Professors', zh: '教授总数' }},
  'stat.unis': {{ en: 'Universities', zh: '大学数量' }},
  'stat.email': {{ en: 'With Email', zh: '有邮箱' }},
  'filter.search': {{ en: 'Search name, interest, university...', zh: '搜索姓名、研究方向、大学...' }},
  'filter.match': {{ en: 'Match Level', zh: '匹配等级' }},
  'filter.all': {{ en: 'All Matches', zh: '全部匹配' }},
  'filter.high': {{ en: 'High Match', zh: '高度匹配' }},
  'filter.good': {{ en: 'Good Match', zh: '良好匹配' }},
  'filter.partial': {{ en: 'Partial Match', zh: '部分匹配' }},
  'filter.region': {{ en: 'Region', zh: '地区' }},
  'filter.worldwide': {{ en: 'Worldwide', zh: '全球' }},
  'filter.us': {{ en: 'United States', zh: '美国' }},
  'filter.australia': {{ en: 'Australia', zh: '澳大利亚' }},
  'filter.contact': {{ en: 'Contact', zh: '联系方式' }},
  'filter.has_email': {{ en: 'Has Email', zh: '有邮箱' }},
  'card.scholar': {{ en: 'Scholar', zh: '学术档案' }},
  'card.profile': {{ en: 'Profile', zh: '个人主页' }},
  'card.email': {{ en: 'Email', zh: '邮箱' }},
  'card.no_email': {{ en: 'Email not found', zh: '未找到邮箱' }},
  'card.matched_kw': {{ en: 'Matched Keywords', zh: '匹配关键词' }},
  'card.pubs': {{ en: 'Recent Publications', zh: '近期论文' }},
  'card.citations': {{ en: 'citations', zh: '引用' }},
  'card.h_index': {{ en: 'h-index', zh: 'h指数' }},
  'card.citations_total': {{ en: 'Citations', zh: '总引用' }},
  'modal.title': {{ en: 'Configure Keywords', zh: '配置关键词' }},
  'modal.loading': {{ en: 'Loading keywords...', zh: '加载关键词中...' }},
  'modal.fail': {{ en: 'Failed to load keywords.', zh: '加载关键词失败。' }},
  'modal.save': {{ en: 'Save Configuration', zh: '保存配置' }},
  'modal.cancel': {{ en: 'Cancel', zh: '取消' }},
  'modal.saving': {{ en: 'Saving...', zh: '保存中...' }},
  'modal.saved': {{ en: 'Configuration saved! Next scan will use new keywords.', zh: '配置已保存！下次扫描将使用新关键词。' }},
  'modal.save_fail': {{ en: 'Failed to save configuration.', zh: '保存配置失败。' }},
  'footer.generated': {{ en: 'Generated on', zh: '生成于' }},
}};

function __(key) {{
  const entry = I18N[key];
  if (!entry) return key;
  return entry[currentLang] || entry.en || key;
}}

let currentLang = 'en';

function initLanguage() {{
  const saved = localStorage.getItem('advisor-scout-lang');
  if (saved && (saved === 'en' || saved === 'zh')) {{
    currentLang = saved;
  }} else if (navigator.language.startsWith('zh')) {{
    currentLang = 'zh';
  }} else {{
    currentLang = 'en';
  }}
  applyLanguage();
  updateLangToggle();
}}

function toggleLanguage() {{
  currentLang = currentLang === 'en' ? 'zh' : 'en';
  localStorage.setItem('advisor-scout-lang', currentLang);
  applyLanguage();
  updateLangToggle();
}}

function applyLanguage() {{
  document.querySelectorAll('[data-i18n]').forEach(el => {{
    const key = el.dataset.i18n;
    const text = __(key);
    if (el.tagName === 'INPUT' && el.type === 'text') {{
      el.placeholder = text;
    }} else {{
      el.textContent = text;
    }}
  }});
  document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {{
    el.placeholder = __(el.dataset.i18nPlaceholder);
  }});
}}

function updateLangToggle() {{
  const btn = document.getElementById('lang-toggle');
  if (btn) {{
    btn.innerHTML = currentLang === 'en' ? '🌐 中文' : '🌐 English';
  }}
}}

document.addEventListener('DOMContentLoaded', initLanguage);
</script></head>
<body>
<div class="sidebar">
  <div class="hero">
    <h1 data-i18n="app.title">🎓 Global Geoscience Advisor Finder</h1>
    <p data-i18n="app.subtitle">Target: 150+ Universities Worldwide</p>
  </div>

  <!-- START BUTTON -->
  <div class="start-box">
    <button class="start-btn" id="start-btn" data-i18n="btn.start">
        🚀 Start New Scan
    </button>
  </div>

  <div class="config-box">
    <button class="config-btn" id="config-btn" data-i18n="btn.config">
        ⚙️ Configure Keywords
    </button>
  </div>

  <!-- LIVE PROGRESS SECTION -->
  <div class="live-status" id="live-status">
    <div class="status-header">
        <span class="status-title" id="status-phase" data-i18n="status.idle">Idle</span>
        <span class="status-percent" id="status-percent">0%</span>
    </div>
    <div class="progress-bar-bg">
        <div class="progress-bar-fill" id="status-bar"></div>
    </div>
    <span class="status-text" id="status-uni" data-i18n="status.ready">Ready to begin</span>
  </div>
  
  <div class="stats">
    <div class="stat wide"><div class="num" id="stat-total">{total}</div><div class="label" data-i18n="stat.total">Total Professors</div></div>
    <div class="stat"><div class="num" id="stat-unis">{unis}</div><div class="label" data-i18n="stat.unis">Universities</div></div>
    <div class="stat"><div class="num" id="stat-email">{with_email}</div><div class="label" data-i18n="stat.email">With Email</div></div>
  </div>

  <div class="controls">
    <div class="filter-group">
        <span class="filter-label">Search</span>
        <input type="text" class="search-box" id="search" data-i18n-placeholder="filter.search" placeholder="🔍 Search name, interest, university...">
    </div>

    <div class="filter-group">
        <span class="filter-label" data-i18n="filter.match">Match Level</span>
        <button class="filter-btn active" data-filter="all" data-i18n="filter.all">🌐 All Matches <span class="count-badge">{total}</span></button>
        <button class="filter-btn" data-filter="high" data-i18n="filter.high">🔥 High Match <span class="count-badge">{high}</span></button>
        <button class="filter-btn" data-filter="good" data-i18n="filter.good">⭐ Good Match <span class="count-badge">{good}</span></button>
    </div>

    <div class="filter-group">
        <span class="filter-label" data-i18n="filter.region">Country</span>
        <button class="filter-btn active" data-country="all">🌍 <span data-i18n="filter.worldwide">Worldwide</span> <span class="count-badge">{total}</span></button>
''' + "".join(f'        <button class="filter-btn" data-country="{k.lower().replace(" ", "-")}">{_country_flag(k)} {k} <span class="count-badge">{v}</span></button>\n' for k, v in sorted(countries.items(), key=lambda x: -x[1])) + f'''
    </div>

    <div class="filter-group">
        <span class="filter-label">📌 Bookmarks</span>
        <button class="filter-btn" data-filter="bookmarked" id="filter-bookmarked">⭐ Bookmarked <span class="count-badge" id="bm-count">0</span></button>
        <div class="tags" id="bm-tag-filters" style="margin-top:.5rem"></div>
    </div>
    
    <div class="filter-group">
        <span class="filter-label" data-i18n="filter.contact">Contact</span>
        <button class="filter-btn" data-filter="email" data-i18n="filter.has_email">📧 Has Email <span class="count-badge">{with_email}</span></button>
    </div>
  </div>

  <div style="text-align:center;padding:1rem 0;">
    <button id="lang-toggle" onclick="toggleLanguage()" style="background:var(--glass);border:1px solid var(--border);border-radius:12px;color:var(--text);padding:0.6rem 1.2rem;cursor:pointer;font-size:0.85rem;font-weight:600;transition:all .2s;width:100%"
        onmouseover="this.style.background='rgba(255,255,255,0.08)'" onmouseout="this.style.background='var(--glass)'">
        🌐 中文
    </button>
  </div>

  <div class="footer"><span data-i18n="footer.generated">Generated on</span><br>{datetime.now().strftime("%b %d, %Y at %I:%M %p")}</div>
</div>

<div class="main-content">
  <div class="container" id="report-container">
    {professor_cards}
  </div>
</div>

<!-- CONFIG MODAL -->
<div class="modal-overlay" id="config-modal">
  <div class="modal-content">
    <div class="modal-header">
      <h2 data-i18n="modal.title">Configure Keywords</h2>
      <button class="close-modal" id="close-modal">&times;</button>
    </div>
    <div id="keywords-container">
        <!-- Dynamic keyword inputs will go here -->
    </div>
    <div class="modal-footer">
      <button class="btn-cancel" id="btn-cancel" data-i18n="modal.cancel">Cancel</button>
      <button class="btn-save" id="btn-save" data-i18n="modal.save">Save Configuration</button>
    </div>
  </div>
</div>

<script>
const search=document.getElementById('search');
const cards=document.querySelectorAll('.card');
const filters=document.querySelectorAll('.filter-btn[data-filter]');
const countryFilters=document.querySelectorAll('.filter-btn[data-country]');
const startBtn = document.getElementById('start-btn');
let activeFilter='all', activeCountry='all', activeBmTag='';

// ── Bookmarks (localStorage) ──
function loadBookmarks(){{
    try{{ return JSON.parse(localStorage.getItem('advisor-bookmarks')||'{{}}'); }}catch(e){{ return {{}}; }}
}}
function saveBookmarks(data){{ localStorage.setItem('advisor-bookmarks',JSON.stringify(data)); }}

function toggleBookmark(id){{
    const bm = loadBookmarks();
    const btn = document.getElementById('bm-'+id);
    if(!btn) return;
    const card = document.querySelector('.card[data-id=\"'+id+'\"]');
    if(bm[id]){{
        delete bm[id]; btn.classList.remove('bookmarked'); btn.textContent='☆';
    }}else{{
        bm[id]={{name:card?card.dataset.name:'', uni:card?card.dataset.uni:'', tags:[]}};
        btn.classList.add('bookmarked'); btn.textContent='★';
    }}
    saveBookmarks(bm); updateBmUI(); applyFilters();
}}

function addBookmarkTag(profId,input){{
    const tag = input.value.trim(); if(!tag) return;
    const bm = loadBookmarks();
    const entry = bm[profId]||{{name:'',uni:'',tags:[]}};
    if(!entry.tags.includes(tag)){{ entry.tags.push(tag); }}
    bm[profId]=entry; saveBookmarks(bm);
    input.value=''; renderBmTags(profId); updateBmUI(); applyFilters();
}}

function removeBookmarkTag(profId,tag){{
    const bm = loadBookmarks();
    if(bm[profId]){{ bm[profId].tags = bm[profId].tags.filter(t=>t!==tag); saveBookmarks(bm); }}
    renderBmTags(profId); updateBmUI();
}}

function renderBmTags(profId){{
    const container = document.getElementById('bm-tags-'+profId);
    if(!container) return;
    const bm = loadBookmarks();
    const tags = (bm[profId]&&bm[profId].tags)||[];
    container.innerHTML = tags.map(t=>'<span class="tag matched" style="cursor:pointer" onclick="removeBookmarkTag(\''+profId+'\',\''+t+'\')">'+t+' ×</span>').join('');
}}

function updateBmUI(){{
    const bm = loadBookmarks();
    // Update star buttons
    document.querySelectorAll('.bookmark-btn').forEach(btn=>{{
        const id = btn.id.replace('bm-','');
        if(bm[id]){{ btn.classList.add('bookmarked'); btn.textContent='★'; }}
        else{{ btn.classList.remove('bookmarked'); btn.textContent='☆'; }}
    }});
    // Update count
    const count = Object.keys(bm).length;
    document.getElementById('bm-count').innerText = count;
    // Build tag filter buttons from all bookmark tags
    const allTags = new Set();
    Object.values(bm).forEach(e=>e.tags.forEach(t=>allTags.add(t)));
    const container = document.getElementById('bm-tag-filters');
    container.innerHTML = Array.from(allTags).map(t=>
        '<span class="tag tag-filter" data-bmtag="'+t+'" onclick="toggleBmTag(this,\''+t+'\')">🏷️ '+t+'</span>'
    ).join('');
}}

function toggleBmTag(el,tag){{
    document.querySelectorAll('[data-bmtag]').forEach(t=>t.classList.remove('active'));
    if(activeBmTag===tag){{ activeBmTag=''; }}else{{ el.classList.add('active'); activeBmTag=tag; }}
    applyFilters();
}}

// ── Drawer ──
function openDrawer(id){{
    var d=document.getElementById('drawer-'+id);
    if(d){{ d.classList.add('open'); renderBmTags(id); }}
}}
function closeDrawer(id){{
    var d=document.getElementById('drawer-'+id);
    if(d) d.classList.remove('open');
}}

// ── Filters ──
function applyFilters(){{
    const q=search.value.toLowerCase(); const bm=loadBookmarks();
    cards.forEach(c=>{{
        let show=true;
        const name=c.dataset.name||'', uni=c.dataset.uni||'';
        const score=parseFloat(c.dataset.score)||0, country=c.dataset.country||'';
        if(q && !name.includes(q) && !uni.includes(q)) show=false;
        if(activeFilter==='high' && score<3) show=false;
        if(activeFilter==='good' && score<2) show=false;
        if(activeFilter==='email' && !c.querySelector('.email-btn')) show=false;
        if(activeFilter==='bookmarked' && !bm[c.dataset.id]) show=false;
        if(activeCountry!=='all' && country!==activeCountry) show=false;
        if(activeBmTag){{
            const entry=bm[c.dataset.id];
            if(!entry||!entry.tags.includes(activeBmTag)) show=false;
        }}
        c.classList.toggle('hidden',!show);
    }});
    var visible=document.querySelectorAll('.card:not(.hidden)').length;
    document.getElementById('stat-total').innerText=visible;
    document.getElementById('stat-unis').innerText=new Set(Array.from(document.querySelectorAll('.card:not(.hidden)')).map(c=>c.dataset.uni)).size;
    document.getElementById('stat-email').innerText=document.querySelectorAll('.card:not(.hidden) .email-btn').length;
}}

search.addEventListener('input',applyFilters);
filters.forEach(b=>b.addEventListener('click',()=>{{
    filters.forEach(f=>f.classList.remove('active'));
    b.classList.add('active'); activeFilter=b.dataset.filter; applyFilters();
}}));
countryFilters.forEach(b=>b.addEventListener('click',()=>{{
    countryFilters.forEach(f=>f.classList.remove('active'));
    b.classList.add('active'); activeCountry=b.dataset.country; applyFilters();
}}));

// Init
updateBmUI();

// START BUTTON HANDLER
startBtn.addEventListener('click', async () => {{
    if (startBtn.classList.contains('running')) return;
    
    if (confirm((currentLang === 'zh' ? '确认开始全新扫描所有大学？这可能需要10-20分钟。' : 'Start a fresh scan of all universities? This may take 10-20 minutes.'))) {{
        startBtn.innerText = '⚙️ ' + __('btn.start.running');
        startBtn.classList.add('running');
        try {{
            const response = await fetch('/start');
            const data = await response.json();
            console.log('Scraper started', data);
        }} catch (e) {{
            alert('Failed to start scraper. Make sure app.py is running.');
            startBtn.innerText = '🚀 ' + __('btn.start');
            startBtn.classList.remove('running');
        }}
    }}
}});

// CONFIG MODAL HANDLER
const configBtn = document.getElementById('config-btn');
const configModal = document.getElementById('config-modal');
const closeModal = document.getElementById('close-modal');
const btnCancel = document.getElementById('btn-cancel');
const btnSave = document.getElementById('btn-save');
const kwContainer = document.getElementById('keywords-container');

if(!configBtn||!configModal){{ console.error('Config modal elements missing'); }}
configBtn && configBtn.addEventListener('click', async () => {{
    kwContainer.innerHTML = '<p style="text-align:center;padding:2rem;"><span data-i18n="modal.loading">Loading keywords...</span></p>';
    configModal.style.display = 'flex';
    
    try {{
        const response = await fetch('/get_keywords');
        const keywords = await response.json();
        
        kwContainer.innerHTML = '';
        Object.entries(keywords).forEach(([category, list]) => {{
            const group = document.createElement('div');
            group.className = 'kw-group';
            group.innerHTML = `
                <label class="kw-label">${{category.replace(/_/g, ' ')}}</label>
                <textarea class="kw-input" data-category="${{category}}">${{list.join(', ')}}</textarea>
            `;
            kwContainer.appendChild(group);
        }});
    }} catch (e) {{
        kwContainer.innerHTML = '<p style="color:var(--red);text-align:center;padding:2rem;"><span data-i18n="modal.fail">Failed to load keywords.</span></p>';
    }}
}});

const hideModal = () => {{ if(configModal) configModal.style.display = 'none'; }};
if(closeModal) closeModal.addEventListener('click', hideModal);
if(btnCancel) btnCancel.addEventListener('click', hideModal);

btnSave.addEventListener('click', async () => {{
    const textareas = kwContainer.querySelectorAll('textarea');
    const newKeywords = {{}};
    
    textareas.forEach(ta => {{
        const category = ta.dataset.category;
        const list = ta.value.split(',').map(s => s.trim()).filter(s => s.length > 0);
        newKeywords[category] = list;
    }});
    
    btnSave.innerText = '⌛ ' + __('modal.saving');
    btnSave.disabled = true;
    
    try {{
        const response = await fetch('/save_keywords', {{
            method: 'POST',
            headers: {{ 'Content-Type': 'application/json' }},
            body: JSON.stringify(newKeywords)
        }});
        if (response.ok) {{
            hideModal();
            alert(__('modal.saved'));
        }} else {{
            alert(__('modal.save_fail'));
        }}
    }} catch (e) {{
        alert('Error saving configuration.');
    }} finally {{
        btnSave.innerText = __('modal.save');
        btnSave.disabled = false;
    }}
}});

// LIVE PROGRESS POLLING
async function pollStatus() {{
    try {{
        // Use relative path for status.json since it's served by the same server
        const response = await fetch('status.json?t=' + new Date().getTime());
        if (response.ok) {{
            const status = await response.json();
            
            document.getElementById('status-phase').innerText = status.phase;
            document.getElementById('status-uni').innerText = status.current_university || 'Idle';
            
            const total = status.total_urls || 1;
            const current = status.current_index || 0;
            const percent = Math.round((current / total) * 100);
            
            document.getElementById('status-percent').innerText = percent + '%';
            document.getElementById('status-bar').style.width = percent + '%';
            document.getElementById('stat-total').innerText = status.professors_total;
            
            if (status.phase !== 'Completed' && status.phase !== 'Idle') {{
                startBtn.innerText = '⚙️ ' + __('btn.start.running');
                startBtn.classList.add('running');
            }} else if (status.phase === 'Completed') {{
                startBtn.innerText = '✅ ' + __('btn.start.done');
                startBtn.classList.remove('running');
                // Optional: reload after some time
                // location.reload();
            }}
        }}
    }} catch (e) {{
        console.log('Status poll failed', e);
    }}
}}

// Poll every 3 seconds
setInterval(pollStatus, 3000);
pollStatus();

</script></body></html>'''

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    logger.info(f"HTML report generated: {output_path}")


def _country_flag(country: str) -> str:
    flags = {
        "America": "🇺🇸", "UK": "🇬🇧", "Australia": "🇦🇺", "Canada": "🇨🇦",
        "New Zealand": "🇳🇿", "Switzerland": "🇨🇭", "Netherlands": "🇳🇱",
        "Germany": "🇩🇪", "Norway": "🇳🇴", "France": "🇫🇷",
        "Italy": "🇮🇹", "Denmark": "🇩🇰", "Sweden": "🇸🇪",
        "Finland": "🇫🇮", "Iceland": "🇮🇸", "Austria": "🇦🇹",
        "Belgium": "🇧🇪", "Spain": "🇪🇸", "Ireland": "🇮🇪",
        "Singapore": "🇸🇬", "Hong Kong": "🇭🇰", "Japan": "🇯🇵",
        "China": "🇨🇳", "South Korea": "🇰🇷", "Taiwan": "🇹🇼",
    }
    return flags.get(country, "🌍")

def _esc(text: str) -> str:
    """Escape HTML special characters."""
    if not text:
        return ""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def _get_country(university: str) -> str:
    """Determine country by looking up universities.json."""
    info = _get_uni_info(university)
    return info.get("country", "US")

def _get_region(university: str) -> str:
    """Map country to display region for filtering."""
    country = _get_country(university)
    region_map = {
        "US": "Americas", "Canada": "Americas", "Mexico": "Americas",
        "UK": "Europe", "Switzerland": "Europe", "Netherlands": "Europe",
        "Germany": "Europe", "Norway": "Europe", "France": "Europe",
        "Italy": "Europe", "Denmark": "Europe", "Sweden": "Europe",
        "Finland": "Europe", "Iceland": "Europe", "Austria": "Europe",
        "Belgium": "Europe", "Spain": "Europe", "Ireland": "Europe",
        "Australia": "Oceania", "New Zealand": "Oceania",
        "Singapore": "Asia", "Hong Kong": "Asia",
        "Japan": "Asia", "China": "Asia", "South Korea": "Asia", "Taiwan": "Asia",
    }
    return region_map.get(country, "Other")
