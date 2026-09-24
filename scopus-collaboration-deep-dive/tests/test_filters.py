"""Tests for the author-count filter."""
import sys
from pathlib import Path

import pandas as pd

# Add scripts/ to path
SCRIPT_DIR = Path(__file__).parent.parent / 'scripts'
sys.path.insert(0, str(SCRIPT_DIR))

from filters import apply_author_filter, count_authors, should_apply_filter, author_count_summary  # noqa


def test_count_authors_empty():
    assert count_authors(None) == 0
    assert count_authors('') == 0
    assert count_authors(float('nan')) == 0


def test_count_authors_simple():
    assert count_authors('Smith, J. | Doe, A. | Brown, K.') == 3


def test_count_authors_with_whitespace():
    assert count_authors(' | Smith, J. |  Doe, A. | ') == 2


def test_apply_author_filter_basic():
    df = pd.DataFrame({
        'Authors': [
            'Smith, J. | Doe, A.',  # 2
            'Smith, J. | Doe, A. | Brown, K. | Wilson, L. | Taylor, M.',  # 5
            ' | '.join([f'Author{i}, X.' for i in range(60)]),  # 60
            ' | '.join([f'Author{i}, X.' for i in range(20)]),  # 20
        ]
    })
    df_filtered, _ = apply_author_filter(df, max_authors=50, verbose=False)
    assert len(df_filtered) == 3  # excludes 60-author paper


def test_apply_author_filter_returns_original():
    df = pd.DataFrame({
        'Authors': ['A | B | C', 'X | Y'],
    })
    df_filtered, df_orig = apply_author_filter(df, max_authors=10, verbose=False)
    assert len(df_orig) == 2
    assert len(df_filtered) == 2  # both pass


def test_should_apply_filter_threshold():
    # 60% have >50 authors → should apply
    authors_list = (
        ['A | B'] * 4 +
        [' | '.join([f'Author{i}, X.' for i in range(60)])] * 6
    )
    df = pd.DataFrame({'Authors': authors_list})
    assert should_apply_filter(df, threshold_pct=30.0) is True


def test_should_apply_filter_small_dataset():
    # 0% have >50 authors → should NOT apply
    df = pd.DataFrame({'Authors': ['A | B | C'] * 10})
    assert should_apply_filter(df, threshold_pct=30.0) is False


def test_author_count_summary_keys():
    df = pd.DataFrame({'Authors': ['A | B | C', 'X | Y']})
    summary = author_count_summary(df)
    assert 'max' in summary
    assert 'median' in summary
    assert 'pct_over_50' in summary
    assert summary['max'] == 3


def test_author_count_summary_over_50_pct():
    authors_list = (
        ['A | B'] * 5 +
        [' | '.join([f'Author{i}, X.' for i in range(60)])] * 5
    )
    df = pd.DataFrame({'Authors': authors_list})
    summary = author_count_summary(df)
    assert summary['pct_over_50'] == 50.0