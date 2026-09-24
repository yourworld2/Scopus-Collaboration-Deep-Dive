"""Tests for bilingual label generation."""
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).parent.parent / 'scripts'
sys.path.insert(0, str(SCRIPT_DIR))

from bilingual import (  # noqa
    B,
    translate_region,
    bilingual_region_table,
    REGION_TRANSLATIONS,
    LABEL_TRANSLATIONS,
    QUALITY_SCORE_DESC,
    NAME_DISAMBIGUATION_DESC,
)


def test_b_label():
    assert B('Total Publications', '总发表数') == 'Total Publications | 总发表数'


def test_translate_region():
    assert translate_region('Mainland China') == '中国大陆（其他）'
    assert translate_region('Hong Kong / Macau / Taiwan') == '香港 / 澳门 / 台湾'


def test_translate_region_unknown():
    assert translate_region('Unknown Region') == 'Unknown Region'


def test_bilingual_region_table():
    data = {'Mainland China': 100, 'US (other top)': 80, 'Other International': 50}
    table = bilingual_region_table(data)
    assert len(table) == 3
    assert table[0][0] == 'Mainland China'
    assert table[0][1] == '中国大陆（其他）'
    assert table[0][2] == 100
    assert abs(table[0][3] - 43.48) < 0.1


def test_region_translations_keys_present():
    """Verify all 14 known regions have translations."""
    expected = {
        'Stanford (source)', 'Shanghai Jiao Tong (target)',
        'Mainland China', 'US (other top)', 'Hong Kong / Macau / Taiwan',
        'US (Federal/DOE)', 'Germany / Switzerland', 'UK', 'Singapore',
        'US (National Labs)', 'Europe (physics labs)', 'Japan', 'Korea',
        'Other International',
    }
    assert expected.issubset(set(REGION_TRANSLATIONS.keys()))


def test_label_translations_keys_present():
    """Spot-check key labels."""
    assert 'Overview' in LABEL_TRANSLATIONS
    assert 'Top 20 Partner Institutions' in LABEL_TRANSLATIONS
    assert 'Year' in LABEL_TRANSLATIONS


def test_quality_score_desc_bilingual():
    assert 'en' in QUALITY_SCORE_DESC
    assert 'zh' in QUALITY_SCORE_DESC
    assert 'sqrt' in QUALITY_SCORE_DESC['en']
    assert 'sqrt' in QUALITY_SCORE_DESC['zh']


def test_name_disambiguation_desc():
    assert 'Scopus' in NAME_DISAMBIGUATION_DESC['en']
    assert 'Scopus' in NAME_DISAMBIGUATION_DESC['zh']


def test_b_label_empty_chinese():
    """B() should still work even if Chinese is empty."""
    assert B('Hello', '') == 'Hello | '