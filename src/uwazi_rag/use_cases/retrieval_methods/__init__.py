"""Retrieval-method families (Step 3.5): one class per method, settings on the constructor.

A method turns a prepared golden run into ``{row_id: [Hit]}`` rankings through the
shared ranking path (:mod:`uwazi_rag.use_cases.eval_run`), so sweep numbers equal
``eval`` numbers by construction. The uniform ``Hit`` output keeps every method
gradeable by :func:`uwazi_rag.use_cases.eval_retrieval.score_rows`; only
cosine-calibrated methods may report false-retrieval (``cosine_calibrated``).

Instances are self-describing — ``name``, ``params()`` and ``describe()`` —
which is what lets sweep results record exactly what was graded, with no
per-method spec vocabulary.
"""

from uwazi_rag.use_cases.retrieval_methods.base import RetrievalMethod
from uwazi_rag.use_cases.retrieval_methods.bm25 import Bm25Index, Bm25Retrieval, tokenize
from uwazi_rag.use_cases.retrieval_methods.embedding import EmbeddingRetrieval
from uwazi_rag.use_cases.retrieval_methods.rrf import RRF_K, RrfRetrieval, fused_ranking, rrf_scores

__all__ = [
    "RRF_K",
    "Bm25Index",
    "Bm25Retrieval",
    "EmbeddingRetrieval",
    "RetrievalMethod",
    "RrfRetrieval",
    "fused_ranking",
    "rrf_scores",
    "tokenize",
]
