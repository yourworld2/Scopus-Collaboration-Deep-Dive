#!/usr/bin/env python3
"""Build a Scopus collaboration XLSX + HTML dashboard from a CSV export.

Usage:
    python scripts/build_xlsx.py --csv path/to/scopus.csv --source "Yale" --target "China" --output ./output

This is a working example / reference implementation. For the production version
used by Mavis, the XLSX construction is integrated with the minimax-xlsx skill
(xlsx_pack.py + LibreOffice post-process). See SKILL.md for full details.
"""

import argparse
import json
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path

import pandas as pd

# Add the scripts/ directory to the path so we can import siblings
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from filters import apply_author_filter, should_apply_filter, author_count_summary  # noqa
from region_classifier import classify_inst_v3, classify_batch  # noqa


def load_csv(csv_path: str) -> pd.DataFrame:
    """Load a Scopus CSV export with header detection."""
    # Try common header offsets
    for skiprows in [18, 19, 20, 21]:
        try:
            df = pd.read_csv(csv_path, skiprows=skiprows)
            if 'Title' in df.columns and 'Authors' in df.columns:
                print(f"Loaded {csv_path} with skiprows={skiprows}: {len(df)} rows")
                return df
        except Exception:
            continue
    raise ValueError(f"Could not find Scopus header in {csv_path}. Check file format.")


def numeric_coerce(df: pd.DataFrame) -> pd.DataFrame:
    """Coerce numeric columns that come in as strings."""
    for col in ['Year', 'Citations', 'Field-Weighted Citation Impact',
                'Field-Weighted View Impact', 'Topic Cluster Prominence Percentile',
                'Topic Prominence Percentile',
                'Outputs in Top Citation Percentiles, per percentile']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    return df


def build_paper_cache(df: pd.DataFrame) -> list:
    """Convert DataFrame rows to paper records (dicts)."""
    papers = []
    for _, row in df.iterrows():
        authors_raw = row.get('Authors', '')
        authors = ([a.strip() for a in str(authors_raw).split('|') if a.strip()]
                   if pd.notna(authors_raw) and authors_raw else [])
        insts_raw = row.get('Institutions', '')
        insts = ([i.strip() for i in str(insts_raw).split('|') if i.strip()]
                 if pd.notna(insts_raw) and insts_raw else [])
        fields_raw = row.get('All Science Journal Classification (ASJC) field name', '')
        fields = ([f.strip() for f in str(fields_raw).split('|') if f.strip()]
                  if pd.notna(fields_raw) and fields_raw else [])
        papers.append({
            'title': row.get('Title', ''),
            'authors': authors,
            'institutions': insts,
            'fields': fields,
            'journal': str(row.get('Scopus Source title', '')).strip()
                        if pd.notna(row.get('Scopus Source title')) else '',
            'citations': float(row['Citations']) if pd.notna(row.get('Citations')) else 0,
            'fwci': (float(row['Field-Weighted Citation Impact'])
                     if pd.notna(row.get('Field-Weighted Citation Impact')) else None),
            'year': int(row['Year']) if pd.notna(row.get('Year')) else None,
        })
    return papers


def main():
    parser = argparse.ArgumentParser(description='Build Scopus collaboration XLSX')
    parser.add_argument('--csv', required=True, help='Path to Scopus CSV export')
    parser.add_argument('--source', required=True, help='Source university name (e.g., "Yale")')
    parser.add_argument('--target', required=True, help='Target region (e.g., "China")')
    parser.add_argument('--output', default='./output', help='Output directory')
    parser.add_argument('--no-filter', action='store_true',
                        help='Skip author-count filter (use only for small datasets)')
    parser.add_argument('--bilingual', action='store_true',
                        help='Generate bilingual EN+中文 output')
    args = parser.parse_args()

    # Setup
    os.makedirs(args.output, exist_ok=True)
    print(f"=== Scopus Collaboration Deep Dive ===")
    print(f"Source: {args.source}")
    print(f"Target: {args.target}")
    print(f"Output: {args.output}\n")

    # 1. Load
    df = load_csv(args.csv)
    df = numeric_coerce(df)

    # 2. Author-count filter (with confirmation)
    if not args.no_filter and should_apply_filter(df):
        print(f"\n⚠️  >30% papers have >50 authors. Applying author-count filter.")
        df, _ = apply_author_filter(df, max_authors=50)
    elif not args.no_filter:
        # Run anyway for stats
        apply_author_filter(df, max_authors=50, verbose=True)

    # 3. Build paper cache
    papers = build_paper_cache(df)
    print(f"\n📊 Loaded {len(papers)} papers")

    # 4. Basic analysis
    fwci_vals = [p['fwci'] for p in papers if p['fwci'] is not None]
    print(f"   Avg FWCI: {sum(fwci_vals)/len(fwci_vals):.2f}")
    print(f"   Total citations: {sum(p['citations'] for p in papers):,}")

    # 5. Region distribution
    region_counter = classify_batch(papers)
    print(f"\n🌍 Top 5 regions:")
    for region, count in Counter(region_counter).most_common(5):
        print(f"   {region:35s} {count:5d} ({count/sum(region_counter.values())*100:.1f}%)")

    # 6. Top journals + fields
    journal_counter = Counter(p['journal'] for p in papers if p['journal'])
    field_counter = Counter()
    for p in papers:
        for f in p['fields']:
            if f and f != 'Multidisciplinary':
                field_counter[f] += 1

    print(f"\n📰 Top 5 journals:")
    for j, c in journal_counter.most_common(5):
        print(f"   {j:50s} {c:3d} papers")

    print(f"\n📚 Top 5 fields:")
    for f, c in field_counter.most_common(5):
        print(f"   {f:50s} {c:3d} papers")

    # 7. Save intermediate JSON
    summary = {
        'source': args.source,
        'target': args.target,
        'total_papers': len(papers),
        'total_citations': sum(p['citations'] for p in papers),
        'avg_fwci': sum(fwci_vals) / len(fwci_vals) if fwci_vals else 0,
        'regions': dict(Counter(region_counter).most_common()),
        'top_journals': [{'name': j, 'papers': c} for j, c in journal_counter.most_common(20)],
        'top_fields': [{'name': f, 'papers': c} for f, c in field_counter.most_common(20)],
    }
    with open(os.path.join(args.output, 'summary.json'), 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print(f"\n✅ Summary saved to {args.output}/summary.json")

    # 8. Note about XLSX
    print(f"\n📝 Note: For full XLSX + HTML dashboard, use the Mavis skill.")
    print(f"   This script produces a summary JSON. Run the full pipeline via:")
    print(f"   'Mavis, analyze {args.source} × {args.target} collaboration'")
    print(f"   Or in standalone mode, see SKILL.md for the full 9-step procedure.")


if __name__ == '__main__':
    main()