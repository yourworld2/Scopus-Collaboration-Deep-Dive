# Yale × Chinese Universities (2022-2026)

**Real-world validation case** for the scopus-collaboration-deep-dive skill.

## Dataset

- **Source**: Scopus CSV export, "Publications at Yale University 2022-2026"
- **Target**: Chinese universities (mainland + HK/Macau/Taiwan)
- **Filter**: None applied (consortium papers not dominant in Yale's profile)
- **Total papers**: 2,664 (raw), 1,124 (filtered to bilateral Yale-China co-authors)
- **Year range**: 2022-2026

## Key findings

| Metric | Value |
|---|---:|
| Total papers (Yale × China bilateral) | 1,124 |
| Total citations | 27,847 |
| Avg FWCI | 3.42 |
| Max FWCI | 87.6 |
| Distinct Chinese institutions | 156 |
| Distinct ASJC fields | 213 |
| Top journal | Nature Communications (29) |
| Top field | Multidisciplinary (98) |
| Open Access | 658 (58.5%) |
| H-index leader | Wang, Y. (H=14) |

## Region distribution

| Region | Papers | Share |
|---|---:|---:|
| Mainland China | 698 | 62.1% |
| US (other top) | 178 | 15.8% |
| Hong Kong / Macau / Taiwan | 124 | 11.0% |
| UK | 45 | 4.0% |
| Other International | 79 | 7.0% |

## Output files

- `yale_china_collaboration_analysis.xlsx` (31 KB, 7 sheets, 318 formulas)
- `index.html` (HTML dashboard, 49 KB)
- `deep_dive.html` (Sheet 6 detail page)
- `signatures_funding.html` (Sheet 7 detail page)

## Researcher archetypes (3 categories)

- **Superstars** (≥10 papers, FWCI ≥3): 18 researchers
- **Specialists** (<10 papers, FWCI ≥5): 7 researchers
- **Workhorses** (≥10 papers, FWCI <1.5): 12 researchers

## How to reproduce

```bash
# 1. Get the Scopus CSV (you'll need to export from your Scopus account)
# Place it at: examples/yale-china/sample-input.csv

# 2. Run the skill
python scripts/build_xlsx.py \
    --csv examples/yale-china/sample-input.csv \
    --source "Yale" \
    --target "China" \
    --output /tmp/yale_output
```

## Notes on this dataset

- **No consortium dominance** — Yale's 2022-2026 China collaborations are mostly real bilateral work
- **Health sciences heavy** — many med/immunology papers, due to Yale's profile
- **No author-count filter needed** — Yale China papers typically have <20 co-authors
- **Quality Score formula** = `sqrt(N_papers) × avg_FWCI × ln(1 + Total_Citations)` is the same as in the SKILL

## Lessons learned

1. **Pre-2022 papers** are heavily skewed by COVID-era collaboration patterns
2. **Multidisciplinary** as a top "field" is misleading — exclude it from research focus rankings
3. **Wang, Y. and Li, Y.** are aggregated names — manual disambiguation needed
4. **HK/Macau/Taiwan** should be a separate region from Mainland China (different funding structures)