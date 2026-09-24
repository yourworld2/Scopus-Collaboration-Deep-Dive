# Scopus Collaboration Deep Dive

> Analyze a Scopus CSV export of one university's co-authorship papers with a target region and produce a multi-sheet XLSX with live formulas + a bilingual HTML dashboard.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Mavis Skill](https://img.shields.io/badge/Mavis-skill-blueviolet)](SKILL.md)
[![Examples](https://img.shields.io/badge/examples-2-success)](#examples)

## ✨ What it does

Turn a Scopus export like `yale_china_2022_2026.csv` into:

- **5-sheet XLSX** (default) or **7-sheet XLSX** (extended) with **live formulas** — no hardcoded ratios
- **Bilingual HTML dashboard** (English + 中文) with toggle button
- Optional **public deployment** to `space.mcode.cn` URLs

All in ~2 minutes, no manual data wrangling.

## 🚀 Quick start

### As a Mavis skill

The skill auto-loads for relevant tasks. Just describe what you want:

```
"分析 Yale × 中国高校 2022-2026 合作情况"
"Analyze Stanford × Shanghai Jiao Tong co-authorship data"
```

### Standalone Python usage

```bash
# Install
pip install -r requirements.txt

# Run on a Scopus CSV
python scripts/build_xlsx.py \
    --csv path/to/scopus_export.csv \
           --source "Yale" \
           --target "China" \
           --output ./output
```

The script auto-detects header offset, filters consortium papers (>50 authors), classifies regions, and writes the XLSX + JSON intermediates + HTML dashboard.

## 📊 What you get

### XLSX structure (default base = 5 sheets)

| Sheet | Content |
|---|---|
| Overview | Total stats, year window, top journal |
| Top 20 Partner Institutions | With live share formulas |
| Top 10 Research Fields | With FWCI averages |
| Top 10 Researchers | Primary institution + core field enrichment |
| Trends & Patterns | YoY trends, topic evolution, HHI concentration, region breakdown, 3 archetypes, top journals + Funding Horizon proxies |

### Extended (7 sheets, on request)

| Sheet | Content |
|---|---|
| Deep Dive | ASJC major categories (5 buckets), AI cluster detection, H-index, multi-region partnership profile |
| Signatures & Funding | Top 1%/5%/10% papers, multi-sector collaboration, OA status, document types |

### HTML dashboard

- Bilingual EN/中文 toggle
- Self-contained (no external CDN/fonts)
- Embedded data option (offline-ready, single file)
- Includes XLSX download button
- Deployable to public URL

## 📋 Features

- **Author-count filter** — automatically detects & filters ATLAS/CMS/GBD mega-cohorts
- **Region classifier v3** — handles 50+ US/international university names explicitly
- **Bilingual labels** — single XLSX column with `English | 中文` format
- **Live formulas** — all percentages are computed by Excel, not pre-baked
- **Production-tested** — used in 2 real-world cases (Yale × China, Stanford × SJTU)

## 📦 Examples

- [examples/yale-china/](examples/yale-china/) — 2,664 papers, 7 sheets, 318 formulas
- [examples/stanford-sjtu/](examples/stanford-sjtu/) — 456 papers (after filter), 7 sheets, 56 formulas, bilingual EN+中文

## 🛠️ Tech stack

- Python 3.10+
- pandas — CSV parsing & analysis
- openpyxl + custom XML — XLSX construction
- LibreOffice headless — post-process XLSX (resolves non-sequential rIds)
- Standard library — XML manipulation

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the workflow. Most useful contributions:

- New region classifier rules for other countries
- New cluster patterns (life sciences, physics, etc.)
- New pattern templates (citation lag, topic shift, etc.)
- Translation corrections in bilingual labels

## 📝 License

MIT — see [LICENSE](LICENSE).

## 📚 Documentation

- [SKILL.md](SKILL.md) — main skill specification (for Mavis AI consumption)
- [docs/architecture.md](docs/architecture.md) — how it works internally
- [docs/bilingual.md](docs/bilingual.md) — adding bilingual output to new regions
- [docs/deployment.md](docs/deployment.md) — how to deploy publicly
- [references/analysis-cookbook.md](references/analysis-cookbook.md) — 16 reusable code snippets
- [CHANGELOG.md](CHANGELOG.md) — version history

## 👤 Author

Built by **Mavis** (Mavis Agent team), Sep 2026.
Validated on Yale × Chinese Universities (2,664 papers) and Stanford × SJTU (456 papers after filter).

## 📊 Stats

- 5-sheet XLSX: ~10 seconds
- 7-sheet XLSX + bilingual HTML: ~2 minutes
- 100% formula coverage on derived metrics (no hardcoded ratios)
- 0 formula errors on all validation runs