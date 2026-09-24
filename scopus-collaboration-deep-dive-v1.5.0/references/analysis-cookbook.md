# Analysis Cookbook — Concrete code snippets

Each section maps to one of the 7 sheets in the deliverable XLSX.

---

## 1. CSV Header Detection

Scopus exports wrap metadata in the first ~20 rows. Find the real header:

```python
import pandas as pd

# Try skipping known pre-amble row counts
for skip in [0, 19, 20, 21]:
    df = pd.read_csv(path, skiprows=skip)
    if 'Title' in df.columns and 'Authors' in df.columns:
        print(f"Header found at skiprows={skip}")
        break

# Required columns (warn if missing)
required = ['Title', 'Authors', 'Year', 'Citations',
            'Field-Weighted Citation Impact', 'Scopus Source title',
            'Institutions', 'All Science Journal Classification (ASJC) field name',
            'Outputs in Top Citation Percentiles, per percentile']
missing = [c for c in required if c not in df.columns]
if missing:
    print(f"WARN: missing {missing} — these sections will degrade")
```

---

## 2. Numeric Column Coercion

```python
for col in ['Year', 'Citations', 'Field-Weighted Citation Impact',
            'Field-Weighted View Impact', 'Topic Cluster Prominence Percentile',
            'Outputs in Top Citation Percentiles, per percentile']:
    df[col] = pd.to_numeric(df[col], errors='coerce')
```

---

## 3. Chinese Institution Filter

Exclude non-Chinese majors and top US/UK names that frequently appear in Scopus affiliation strings:

```python
def is_chinese_inst(name):
    nm = name.lower()
    non_chinese = ['harvard', 'stanford', 'mit ', 'mit,', 'cambridge', 'oxford',
                   'rice university', 'emory', 'duke', 'penn state',
                   'michigan,', 'washington,', 'wisconsin', 'minnesota', 'toronto',
                   'nus', 'singapore', 'tokyo', 'max planck', 'delft', 'amsterdam',
                   'northwestern university']
    for nc in non_chinese:
        if nc in nm: return False
    if 'yale' in nm: return False
    return any(kw in nm for kw in ['chinese academy', 'peking', 'tsinghua',
                                    'beijing', 'shanghai', 'fudan', 'zhejiang',
                                    'nanjing', 'wuhan', 'sichuan', 'hong kong',
                                    'taiwan', 'shenzhen', 'sustech', 'westlake',
                                    'tencent', 'alibaba', 'baidu', 'huawei'])
```

For other regions, swap keywords: `is_european_inst()` would include Oxford/Cambridge/Max Planck/etc., exclude US names.

---

## 4. ASJC Major Category Mapping

Map ~293 ASJC fields to 5 categories via keyword matching:

```python
def categorize_field(field):
    f = field.lower()
    if any(kw in f for kw in ['medicine', 'immunology', 'pharmacology', 'neuroscience',
                                'biology', 'biochem', 'genetics', 'molecular',
                                'psychiatry', 'mental health', 'clinical', 'oncology',
                                'cardiology', 'epidemiology', 'cancer', 'cell biology']):
        return 'Life Sciences & Medicine'
    if any(kw in f for kw in ['chemistry', 'physics', 'astronomy', 'material',
                                'engineering', 'mechanical', 'electrical', 'energy',
                                'geology', 'environmental', 'ecology', 'mathematics',
                                'statistics', 'probability', 'applied mathematics']):
        return 'Physical Sciences & Engineering'
    if any(kw in f for kw in ['computer science', 'software', 'artificial intelligence',
                                'information system', 'machine learning']):
        return 'Computer Science & AI'
    if any(kw in f for kw in ['economics', 'business', 'sociology', 'psychology',
                                'education', 'political', 'law', 'history',
                                'language', 'linguistics', 'public health']):
        return 'Social Sciences & Humanities'
    if 'multidisciplinary' in f:
        return 'Multidisciplinary'
    return 'Other'
```

---

## 5. H-Index Computation

