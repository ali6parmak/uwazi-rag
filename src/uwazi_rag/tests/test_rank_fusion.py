"""Reciprocal-rank fusion tests: exact hand-computed 1/(k + rank) sums.

Fully offline (AGENTS.md testing policy), plain assertions. With k = 60:
position 1 contributes 1/61 ≈ 0.01639344, position 2 → 1/62, position 3 → 1/63.
"""

from __future__ import annotations

import pytest

from uwazi_rag.use_cases.rank_fusion import fused_ranking, rrf_scores

RANKING_A = ["a", "b", "c"]
RANKING_B = ["b", "c"]


def test_rrf_scores_sum_exact_reciprocals() -> None:
    scores = rrf_scores([RANKING_A, RANKING_B])
    assert scores["a"] == pytest.approx(1 / 61, rel=1e-9)
    assert scores["b"] == pytest.approx(1 / 62 + 1 / 61, rel=1e-9)
    assert scores["c"] == pytest.approx(1 / 63 + 1 / 62, rel=1e-9)
    # 1/62 + 1/61 > 1/63 + 1/62 → b and c beat a, in that order
    assert fused_ranking([RANKING_A, RANKING_B]) == ["b", "c", "a"]


def test_weights_reweight_each_ranking() -> None:
    scores = rrf_scores([RANKING_A, RANKING_B], weights=[2.0, 1.0])
    assert scores["a"] == pytest.approx(2 / 61, rel=1e-9)
    assert scores["b"] == pytest.approx(2 / 62 + 1 / 61, rel=1e-9)
    assert scores["c"] == pytest.approx(2 / 63 + 1 / 62, rel=1e-9)


def test_zero_weight_ranking_contributes_nothing() -> None:
    scores = rrf_scores([RANKING_A, RANKING_B], weights=[0.0, 1.0])
    assert scores["a"] == pytest.approx(0.0, abs=1e-12)
    assert scores["b"] == pytest.approx(1 / 61, rel=1e-9)
    assert fused_ranking([RANKING_A, RANKING_B], weights=[0.0, 1.0]) == ["b", "c", "a"]


def test_ties_break_by_first_appearance_across_rankings() -> None:
    # "x" and "y" both score exactly 1/(k+1): x is seen first → ranked first.
    rankings = [["x", "y"], ["y", "x"]]
    scores = rrf_scores(rankings)
    assert scores["x"] == pytest.approx(scores["y"], rel=1e-9)
    assert fused_ranking(rankings) == ["x", "y"]


def test_fusion_is_deterministic_and_rrf_k_is_the_default() -> None:
    rankings = [[f"d{index:03d}" for index in range(50)], [f"d{index:03d}" for index in range(20, 40)]]
    assert fused_ranking(rankings) == fused_ranking(rankings)
    # d020 tops the fusion (pos 1 of ranking B plus deep in ranking A beats any single hit)
    assert fused_ranking(rankings)[0] == "d020"
    assert fused_ranking([rankings[0]])[0] == "d000"


def test_rrf_validates_inputs() -> None:
    with pytest.raises(ValueError, match="k"):
        rrf_scores([RANKING_A], k=0)
    with pytest.raises(ValueError, match="weights"):
        rrf_scores([RANKING_A, RANKING_A], weights=[1.0])
    with pytest.raises(ValueError, match="weights"):
        rrf_scores([RANKING_A], weights=[-1.0])
