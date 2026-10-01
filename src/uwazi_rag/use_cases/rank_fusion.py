"""Reciprocal rank fusion — the rank-based half of the hybrid preview (Step 3.5).

Fusions of ranked id lists are scale-free: ``weight × 1/(k + rank)`` sums
combine an embedding cosine ranking and a BM25 score ranking without any
calibration of their very different score scales. ``k = 60`` is the classic
default; ties break by first appearance across the rankings in fusion order,
so the same input always yields the same ranking.
"""

from __future__ import annotations

from collections.abc import Sequence

RRF_K = 60


def rrf_scores(
    rankings: Sequence[Sequence[str]], *, k: int = RRF_K, weights: Sequence[float] | None = None
) -> dict[str, float]:
    """Accumulated 1/(k + rank) per id across all rankings (weighted, rank is 1-based)."""
    if k < 1:
        raise ValueError(f"k must be >= 1, got {k}")
    if weights is None:
        weights = [1.0] * len(rankings)
    if len(weights) != len(rankings):
        raise ValueError(f"{len(weights)} weights for {len(rankings)} rankings — counts must match")
    if any(weight < 0.0 for weight in weights):
        raise ValueError(f"weights must be >= 0, got {weights}")
    scores: dict[str, float] = {}
    for ranking, weight in zip(rankings, weights, strict=True):
        for rank, doc_id in enumerate(ranking, start=1):
            scores[doc_id] = scores.get(doc_id, 0.0) + weight / (k + rank)
    return scores


def fused_ranking(rankings: Sequence[Sequence[str]], *, k: int = RRF_K, weights: Sequence[float] | None = None) -> list[str]:
    """Ids ranked by accumulated RRF score; ties break by first appearance (deterministic)."""
    scores = rrf_scores(rankings, k=k, weights=weights)
    first_seen: dict[str, int] = {}
    position = 0
    for ranking in rankings:
        for doc_id in ranking:
            if doc_id not in first_seen:
                first_seen[doc_id] = position
            position += 1
    return sorted(scores, key=lambda doc_id: (-scores[doc_id], first_seen[doc_id]))
