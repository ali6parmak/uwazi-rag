"""Reciprocal rank fusion — the rank-based half of the hybrid preview (Step 3.5).

Fusions of ranked id lists are scale-free: ``weight × 1/(k + rank)`` sums
combine an embedding cosine ranking and a BM25 score ranking without any
calibration of their very different score scales. ``k = 60`` is the classic
default; ties break by first appearance across the rankings in fusion order,
so the same input always yields the same ranking.

:class:`RrfRetrieval` is the method instance: its arms are the shared grading
path's embedding + BM25 rankings (deferred import — eval_run imports this
package's primitives), fused with the instance's own ``k``/``weights``.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

from uwazi_rag.use_cases.eval_retrieval import RETRIEVAL_DEPTH, DocKey, Hit
from uwazi_rag.use_cases.retrieval_methods.base import RetrievalMethod

if TYPE_CHECKING:
    from uwazi_rag.ports.embedding_port import EmbeddingPort
    from uwazi_rag.use_cases.eval_run import PreparedRun

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


class RrfRetrieval(RetrievalMethod):
    """Reciprocal-rank fusion of the embedding + BM25 rankings for every golden row.

    Rank-based fusion is scale-free; ``k`` and the two per-arm ``weights``
    (embedding arm first, BM25 arm second) are constructor params. The default
    instance (k=60, equal weights) is exactly ``rank_rows(retrieval="rrf")``
    on the shared path. Fused top-1 scores are 1/(k+rank) sums, not cosine,
    so this method is not cosine-calibrated: false-retrieval is not measured.
    """

    def __init__(self, *, k: int = RRF_K, weights: Sequence[float] = (1.0, 1.0)) -> None:
        if k < 1:
            raise ValueError(f"k must be >= 1, got {k}")
        weights = tuple(weights)
        if len(weights) != 2:  # the arms are fixed: [embedding, bm25]
            raise ValueError(f"rrf fuses exactly two arms — got {len(weights)} weights")
        if any(weight < 0.0 for weight in weights):
            raise ValueError(f"weights must be >= 0, got {weights}")
        self.k = k
        self.weights: tuple[float, ...] = weights

    @property
    def name(self) -> str:
        return "rrf"

    def params(self) -> dict[str, Any]:
        return {"k": self.k, "weights": list(self.weights)}

    def describe(self) -> str:
        return f"rrf k={self.k} w=" + "/".join(str(weight) for weight in self.weights)

    def rank(self, prepared: PreparedRun, *, embedder: EmbeddingPort | None = None) -> dict[str, list[Hit]]:
        """Fuse the shared path's embedding ranking with its BM25 ranking, per row."""
        if embedder is None:
            raise ValueError("retrieval 'rrf' needs an embedder — build one for the store's model")
        # Deferred import: eval_run imports this package's primitive modules.
        from uwazi_rag.use_cases.eval_run import rank_rows

        embed_hits = rank_rows(prepared, retrieval="embedding", embedder=embedder)
        bm25_hits = rank_rows(prepared, retrieval="bm25")
        doc_keys: dict[str, DocKey] = {
            chunk.chunk_id: (chunk.instance_key, chunk.shared_id, chunk.language) for chunk in prepared.store.chunks()
        }
        fused: dict[str, list[Hit]] = {}
        for row in prepared.rows:
            row_id = str(row["id"])
            rankings = [
                [hit.chunk_id for hit in embed_hits.get(row_id, ())],
                [hit.chunk_id for hit in bm25_hits.get(row_id, ())],
            ]
            scores = rrf_scores(rankings, k=self.k, weights=self.weights)
            fused[row_id] = [
                Hit(chunk_id=chunk_id, doc_key=doc_keys[chunk_id], score=scores[chunk_id])
                for chunk_id in fused_ranking(rankings, k=self.k, weights=self.weights)[:RETRIEVAL_DEPTH]
            ]
        return fused
