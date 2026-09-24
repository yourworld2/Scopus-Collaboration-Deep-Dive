---
name: scopus-collaboration-deep-dive
version: 1.0.0
description: Analyze a Scopus CSV export of one university's co-authorship papers with a target region and produce a multi-sheet XLSX with live formulas + a bilingual HTML dashboard. Use when the user uploads a Scopus CSV/XLSX and asks to "analyze collaborations", "compare partner universities", "identify research clusters", "rank researchers", "trend analysis", "deep dive", or wants a bibliometric partnership report. Do NOT use for: single-paper summarization, full Scopus search/exports, journal-impact-factor queries, or general XLSX building.
github_url: https://github.com/minimax/scopus-collaboration-deep-dive
license: MIT
authors:
  - name: Mavis Agent Team
    email: support@mavis.ai
keywords:
  - bibliometric
  - scopus
  - collaboration
  - h-index
  - FWCI
  - ASJC
  - XLSX
  - bilingual
  - research-analytics
---

# scopus-collaboration-deep-dive

> A skill that turns a Scopus CSV export into a 5-7 sheet XLSX with live formulas + bilingual HTML dashboard.

## 🎯 When to use

User uploads a Scopus CSV/XLSX export and asks any of:
- "Analyze collaborations" / "compare partner universities"
- "Identify research clusters" / "rank researchers"
- "Trend analysis" / "deep dive" / "detailed report"
- "Bilateral cooperation" / "who are they working with"

**Auto-trigger** for any Scopus CSV/XLSX upload (don't ask first — just run the base pipeline).

**Ask first** before:
- Public deployment to `space.mcode.cn`
- Deep-dive Sheet 6/7 (Clusters/H-index/Multi-ASF/Signatures & Funding)

## 🚦 Decision matrix

| Trigger | Action |
|---|---|
| Scopus CSV/XLSX uploaded | Auto-run 5-sheet base pipeline |
| User says "deep dive" / "all topics" | Add Sheets 6 (Deep Dive) + 7 (Signatures & Funding) |
| User says "publish" / "deploy" | Ask confirmation, then `website_deploy` |
| User says "bilingual" / "中文" | Add bilingual EN+中文 labels |
| User says "offline" / "no internet" | Generate self-contained HTML package |

## 📋 The 10-topic base pipeline

Default 5-sheet XLSX covers these 10 topics:

1. **Overview** — totals, year window, top journal
2. **Top 20 Partner Institutions** — with live share formulas
3. **Top 10 Research Fields** — FWCI averages
4. **Top 10 Researchers** — primary institution + core field enrichment
5. **Trends & Patterns** — YoY trends, topic evolution, HHI concentration, region breakdown, 3 archetypes, top journals + Funding Horizon proxies

Extended 7-sheet adds:
6. **Deep Dive** — ASJC major categories (5 buckets), AI cluster, H-index, multi-region profile
7. **Signatures & Funding** — Top 1%/5%/10%, multi-sector, OA, document types

## 🚨 Critical: Author-count filter

> **Always check whether the dataset is dominated by consortium papers before processing.**

If >30% of papers have >50 authors, the dataset is dominated by mega-author consortium papers (ATLAS/CMS/LHCb physics, GBD medical cohorts). These inflate all metrics and obscure real bilateral collaboration patterns.

**Apply filter:**
```python
from filters import apply_author_filter, should_apply_filter

if should_apply_filter(df, threshold_pct=30.0):
    df_filtered, _ = apply_author_filter(df, max_authors=50)
```

**Real impact on Stanford × SJTU (2022-2026):**
- 1,174 papers → 456 papers (61% removed)
- Avg FWCI: 8.85 → 2.79 (still high but no longer dominated by ATLAS/CMS)
- Max FWCI: 927 → 67 (real outliers surface)

## 🌍 Region classifier v3

Maps each institution name to one of 14 categories:

- Stanford (source)
- Shanghai Jiao Tong (target) — adapt to your target
- Mainland China
- Hong Kong / Macau / Taiwan
- US (Federal/DOE)
- US (National Labs)
- US (other top) — 50+ top US universities
- Germany / Switzerland
- UK
- Singapore
- Japan
- Korea
- Europe (physics labs)
- Other International

**Why explicit full-name matching:** Scopus writes institution names in varied forms (e.g., "Massachusetts Institute of Technology" vs "MIT"). v3 uses full-name patterns for 50+ US/international universities.

## 🌐 Bilingual output

**HTML**: `body.className` toggle pattern with two divs:
```html
<div class="lang-zh">中文内容</div>
<div class="lang-en">English content</div>
```
```css
.lang-en { display: none; }
body.show-en .lang-zh { display: none; }
body.show-en .lang-en { display: block; }
```

**XLSX**: Single column with `English | 中文` labels:
```
Total Publications | 总发表数
```

**Region names**: Translate each region name separately (`scripts/bilingual.py:REGION_TRANSLATIONS`).

## 🛠️ Tech stack

- Python 3.10+
- pandas — CSV parsing & analysis
- openpyxl + custom XML — XLSX construction
- LibreOffice headless — post-process (fixes non-sequential rIds)
- Standard library — XML, json

## ⚙️ Implementation pattern

For full production implementation see SKILL.md and the minimax-xlsx skill. The standalone scripts in `scripts/` provide working reference implementations:

```bash
python scripts/build_xlsx.py --csv path/to/scopus.csv \
    --source "Yale" --target "China" --output ./output
```

For full XLSX + HTML, use the production workflow:

1. Read CSV with `pd.read_csv(skiprows=18)` (or 19/20/21)
2. Apply `apply_author_filter(df, max_authors=50)` if >30% are consortium
3. Build paper cache (list of dicts)
4. Compute 10 base topics + (optional) 4 deep-dive topics
5. Build XLSX XML manually (formula-by-formula) using minimax-xlsx pattern
6. `xlsx_pack.py` to package
7. LibreOffice convert for final XLSX
8. Build HTML dashboard with bilingual toggle
9. Optional: `website_deploy` for public URL

## 📊 Insight patterns

8 reusable patterns (each producing 1+ table or chart):

1. **Top 20 partner institutions** with concentration (HHI)
2. **YoY trends** with year-over-year growth
3. **Topic evolution** by year
4. **Region breakdown** with international collaboration profile
5. **Researcher archetypes** (Superstar/Specialist/Workhorse)
6. **Top 20 high-impact journals**
8. **Funding Horizon proxies** (Top 1%/5%/10% papers, OA, multi-sector)
9. **Multi-region partnership** profile (200 papers = bilateral + US)
10. **AI cluster detection** by Chinese surname pattern
11. **Consortium signature** (FWCI >100 flag for physics papers)

## 📚 Reference documentation

- `references/analysis-cookbook.md` — 16 reusable code snippets
- `docs/architecture.md` — internal architecture
- `docs/bilingual.md` — adding bilingual to new regions
- `docs/deployment.md` — public deployment guide
- Examples: `examples/yale-china/`, `examples/stanford-sjtu/`

## ✅ Validation

Self-validation patterns:
- Open XLSX in LibreOffice — verify all formulas calculate
- Open HTML in browser — verify both languages toggle
- Check FWCI distribution — verify not skewed by single mega-paper
- Verify `should_apply_filter()` triggers correctly on ATLAS/CMS datasets

## 📝 License

MIT — see [LICENSE](LICENSE).

## 👤 Author

Mavis Agent team, Sep 2026. Inspired by real-world bibliometric consulting work.