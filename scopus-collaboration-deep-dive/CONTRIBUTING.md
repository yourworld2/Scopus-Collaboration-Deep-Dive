# Contributing

Thanks for considering a contribution to **scopus-collaboration-deep-dive**!

## Most useful contributions

1. **New region classifier rules** — extending `scripts/region_classifier.py` for other countries
2. **New cluster patterns** — life sciences, physics, materials, etc.
3. **New templated insights** — bibliometric patterns observed in different fields
4. **Translation corrections** in bilingual labels
5. **Bug fixes** — XLSX structural issues, formula errors, CSS rendering bugs

## Development setup

```bash
git clone https://github.com/minimax/scopus-collaboration-deep-dive.git
cd scopus-collaboration-deep-dive

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/

# Try on the example CSVs
python scripts/build_xlsx.py \
    --csv examples/yale-china/sample-input.csv \
    --source "Yale" \
    --target "China" \
    --output /tmp/test_output
```

## Pull request workflow

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/new-region-rule`)
3. Make changes (with tests if applicable)
4. Run `pytest tests/` to verify no regressions
5. Update [CHANGELOG.md](CHANGELOG.md) under "Unreleased" section
6. Open PR with before/after screenshots if visual changes

## Code style

- Python: PEP 8, type hints where possible, docstrings for public functions
- XLSX: Live formulas everywhere on derived metrics, never hardcoded ratios
- HTML: Self-contained (no external CDN/fonts), bilingual-ready by default

## Adding a new region classifier

To add rules for a new country (e.g., Singapore, Korea, Brazil):

1. Add keyword lists to `scripts/region_classifier.py`:
   ```python
   SINGAPORE_KEYWORDS = ['singapore', 'nus ', 'ntu', 'nanyang technological']
   ```
2. Add a check function:
   ```python
   def is_singapore_inst(name):
       nm = name.lower()
       return any(k in nm for k in SINGAPORE_KEYWORDS)
   ```
3. Update `classify_inst_v3()` to add a branch
4. Add a test case in `tests/test_region_classifier.py`
5. Update bilingual labels in `examples/*/README.md` if needed

## Adding a new cluster pattern

To add detection of, say, a Materials Science cluster:

1. Add to `scripts/clusters.py`:
   ```python
   def detect_materials_cluster(papers):
       """Papers with Materials Science ASJC field."""
       return [p for p in papers 
               if any('material' in f.lower() for f in p['fields'])]
   ```
2. Add a usage example in `examples/materials-cluster/`
3. Document in SKILL.md under "Deep-dive topics" section

## Testing

All PRs should pass `pytest tests/`. Add new tests for new functionality.

```python
# tests/test_my_feature.py
def test_author_count_filter():
    from scripts.filters import apply_author_filter
    df = pd.DataFrame(...)
    df_filtered, _ = apply_author_filter(df, max_authors=50)
    assert all(df_filtered['n_authors'] <= 50)
```

## Questions?

Open an issue. We're friendly.