```python
def compute_h_index(papers):
    citations_sorted = sorted([p['citations'] for p in papers], reverse=True)
    h = 0
    for i, c in enumerate(citations_sorted, 1):
        if c >= i:
            h = i
        else:
            break
    return h
```

The H-index is **estimated** from this dataset only — not the researcher's full career.

---

## 6. Signature Paper Scoring

Score = Citations × 0.5 + FWCI × 10 + (101 - Percentile) × 0.5

```python
for p in papers:
    pct_score = (101 - (p['pct_percentile'] or 50)) if p['pct_percentile'] else 50
    p['signature_score'] = p['citations'] * 0.5 + p['fwci'] * 10 + pct_score * 0.5
papers.sort(key=lambda x: -x['signature_score'])
```

Higher = more impactful work. Top 6 per cluster.

---

## 7. Funding Horizon Proxies

When direct funding data is missing:

```python
# Top 1% / 5% / 10% percentile (1.0 = top 1% most cited)
df['pct'] = df['Outputs in Top Citation Percentiles, per percentile']
top_1pct = df[df['pct'] <= 1.0]

# Multi-sector papers (≥2 sectors)
df['sector_count'] = df['Sector'].apply(lambda s: len(str(s).split('|')) if pd.notna(s) else 0)
multi_sector = df[df['sector_count'] >= 2]

# Open Access rate
oa_dist = df['Open Access'].value_counts()
```

---

## 8. XLSX Building Workflow

Always use this exact pattern (openpyxl is unreliable for multi-sheet authoring):

```python
# 1. Build sharedStrings.xml + per-sheet XML files in a temp dir
# 2. Run `xlsx_pack.py` from minimax-xlsx skill
# 3. LibreOffice convert to fix non-sequential rIds
# 4. Copy LO output back over original file
# 5. Run `formula_check.py` to validate

import subprocess, shutil
subprocess.run(['python3', '/workspace/.skills/minimax-xlsx/scripts/xlsx_pack.py',
                '/tmp/xlsx_work/', '/workspace/analysis/output.xlsx'])
subprocess.run(['libreoffice', '--headless', '--convert-to', 'xlsx',
                '--outdir', '/tmp/check_xlsx/converted',
                '/workspace/analysis/output.xlsx'])
shutil.copy('/tmp/check_xlsx/converted/output.xlsx',
            '/workspace/analysis/output.xlsx')
```

---

## 9. Sheet XML Snippet (formula-based share)

```python
sheet.append('<row r="{}">'.format(row) +
    cell_num("A{}".format(row), rank, 10) +
    cell_str("B{}".format(row), idx[name]) +
    cell_num("C{}".format(row), papers, 10) +
    cell_formula("D{}".format(row), "C{}/{}".format(row, total_papers), 8) +
    '</row>')
```

The formula `=C{row}/{total}` recomputes share when total_papers changes. Style 8 = percentage format.

---

## 10. Color Convention Cheatsheet

