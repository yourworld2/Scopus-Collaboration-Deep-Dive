# Changelog

All notable changes to this project are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
This project adheres to [Semantic Versioning](https://semver.org/).

## [1.0.0] - 2026-09-24

### Added
- **Author-count filter** — automatic detection of consortium mega-papers (ATLAS/CMS/GBD)
- **Region classifier v3** — 50+ explicit US/international university names
- **Bilingual output** — EN + 中文 labels in single XLSX column
- **5-sheet base pipeline** covering 10 default topics:
  1. Overview stats
  2. Top 20 partner institutions
  3. Top 10 research fields
  4. Top 10 researchers
  5. YoY trends, topic evolution, HHI concentration, region breakdown, 3 archetypes, top journals + Funding Horizon
- **Extended 7-sheet pipeline** (on request):
  6. Deep Dive — ASJC categories (5 buckets), AI cluster, H-index, multi-region profile
  7. Signatures & Funding — Top 1%/5%/10%, multi-sector, OA, document types
- **HTML dashboard** with EN/中文 toggle
- **Public deployment** support via `website_deploy`
- **Offline package** — self-contained HTML with embedded data + XLSX download
- **Live formulas** throughout (no hardcoded ratios)
- **Multi-platform compatibility** — works on Linux/macOS/WSL

### Validated on
- **Yale × Chinese Universities (2022-2026)** — 2,664 papers, 7 sheets, 318 formulas, 31 KB
- **Stanford × Shanghai Jiao Tong University (2022-2026, filtered ≤50 authors)** — 456 papers, 7 sheets, 56 formulas, 27 KB, bilingual

### Inspiration
- Built for the `minimax-xlsx` skill's `xlsx_pack.py` workflow
- Uses LibreOffice headless conversion to fix non-sequential rIds

## [0.9.0] - 2026-09-20 (pre-release)

### Added
- Initial SKILL.md with 9-step procedure
- 11-code-snippet analysis-cookbook
- 8 templated insight patterns
- 3 worked examples

[1.0.0]: https://github.com/minimax/scopus-collaboration-deep-dive/releases/tag/v1.0.0
[0.9.0]: https://github.com/minimax/scopus-collaboration-deep-dive/releases/tag/v0.9.0