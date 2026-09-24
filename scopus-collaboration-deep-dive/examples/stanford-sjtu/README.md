# Stanford × Shanghai Jiao Tong University (2022-2026)

**Real-world validation case** with author-count filtering and bilingual output.

## Dataset

- **Source**: Scopus CSV export, "Publications at Stanford University 2022-2026"
- **Target**: Shanghai Jiao Tong University
- **Filter**: ≤50 authors applied (61% papers removed — dominated by ATLAS/CMS/GBD)
- **Total papers**: 1,174 (raw) → 456 (filtered to bilateral Stanford-SJTU co-authors)
- **Year range**: 2022-2026

## Why the filter matters

| Metric | Before | After | Insight |
|---|---:|---:|---|
| Papers | 1,174 | 456 | 61% removed |
| Avg FWCI | 8.85 | 2.79 | Real research focus |
| Max FWCI | 927 | 67 | Outliers were physics |
| Top field | Physics | CS / AI | Real research profile |

**Without the filter**, Stanford-SJTU looks like a physics consortium.
**With the filter**, you see the real bilateral AI/CS/health collaboration.

## Key findings

| Metric | Value |
|---|---:|
| Total papers | 456 |
| Total citations | 8,989 |
| Avg FWCI | 2.79 |
| Distinct institutions | 187 |
| Distinct ASJC fields | 207 |
| Top journal | Nature Communications (17) |
| Top field | Computer Science Applications (43) |
| Open Access | 215 (47.1%) |
| Multi-sector papers | 409 (89.7%) |

## Region distribution (after classifier v3)

| Region | Papers | Share |
|---|---:|---:|
| Stanford (source) | 455 | 13.6% |
| Shanghai Jiao Tong (target) | 410 | 12.3% |
| Mainland China | 391 | 11.7% |
| US (other top) | 387 | 11.6% |
| Hong Kong / Macau / Taiwan | 60 | 1.8% |
| US (Federal/DOE) | 60 | 1.8% |
| Germany / Switzerland | 56 | 1.7% |
| UK | 50 | 1.5% |
| Singapore | 47 | 1.4% |
| Other International | 1,308 | 39.3% |

## AI / ML cluster

- **Detection**: Co-authors whose surnames match top CS/AI Chinese names (Wang/Li/Liu/Zhang/Ma/Zhao/Chen/Tang/Sun/Cai/Hu)
- **123 papers match** (27% of dataset)
- **Top researchers**: Zhang Y. (32), Li Y. (30), Wang Y. (28)
- **Yearly trend**: 22 (2022) → 26 (2025), FWCI peaked at 3.10 (2024)

## Output files

- `stanford_sjtu_filtered_analysis.xlsx` (27 KB, 7 sheets, 56 formulas, bilingual EN+中文)
- `index.html` (110 KB, self-contained, bilingual with toggle)
- `stanford_sjtu_offline_bundle.zip` (80 KB, full package)
- Deployed URLs:
  - Dashboard: https://d2qor2at6wdha.space.mcode.cn
  - Offline: https://tf10itfi1x347.space.mcode.cn

## Bilingual features

- All 60+ labels in `English | 中文` format
- Region names translated (`中国大陆（其他）`, `斯坦福（源）`, etc.)
- HTML with toggle button (default: 中文 visible)
- Top 1% papers highlighted in both languages
- Quality Score formula explained in both languages

## Lessons learned

1. **Always check `should_apply_filter()`** — physics consortium papers silently inflate metrics
2. **Region classifier v3 (full names)** is critical — `MIT` vs `Massachusetts Institute of Technology` produce very different results
3. **Bilingual output** doubles the work but vastly improves usability for international teams
4. **Multi-US profile** (43.9% papers include Stanford + SJTU + ≥1 other US university) is a key insight for bilateral analysis
5. **AI cluster detection** by Chinese surname pattern reveals the AI/ML collaboration depth

## How to reproduce

```bash
# Get the Scopus CSV from your account, place at:
# examples/stanford-sjtu/sample-input.csv

python scripts/build_xlsx.py \
    --csv examples/stanford-sjtu/sample-input.csv \
    --source "Stanford" \
    --target "Shanghai Jiao Tong" \
    --output /tmp/stanford_output
```