| Style ID | Purpose | Color |
|---|---|---|
| 0 | Default | Black |
| 1 | Label / header text | Bold black |
| 3 | Sub-header | Bold |
| 4 | Section title | Bold dark blue (#00356b) |
| 8 | Percentage (formula) | Black |
| 10 | Integer number (cell) | Black |
| 11 | Integer number (label column) | Bold black |
| 13 | Decimal (2-decimal, black) | Black |
| 14 | Decimal (2-decimal, blue) | Blue (input) |

Blue = hardcoded data input. Black = formula result. Green (style not yet registered) = cross-sheet reference.

---

## 11. Iteration Pattern

User asks "what about X?" → don't rebuild. Add a sheet:

```python
# Reuse intermediates from previous run
with open('/workspace/analysis/final_data.json') as f:
    data = json.load(f)

# Compute new metric (e.g., yearly concentration)
new_data = compute_yearly_concentration(...)

# Append Sheet 7 to existing XLSX without rebuilding sheets 1-6
# (See scopus-collaboration-deep-dive SKILL.md step 3 for the XML manipulation pattern)
```
---

## Author-count filter (added Sep 2026)

Use this BEFORE any other analysis to detect consortium paper dominance:

```python
def apply_author_filter(df, max_authors=50, verbose=True):
    """Filter out mega-author consortium papers (ATLAS/CMS/GBD/etc).
    
    Returns filtered df. If >30% of papers are removed, this is a strong signal
    the dataset is dominated by physics/medical consortium work.
    """
    df = df.copy()
    df['n_authors'] = df['Authors'].fillna('').apply(
        lambda x: len([a for a in str(x).split('|') if a.strip()])
    )
    if verbose:
        print(f"Original papers: {len(df)}")
        print(f"Authors distribution: max={df['n_authors'].max()}, "
              f"median={df['n_authors'].median()}, "
              f">{max_authors}: {(df['n_authors']>max_authors).sum()} "
              f"({(df['n_authors']>max_authors).sum()/len(df)*100:.1f}%)")
    
    df_filtered = df[df['n_authors'] <= max_authors].copy()
    df_filtered = df_filtered.drop(columns=['n_authors'])
    
    if verbose:
        print(f"Filtered: {len(df_filtered)} papers "
              f"({(len(df)-len(df_filtered))/len(df)*100:.1f}% removed)")
    
    return df_filtered, df
```

Use case: Stanford × SJTU 2022-2026 — 1174 papers had 60% with >50 authors. After filter: 456 papers with realistic distribution (median 8 authors).

---

## Region classifier v3 (added Sep 2026)

Better classification than naive "is_chinese_inst()" — handles full university names, country/region keywords, and edge cases:

```python
def classify_inst_v3(name):
    """Classify an institution by region. Returns short region code."""
    nm = name.lower()
    if 'stanford' in nm: return 'Stanford (source)'
    if 'shanghai jiao tong' in nm: return 'Shanghai Jiao Tong (target)'
    if 'united states department of energy' in nm: return 'US (Federal/DOE)'
    if any(k in nm for k in ['lawrence berkeley', 'lbnl', 'brookhaven', 'argonne', 
                              'fermilab', 'slac']): return 'US (National Labs)'
    if any(k in nm for k in ['peking', 'tsinghua', 'fudan', 'zhejiang', 
                              'university of science and technology of china', 'ustc',
                              'beijing', 'nanjing', 'tongji', 'huazhong', 'wuhan']): 
        return 'Mainland China'
    if any(k in nm for k in ['hong kong', 'hkust', 'cuhk', 'macau', 'taiwan']): 
        return 'Hong Kong / Macau / Taiwan'
    if 'singapore' in nm or 'ntu' in nm or 'nanyang' in nm: return 'Singapore'
    if 'cern' in nm: return 'CERN'
    if any(k in nm for k in ['oxford', 'cambridge', 'imperial', 'ucl']): return 'UK'
    if any(k in nm for k in ['eth ', 'max planck', 'helmholtz']): return 'Germany / Switzerland'
    if any(k in nm for k in ['tokyo', 'kyoto', 'riken']): return 'Japan'
    if any(k in nm for k in ['harvard', 'berkeley', 'mit ', 'cornell', 'yale', 
                              'princeton', 'johns hopkins', 'caltech', 
                              'northwestern', 'duke', 'emory']): return 'US (other top)'
    return 'Other International'
```

For Chinese-name B-classification: check `'massachusetts institute of technology'` not just `'mit'` (Scopus writes full names often).

---

## ASJC major-category aggregation (5 buckets)

Useful when ASJC has 200+ distinct codes — collapse to 5 broad academic areas:

```python
def categorize_field(field):
    """Map any ASJC field to one of 5 major categories."""
    f = field.lower()
    if any(kw in f for kw in ['medicine', 'immunology', 'pharmacology', 'neuroscience',
                                'biology', 'biochem', 'genetics', 'molecular', 'clinical',
                                'pathology', 'surgery', 'cardiology', 'oncology', 'physiology']):
        return 'Life Sciences & Medicine'
    if any(kw in f for kw in ['chemistry', 'physics', 'astronomy', 'material', 
                                'engineering', 'mathematics', 'statistics', 'geology',
                                'earth', 'ocean', 'environmental']):
        return 'Physical Sciences & Engineering'
    if any(kw in f for kw in ['computer science', 'software', 'artificial intelligence',
                                'machine learning', 'data processing']):
        return 'Computer Science & AI'
    if any(kw in f for kw in ['economics', 'business', 'sociology', 'psychology', 
                                'education', 'social', 'political', 'law', 'history',
                                'language', 'philosophy']):
        return 'Social Sciences & Humanities'
    if 'multidisciplinary' in f: return 'Multidisciplinary'
    return 'Other'
```

Each paper may belong to multiple ASJC fields → multiple categories. Count once per category per paper.

---

## AI cluster detection by Chinese surname pattern

For AI/ML papers in Chinese co-author networks, define the cluster by the most common surnames:

```python
AI_SURNAMES = ['Wang', 'Li', 'Liu', 'Zhang', 'Ma', 'Zhao', 'Chen', 'Tang', 
               'Sun', 'Cai', 'Hu']

def detect_ai_cluster(papers, surnames=AI_SURNAMES):
    """Papers with any author whose surname matches a top CS/AI Chinese name.
    
    'Author' is in Scopus format 'Last, Initial' (e.g., 'Wang, Y.'). Match on Last.
    """
    ai_papers = [p for p in papers 
                 if any(a.split(',')[0].strip() in surnames for a in p['authors'])]
    return ai_papers
```

Stanford case: 123/456 (27%) papers match. Confirms AI/ML is the dominant research theme.

---

## Multi-US partnership profile (when source = US, target = non-US)

```python
def detect_multi_us_papers(papers, source_name='Stanford', 
                            non_source_us_universities=None):
    """Count papers with source + target + ≥1 other US university.
    Indicates target university is tied into US-wide network, not just bilateral."""
    if non_source_us_universities is None:
        # Top 30 US universities (full names — Scopus uses these)
        non_source_us_universities = {
            'harvard', 'massachusetts institute of technology', 
            'university of california, berkeley', 'columbia', 'yale', 'cornell',
            'university of chicago', 'johns hopkins', 'university of pennsylvania',
            'new york university', 'northwestern', 'duke', 'university of michigan',
            'carnegie mellon', 'emory', 'rice', 'washington university', 'boston university',
            'case western', 'university of southern california'
        }
    
    multi_us = []
    for p in papers:
        has_source = any(source_name.lower() in i.lower() for i in p['institutions'])
        other_us_count = sum(1 for i in p['institutions'] 
                              if any(u in i.lower() for u in non_source_us_universities))
        if has_source and other_us_count >= 1:
            multi_us.append(p)
    return multi_us
```

Stanford case: 200/456 (43.9%) papers meet this criterion.

---

## Bilingual XLSX label pattern

For Chinese + English XLSX labels (single column, both languages):

```python
def B(en, zh):
    """Bilingual label with pipe separator."""
    return en + ' | ' + zh

# All labels use B("English", "中文")
# Section headers, table headers, region names, all get bilingual version.
```

Sheet names stay English (Excel works best with ASCII). Region names get bilingual: `Stanford (source) → Stanford (source) | 斯坦福（源）`.

## Bilingual HTML toggle pattern

```html
<style>
body.lang-en .lang-zh { display: none; }
body.lang-zh .lang-en { display: none; }
body.lang-en .lang-zh-row { display: table-row; }
</style>

<div class="lang-bar">
    <button class="lang-btn active" onclick="setLang('zh')">中文</button>
    <button onclick="setLang('en')">English</button>
</div>

<div class="lang-zh">...</div>
<div class="lang-en">...</div>

<script>
function setLang(lang) {
    document.body.className = 'lang-' + lang;
}
</script>
```

Wrap each language in its own `<div class="lang-en">` / `<div class="lang-zh">` and toggle `body.className`.
