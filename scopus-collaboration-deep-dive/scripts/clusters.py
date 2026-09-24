"""Cluster detection patterns.

Detects research clusters from a list of papers by author/field patterns.
Add new clusters here.
"""

from collections import Counter, defaultdict
from typing import Callable


# Cluster 1: AI/ML — by Chinese surname pattern
AI_SURNAMES = ['Wang', 'Li', 'Liu', 'Zhang', 'Ma', 'Zhao', 'Chen',
                 'Tang', 'Sun', 'Cai', 'Hu']


def detect_ai_cluster(papers):
    """Papers with any author whose surname matches a top CS/AI Chinese name.

    'Author' is in Scopus format 'Last, Initial' (e.g., 'Wang, Y.').
    Match on the Last part only.
    """
    return [p for p in papers
            if any(a.split(',')[0].strip() in AI_SURNAMES for a in p.get('authors', []))]


# Cluster 2: Materials Science — by ASJC field
MATERIALS_FIELDS = ['material', 'ceramic', 'polymer', 'metallurg']


def detect_materials_cluster(papers):
    """Papers with Materials Science ASJC field."""
    cluster = []
    for p in papers:
        fields = p.get('fields', [])
        if any(any(kw in f.lower() for kw in MATERIALS_FIELDS) for f in fields):
            cluster.append(p)
    return cluster


# Cluster 3: Life Sciences / Medicine — by ASJC field
LIFE_SCI_FIELDS = [
    'medicine', 'immunology', 'pharmacology', 'neuroscience', 'neurology',
    'biology', 'biochem', 'genetics', 'molecular', 'physiology', 'microbiology',
    'clinical', 'pathology', 'surgery', 'cardiology', 'oncology', 'cancer',
    'cell biology', 'developmental biology', 'biophysics', 'anatomy',
    'epidemiology', 'public health',
]


def detect_life_sciences_cluster(papers):
    """Papers in life sciences / medicine."""
    cluster = []
    for p in papers:
        fields = p.get('fields', [])
        if any(any(kw in f.lower() for kw in LIFE_SCI_FIELDS) for f in fields):
            cluster.append(p)
    return cluster


# Cluster 4: Physical Sciences / Engineering — by ASJC field
PHYS_SCI_FIELDS = [
    'chemistry', 'physics', 'astronomy', 'engineering', 'mechanical',
    'electrical', 'electronic', 'chemical engineering', 'civil engineering',
    'industrial', 'manufacturing', 'metallurgy', 'ceramic', 'polymer',
    'optics', 'laser', 'energy', 'fuel', 'geology', 'earth', 'planet',
    'ocean', 'atmospheric', 'environmental', 'ecology', 'mining', 'petroleum',
    'geochemistry', 'geophysics', 'mathematics', 'statistics',
]


def detect_phys_sci_cluster(papers):
    """Papers in physical sciences / engineering."""
    cluster = []
    for p in papers:
        fields = p.get('fields', [])
        if any(any(kw in f.lower() for kw in PHYS_SCI_FIELDS) for f in fields):
            cluster.append(p)
    return cluster


# Cluster 5: CS / AI — by ASJC field
CS_AI_FIELDS = [
    'computer science', 'software', 'artificial intelligence',
    'machine learning', 'data processing',
]


def detect_cs_ai_cluster(papers):
    """Papers in computer science / AI."""
    cluster = []
    for p in papers:
        fields = p.get('fields', [])
        if any(any(kw in f.lower() for kw in CS_AI_FIELDS) for f in fields):
            cluster.append(p)
    return cluster


# Cluster helpers
def cluster_summary(cluster_papers, all_papers) -> dict:
    """Return summary stats for a cluster."""
    n = len(cluster_papers)
    fwci_vals = [p['fwci'] for p in cluster_papers if p.get('fwci') is not None]
    return {
        'size': n,
        'share_of_total': n / len(all_papers) * 100 if all_papers else 0,
        'avg_fwci': sum(fwci_vals) / len(fwci_vals) if fwci_vals else None,
        'total_citations': sum(p.get('citations', 0) for p in cluster_papers),
    }


def cluster_yearly_stats(cluster_papers) -> dict:
    """Return yearly paper count for a cluster."""
    counter = Counter()
    for p in cluster_papers:
        if p.get('year'):
            counter[p['year']] += 1
    return dict(sorted(counter.items()))


def cluster_top_researchers(cluster_papers, top_n: int = 15) -> list:
    """Return top researchers in a cluster by paper count."""
    counter = Counter()
    fwci_sum = defaultdict(list)
    for p in cluster_papers:
        for a in p.get('authors', []):
            counter[a] += 1
            if p.get('fwci') is not None:
                fwci_sum[a].append(p['fwci'])
    result = []
    for author, count in counter.most_common(top_n):
        fwci_vals = fwci_sum[author]
        result.append({
            'author': author,
            'papers': count,
            'avg_fwci': sum(fwci_vals) / len(fwci_vals) if fwci_vals else None,
        })
    return result