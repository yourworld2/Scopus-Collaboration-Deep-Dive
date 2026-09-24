"""Author count filter — removes mega-author consortium papers.

Detects physics consortium papers (ATLAS/CMS/LHCb), Global Burden of Disease (GBD)
cohorts, and other mega-cohorts that dominate Scopus exports. These papers inflate
all metrics and obscure real bilateral collaboration patterns.
"""

import pandas as pd
from typing import Tuple


def count_authors(authors_str) -> int:
    """Count authors in a Scopus '|'-delimited string."""
    if pd.isna(authors_str) or not authors_str:
        return 0
    return len([a for a in str(authors_str).split('|') if a.strip()])


def apply_author_filter(df: pd.DataFrame, max_authors: int = 50,
                         verbose: bool = True) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Filter out papers with more than max_authors co-authors.

    Args:
        df: Input Scopus DataFrame (must have 'Authors' column).
        max_authors: Threshold; default 50.
        verbose: Print distribution stats.

    Returns:
        Tuple of (filtered_df, original_df).
    """
    df = df.copy()
    df['_n_authors'] = df['Authors'].apply(count_authors)

    if verbose:
        n_orig = len(df)
        n_remove = (df['_n_authors'] > max_authors).sum()
        print(f"Author count distribution: max={df['_n_authors'].max()}, "
              f"median={df['_n_authors'].median():.0f}, "
              f">{max_authors}: {n_remove} ({n_remove/n_orig*100:.1f}%)")

    df_filtered = df[df['_n_authors'] <= max_authors].copy()
    df_filtered = df_filtered.drop(columns=['_n_authors'])

    if verbose:
        n_kept = len(df_filtered)
        n_removed = n_orig - n_kept
        print(f"Filtered: {n_kept} papers kept "
              f"({n_removed/n_orig*100:.1f}% removed)")

    return df_filtered, df


def should_apply_filter(df: pd.DataFrame, threshold_pct: float = 30.0) -> bool:
    """Return True if the author-count filter is recommended (>threshold_pct papers
    have >50 authors).

    Use this before applying the filter to avoid surprising the user.
    """
    df = df.copy()
    df['_n'] = df['Authors'].apply(count_authors)
    pct = (df['_n'] > 50).sum() / len(df) * 100
    return bool(pct > threshold_pct)


def author_count_summary(df: pd.DataFrame) -> dict:
    """Return a summary of author count distribution for reporting."""
    counts = df['Authors'].apply(count_authors)
    return {
        'min': int(counts.min()),
        'max': int(counts.max()),
        'median': float(counts.median()),
        'mean': float(counts.mean()),
        'pct_over_50': float((counts > 50).sum() / len(counts) * 100),
        'pct_over_100': float((counts > 100).sum() / len(counts) * 100),
        'pct_over_1000': float((counts > 1000).sum() / len(counts) * 100),
    }