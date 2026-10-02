"""Embedding-cosine retrieval — rank golden questions by meaning (Step 3.5 default).

The instance carries no settings of its own: the model/dimensions come from
the store (and the embedder built for the store's model), which is exactly the
guard :func:`uwazi_rag.use_cases.eval_run.rank_rows` enforces. This method is
the cosine-calibrated one — it is the only family whose top-1 scores may be
checked against a false-retrieval threshold.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from uwazi_rag.ports.embedding_port import EmbeddingPort
from uwazi_rag.use_cases.eval_retrieval import Hit
from uwazi_rag.use_cases.retrieval_methods.base import RetrievalMethod

if TYPE_CHECKING:
    from uwazi_rag.use_cases.eval_run import PreparedRun


class EmbeddingRetrieval(RetrievalMethod):
    """Cosine over the store's own embedding space (the committed method-comparison winner).

    Ranking is delegated to the shared path (``rank_rows(retrieval="embedding")``)
    — one implementation, zero drift; the equivalence test pins it.
    """

    cosine_calibrated = True

    @property
    def name(self) -> str:
        return "embedding"

    def rank(self, prepared: PreparedRun, *, embedder: EmbeddingPort | None = None) -> dict[str, list[Hit]]:
        # Deferred import: eval_run imports this package's primitive modules, so
        # importing it while this package loads would be a circular import.
        from uwazi_rag.use_cases.eval_run import rank_rows

        return rank_rows(prepared, retrieval="embedding", embedder=embedder)
