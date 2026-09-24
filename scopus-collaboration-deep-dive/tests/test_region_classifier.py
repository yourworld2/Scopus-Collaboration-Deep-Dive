"""Tests for the region classifier v3."""
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).parent.parent / 'scripts'
sys.path.insert(0, str(SCRIPT_DIR))

from region_classifier import (  # noqa
    classify_inst_v3,
    classify_batch,
    is_target_region,
    CHINESE_UNIVERSITY_KEYWORDS,
    EUROPEAN_UNIVERSITY_KEYWORDS,
)


def test_classify_stanford():
    assert classify_inst_v3('Stanford University') == 'Stanford (source)'
    assert classify_inst_v3('Stanford University School of Medicine') == 'Stanford (source)'


def test_classify_sjtu():
    assert classify_inst_v3('Shanghai Jiao Tong University') == 'Shanghai Jiao Tong (target)'
    assert classify_inst_v3('Shanghai Jiao Tong University School of Medicine') == 'Shanghai Jiao Tong (target)'


def test_classify_mainland_china():
    assert classify_inst_v3('Tsinghua University') == 'Mainland China'
    assert classify_inst_v3('Peking University') == 'Mainland China'
    assert classify_inst_v3('University of Science and Technology of China') == 'Mainland China'
    assert classify_inst_v3('Chinese Academy of Sciences') == 'Mainland China'


def test_classify_hk_macau_taiwan():
    assert classify_inst_v3('Hong Kong Polytechnic University') == 'Hong Kong / Macau / Taiwan'
    assert classify_inst_v3('National Taiwan University') == 'Hong Kong / Macau / Taiwan'
    assert classify_inst_v3('University of Macau') == 'Hong Kong / Macau / Taiwan'


def test_classify_us_top():
    assert classify_inst_v3('Massachusetts Institute of Technology') == 'US (other top)'
    assert classify_inst_v3('Harvard University') == 'US (other top)'
    assert classify_inst_v3('University of California, Berkeley') == 'US (other top)'
    assert classify_inst_v3('California Institute of Technology') == 'US (other top)'
    # 'MIT' as abbreviation alone won't match — full name is needed
    assert classify_inst_v3('MIT') == 'Other International'


def test_classify_europe():
    assert classify_inst_v3('ETH Zurich') == 'Germany / Switzerland'
    assert classify_inst_v3('University of Oxford') == 'UK'
    assert classify_inst_v3('Imperial College London') == 'UK'
    assert classify_inst_v3('Max Planck Institute') == 'Germany / Switzerland'


def test_classify_asia():
    assert classify_inst_v3('National University of Singapore') == 'Singapore'
    assert classify_inst_v3('Nanyang Technological University') == 'Singapore'
    assert classify_inst_v3('University of Tokyo') == 'Japan'
    assert classify_inst_v3('Seoul National University') == 'Korea'


def test_classify_fallback():
    assert classify_inst_v3('Unknown University in Timbuktu') == 'Other International'
    assert classify_inst_v3('') == 'Other International'
    assert classify_inst_v3(None) == 'Other International'


def test_classify_batch():
    entries = [
        {'institutions': ['Stanford University', 'Tsinghua University']},
        {'institutions': ['Shanghai Jiao Tong University', 'Massachusetts Institute of Technology']},
    ]
    result = classify_batch(entries)
    assert result['Stanford (source)'] == 1
    assert result['Mainland China'] == 1
    assert result['Shanghai Jiao Tong (target)'] == 1
    assert result['US (other top)'] == 1


def test_is_target_region_chinese():
    assert is_target_region('Tsinghua University', CHINESE_UNIVERSITY_KEYWORDS) is True
    assert is_target_region('Stanford University', CHINESE_UNIVERSITY_KEYWORDS) is False
    assert is_target_region('Tencent', CHINESE_UNIVERSITY_KEYWORDS) is True  # Chinese corporate


def test_is_target_region_european():
    assert is_target_region('University of Oxford', EUROPEAN_UNIVERSITY_KEYWORDS) is True
    assert is_target_region('Stanford University', EUROPEAN_UNIVERSITY_KEYWORDS) is False


def test_classify_priority():
    """Stanford should be classified as source, not US (other top)."""
    # 'stanford' is checked first in KEYWORD_RULES — verifies priority works
    result = classify_inst_v3('Stanford University')
    assert 'Stanford' in result  # source, not just US (other top)