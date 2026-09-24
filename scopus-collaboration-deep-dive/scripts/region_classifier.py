"""Region classifier v3 — handles 50+ US/international university names explicitly.

Maps each institution name to one of ~13 region categories. Handles full university
names (not just abbreviations) because Scopus writes them in varied forms.
"""

from typing import Optional


# Comprehensive keyword lists. Order matters — most-specific first.
KEYWORD_RULES = {
    'Stanford (source)': lambda nm: 'stanford' in nm,
    'Shanghai Jiao Tong (target)': lambda nm: 'shanghai jiao tong' in nm,
    'US (Federal/DOE)': lambda nm: 'united states department of energy' in nm,
    'US (National Labs)': lambda nm: any(k in nm for k in [
        'lawrence berkeley', 'lbnl', 'brookhaven', 'argonne', 'fermilab', 'slac'
    ]),
    'Mainland China': lambda nm: any(k in nm for k in [
        'peking', 'tsinghua', 'fudan', 'zhejiang',
        'university of science and technology of china', 'ustc',
        'beijing', 'nanjing', 'tongji', 'huazhong', 'wuhan',
        'shandong', 'sichuan', 'sun yat-sen', 'xiamen', 'central south',
        'xi an', "xi'an", 'university of chinese academy', 'chinese academy', 'cas ',
        'fudan university', 'shanghai medical', 'shanghai jiao',  # SJTU already handled
        'capital medical', 'guangzhou medical',
    ]),
    'Hong Kong / Macau / Taiwan': lambda nm: any(k in nm for k in [
        'hong kong', 'hkust', 'cuhk', 'chinese university of hong kong',
        'hong kong polytechnic', 'macau', 'macao', 'taiwan', 'national taiwan',
        'tsing hua',
    ]),
    'Singapore': lambda nm: any(k in nm for k in [
        'singapore', 'nus ', 'ntu', 'nanyang technological',
    ]),
    'CERN': lambda nm: 'cern' in nm,
    'Europe (physics labs)': lambda nm: any(k in nm for k in [
        'desy', 'in2p3', 'infn', 'nikhef', 'cnrs', 'csic', 'paul scherrer', 'psi',
    ]),
    'UK': lambda nm: any(k in nm for k in [
        'university college london', 'ucl ', 'oxford', 'cambridge', 'imperial',
        'manchester', 'edinburgh', 'university of london', 'london school', 'lse',
    ]),
    'Germany / Switzerland': lambda nm: any(k in nm for k in [
        'eth ', 'eth z', 'swiss federal', 'epfl', 'max planck', 'helmholtz',
        'munich', 'heidelberg', 'rwth', 'tübingen', 'freiburg', 'vienna', 'zurich',
    ]),
    'Japan': lambda nm: any(k in nm for k in [
        'tokyo', 'kyoto', 'osaka', 'riken', 'tohoku', 'waseda', 'keio',
        'hokkaido', 'nagoya', 'kobe',
    ]),
    'Korea': lambda nm: any(k in nm for k in [
        'korea', 'snu', 'kaist', 'yonsei', 'seoul national', 'postech',
    ]),
    'US (other top)': lambda nm: any(k in nm for k in [
        'harvard', 'massachusetts institute of technology',
        'university of california', 'berkeley',
        'columbia', 'cornell', 'yale', 'princeton',
        'duke', 'emory', 'rice', 'vanderbilt',
        'johns hopkins', 'northwestern', 'california institute of technology',
        'caltech', 'boston university', 'brown', 'dartmouth',
        'michigan, ann arbor', 'university of wisconsin', 'ohio state',
        'university of illinois', 'ucla', 'ucsf', 'ucsb', 'uc davis',
        'university of washington', 'university of pittsburgh',
        'penn state', 'pennsylvania', 'michigan state', 'purdue', 'texas a&m',
        'university of texas', 'georgia tech', 'usc',
        'university of southern california', 'university of north carolina',
        'university of maryland', 'virginia tech', 'case western',
        'minnesota', 'indiana university', 'colorado', 'rockefeller',
        'emory university',
    ]),
}


def classify_inst_v3(name: str) -> str:
    """Classify a single institution name into a region.

    Args:
        name: Institution name string (e.g., "Massachusetts Institute of Technology").

    Returns:
        One of the 14 region category strings. Falls back to 'Other International'.
    """
    if not name:
        return 'Other International'
    nm = name.lower()
    for region, rule in KEYWORD_RULES.items():
        if rule(nm):
            return region
    return 'Other International'


def classify_batch(entries, institutions_list=None) -> dict:
    """Classify all unique institutions and return counts.

    Args:
        entries: Iterable of paper records with 'institutions' key.
        institutions_list: Optional pre-extracted list of institutions.

    Returns:
        Dict mapping region → count of affiliation appearances.
    """
    from collections import Counter
    counter = Counter()
    if institutions_list is None:
        institutions_list = [inst for p in entries for inst in p.get('institutions', [])]
    for inst in institutions_list:
        counter[classify_inst_v3(inst)] += 1
    return dict(counter)


def is_target_region(name: str, target_keywords: list) -> bool:
    """Check if a name matches the target region keywords.

    Generic helper — pass any keyword list.
    """
    nm = name.lower()
    return any(k.lower() in nm for k in target_keywords)


# Pre-built common target filters
CHINESE_UNIVERSITY_KEYWORDS = [
    'peking', 'tsinghua', 'fudan', 'zhejiang', 'shanghai jiao',
    'university of science and technology of china', 'ustc',
    'hong kong', 'macau', 'macao', 'taiwan', 'national taiwan',
    'beijing', 'nanjing', 'wuhan', 'shandong', 'sichuan', 'xiamen',
    'chinese academy', 'cas ', 'huazhong', 'sun yat-sen', 'tongji',
    'central south', 'capital medical',
    # Chinese corporate research (not academic, but collaboration-related)
    'tencent', 'huawei', 'alibaba', 'baidu', 'bytedance', 'jd.com',
]


EUROPEAN_UNIVERSITY_KEYWORDS = [
    'oxford', 'cambridge', 'imperial', 'ucl',
    'eth zurich', 'epfl', 'max planck', 'helmholtz',
    'karolinska', 'sorbonne', 'paris sciences', 'lettres',
    'university college london',
]