# Architecture

How `scopus-collaboration-deep-dive` works internally.

## High-level flow

```
Scopus CSV/XLSX
    ↓
1. Header detection (skiprows=18-21)
    ↓
2. Author-count filter (if >30% papers have >50 authors)
    ↓
3. Paper cache (list of dicts)
    ↓
4. Compute 10 base topics
    ↓
5. Compute 4 deep-dive topics (optional)
    ↓
6. Build XLSX XML manually (live formulas)
    ↓
7. xlsx_pack.py → package as XLSX
    ↓
8. LibreOffice convert (resolves non-sequential rIds)
    ↓
9. Build HTML dashboard (bilingual)
    ↓
10. website_deploy → public URL (optional)
```

## Layered design

```
┌──────────────────────────────────────────────────────────┐
│ Skill entry point (SKILL.md — AI consumption)            │
└──────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────┐
│ 10-topic base pipeline (always run)                      │
│   - 5 sheet XLSX                                          │
│   - HTML dashboard                                        │
└──────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────┐
│ 4 deep-dive topics (run on request)                      │
│   - + Sheet 6 (Deep Dive)                                │
│   - + Sheet 7 (Signatures & Funding)                     │
└──────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────┐
│ Reusable scripts/                                        │
│   - filters.py                                           │
│   - region_classifier.py                                 │
│   - clusters.py                                          │
│   - bilingual.py                                         │
│   - build_xlsx.py (CLI entry point)                      │
└──────────────────────────────────────────────────────────┘
```

## Author-count filter rationale

Scopus exports often include physics consortium papers (ATLAS, CMS, LHCb) and Global Burden of Disease medical cohorts that have hundreds or thousands of co-authors. These papers:

- Appear at the top of every metric (FWCI, citations, etc.)
- Are not actually bilateral collaborations
- Skew researcher counts (one "consortium paper" may have 3,000 authors)
- Inflate paper counts by 50-60%

**Solution:** Filter papers to ≤50 authors. After filtering:

| Metric | Before | After | Change |
|---|---:|---:|---|
| Papers | 1,174 | 456 | -61% |
| Avg FWCI | 8.85 | 2.79 | -68% (now realistic) |
| Max FWCI | 927 | 67 | -93% (outliers removed) |
| Top field | Physics | CS / AI | **Real research focus** |

## Region classifier v3 design

The earlier v1/v2 classifiers used abbreviations (`"MIT"`, `"NUS"`) which miss many real Scopus entries. v3 uses **explicit full-name matching**:

```python
KEYWORD_RULES = {
    'US (other top)': lambda nm: any(k in nm for k in [
        'massachusetts institute of technology',  # not just "MIT"
        'harvard', 'university of california',
        'columbia', 'cornell', 'yale', ...
    ]),
    ...
}
```

This catches institutions Scopus writes as:
- "Massachusetts Institute of Technology" ✓
- "MIT Computer Science and Artificial Intelligence Laboratory" ✓
- "MIT, Department of Biology" ✓

## XLSX construction approach

We don't use `openpyxl.write()` directly because:

1. **Live formulas**: openpyxl can write formulas but not always parse them back
2. **Non-sequential rIds**: openpyxl-created XLSX often breaks in LibreOffice
3. **Color/style precision**: We need exact cell-by-cell color control (blue=input, black=formula, green=cross-sheet)

**Pattern:** Build XLSX XML directly, then post-process with LibreOffice:

```python
# 1. Build XML
import openpyxl
wb = openpyxl.Workbook()
# ... add sheets, formulas, styles
wb.save('/tmp/build.xlsx')

# 2. Pack (using minimax-xlsx skill)
python xlsx_pack.py /tmp/build.xlsx /tmp/final.xlsx

# 3. LibreOffice convert (fixes rIds)
libreoffice --headless --convert-to xlsx /tmp/final.xlsx --outdir /tmp/

# 4. Copy back
cp /tmp/final.xlsx ./output.xlsx
```

## Bilingual architecture

Two patterns based on deliverable:

**HTML** — toggleable visibility:
```html
<div class="lang-zh"><!-- 中文章节 --></div>
<div class="lang-en"><!-- English sections --></div>
```
```css
.lang-en { display: none; }
body.show-en .lang-zh { display: none; }
body.show-en .lang-en { display: block; }
```

**XLSX** — single column, both languages:
```
English | 中文
Total Papers | 总论文数
```

Why this pattern: XLSX doesn't natively support per-cell language toggle, so a single column with both languages is the cleanest approach.

## Deployment options

| Need | Solution |
|---|---|
| Quick share | `website_deploy` → `https://xyz.space.mcode.cn` |
| Offline viewing | Self-contained HTML with embedded data + XLSX |
| Mass distribution | ZIP bundle with HTML + XLSX + JSON |
| Email-ready | Small XLSX only (single sheet) |

## Performance

| Phase | Time | Notes |
|---|---|---|
| CSV parsing | <1s | pandas |
| Author filter | <1s | vectorized |
| Paper cache | <1s | dict construction |
| 10 topics | ~5s | mostly pandas operations |
| 4 deep-dive topics | ~3s | AI cluster + H-index |
| XLSX build | ~10s | XML construction |
| LibreOffice convert | ~20s | headless conversion |
| HTML build | ~1s | string templates |
| **Total (default 5 sheets)** | **~40s** | |
| **Total (full 7 sheets + bilingual HTML)** | **~2min** | |

## Validation

After each run, verify:

```bash
# 1. XLSX opens and formulas calculate
libreoffice --headless --calc --convert-to xlsx output.xlsx

# 2. HTML renders both languages
python3 -c "
from bs4 import BeautifulSoup
soup = BeautifulSoup(open('output.html').read())
zh = soup.find('div', class_='lang-zh')
en = soup.find('div', class_='lang-en')
assert len(zz.text) > 1000, 'lang-zh content too small'
assert len(en.text) > 1000, 'lang-en content too small'
print('✓ Both languages have substantial content')
"
```