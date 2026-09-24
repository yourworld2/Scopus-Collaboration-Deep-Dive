"""Author count filter — removes mega-author consortium papers.
作者数过滤器 — 剔除大型作者联盟论文。

Detects physics consortium papers (ATLAS/CMS/LHCb), Global Burden of Disease (GBD)
cohorts, and other mega-cohorts that dominate Scopus exports. These papers inflate
all metrics and obscure real bilateral collaboration patterns.

检测物理联盟论文（ATLAS/CMS/LHCb）、全球疾病负担（GBD）队列论文和其他大型队列论文，
它们主导了 Scopus 导出。这些论文会抬高所有指标，模糊真正的双边合作模式。
"""

import pandas as pd
from typing import Tuple


def count_authors(authors_str) -> int:
    """Count authors in a Scopus '|'-delimited string.
    统计 Scopus '|' 分隔字符串中的作者数。"""
    if pd.isna(authors_str) or not authors_str:
        return 0
    return len([a for a in str(authors_str).split('|') if a.strip()])


def apply_author_filter(df: pd.DataFrame, max_authors: int = 50,
                         verbose: bool = True) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Filter out papers with more than max_authors co-authors.
    过滤掉作者数超过 max_authors 的论文。

    Args:
        df: Input Scopus DataFrame (must have 'Authors' column). | 输入 Scopus DataFrame（必须有 'Authors' 列）。
        max_authors: Threshold; default 50. | 阈值；默认 50。
        verbose: Print distribution stats. | 打印分布统计。

    Returns:
        Tuple of (filtered_df, original_df). | (过滤后 DataFrame, 原始 DataFrame) 元组。
    """
    df = df.copy()
    df['_n_authors'] = df['Authors'].apply(count_authors)

    if verbose:
        n_orig = len(df)
        n_remove = (df['_n_authors'] > max_authors).sum()
        print(f"Author count distribution 作者数分布: max={df['_n_authors'].max()}, "
              f"median={df['_n_authors'].median():.0f}, "
              f">{max_authors}: {n_remove} ({n_remove/n_orig*100:.1f}%)")

    df_filtered = df[df['_n_authors'] <= max_authors].copy()
    df_filtered = df_filtered.drop(columns=['_n_authors'])

    if verbose:
        n_kept = len(df_filtered)
        n_removed = n_orig - n_kept
        print(f"Filtered 已过滤: {n_kept} papers kept 保留 "
              f"({n_removed/n_orig*100:.1f}% removed 已移除)")

    return df_filtered, df


def should_apply_filter(df: pd.DataFrame, threshold_pct: float = 30.0) -> bool:
    """Return True if the author-count filter is recommended (>threshold_pct papers
    have >50 authors).
    如果 >threshold_pct 的论文有 >50 作者，返回 True，表示建议应用过滤。

    Use this before applying the filter to avoid surprising the user.
    在应用过滤前使用此函数，避免给用户意外。
    """
    df = df.copy()
    df['_n'] = df['Authors'].apply(count_authors)
    pct = (df['_n'] > 50).sum() / len(df) * 100
    return bool(pct > threshold_pct)


def author_count_summary(df: pd.DataFrame) -> dict:
    """Return a summary of author count distribution for reporting.
    返回作者数分布的摘要，用于报告。"""
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