"""Tests for cluster detection."""
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).parent.parent / 'scripts'
sys.path.insert(0, str(SCRIPT_DIR))

from clusters import (  # noqa
    detect_ai_cluster,
    detect_materials_cluster,
    detect_life_sciences_cluster,
    detect_phys_sci_cluster,
    detect_cs_ai_cluster,
    cluster_summary,
    cluster_yearly_stats,
    cluster_top_researchers,
    AI_SURNAMES,
)


def sample_papers():
    return [
        {'title': 'P1', 'authors': ['Wang, Y.', 'Li, J.'], 'fields': ['Computer Science'], 'fwci': 3.5, 'citations': 50, 'year': 2023},
        {'title': 'P2', 'authors': ['Smith, J.', 'Doe, A.'], 'fields': ['Biology'], 'fwci': 1.2, 'citations': 20, 'year': 2024},
        {'title': 'P3', 'authors': ['Zhang, T.', 'Brown, K.'], 'fields': ['Materials Science'], 'fwci': 4.0, 'citations': 100, 'year': 2024},
        {'title': 'P4', 'authors': ['Chen, M.', 'Garcia, R.'], 'fields': ['Oncology', 'Medicine'], 'fwci': 2.5, 'citations': 75, 'year': 2023},
    ]


def test_ai_cluster_chinese_surname_match():
    papers = sample_papers()
    cluster = detect_ai_cluster(papers)
    titles = [p['title'] for p in cluster]
    assert 'P1' in titles  # Wang, Li
    assert 'P3' in titles  # Zhang
    assert 'P4' in titles  # Chen
    assert 'P2' not in titles  # only Smith, Doe


def test_materials_cluster():
    papers = sample_papers()
    cluster = detect_materials_cluster(papers)
    titles = [p['title'] for p in cluster]
    assert 'P3' in titles  # Materials Science field
    assert 'P1' not in titles  # CS only


def test_life_sciences_cluster():
    papers = sample_papers()
    cluster = detect_life_sciences_cluster(papers)
    titles = [p['title'] for p in cluster]
    assert 'P2' in titles  # Biology
    assert 'P4' in titles  # Oncology + Medicine


def test_phys_sci_cluster():
    papers = sample_papers()
    cluster = detect_phys_sci_cluster(papers)
    titles = [p['title'] for p in cluster]
    # Sample papers don't have phys-sci fields; verify detection logic instead
    test_papers = [
        {'title': 'P1', 'authors': [], 'fields': ['Physics'], 'fwci': 1.0, 'year': 2023, 'citations': 5},
    ]
    cluster2 = detect_phys_sci_cluster(test_papers)
    assert len(cluster2) == 1
    # Also test materials cluster (separate from phys_sci)
    mat_cluster = detect_materials_cluster(test_papers)
    assert 'P1' not in [p['title'] for p in mat_cluster]  # not materials


def test_cs_ai_cluster():
    papers = sample_papers()
    cluster = detect_cs_ai_cluster(papers)
    titles = [p['title'] for p in cluster]
    assert 'P1' in titles  # Computer Science


def test_cluster_summary():
    papers = sample_papers()
    summary = cluster_summary(detect_ai_cluster(papers), papers)
    assert summary['size'] == 3
    assert summary['share_of_total'] == 75.0
    assert summary['avg_fwci'] is not None
    assert summary['avg_fwci'] > 0


def test_cluster_yearly_stats():
    papers = sample_papers()
    yearly = cluster_yearly_stats(detect_ai_cluster(papers))
    assert 2023 in yearly
    assert 2024 in yearly
    assert yearly[2023] == 2  # P1 + P4 in 2023
    assert yearly[2024] == 1  # P3 in 2024


def test_cluster_top_researchers():
    papers = sample_papers()
    top = cluster_top_researchers(detect_ai_cluster(papers), top_n=5)
    assert len(top) > 0
    assert all('author' in r and 'papers' in r and 'avg_fwci' in r for r in top)


def test_ai_surnames_list():
    """Verify AI surname list contains expected names."""
    assert 'Wang' in AI_SURNAMES
    assert 'Li' in AI_SURNAMES
    assert 'Zhang' in AI_SURNAMES
    assert len(AI_SURNAMES) >= 10


def test_empty_input():
    assert detect_ai_cluster([]) == []
    assert detect_materials_cluster([]) == []
    assert cluster_summary([], [])['size'] == 0