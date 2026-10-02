"""Re-export shim: BM25 moved to :mod:`uwazi_rag.use_cases.retrieval_methods.bm25`.

Kept so the shared grading path's imports (``eval_run``) and existing tests
stay untouched; new code should import from the retrieval_methods package.
"""

from uwazi_rag.use_cases.retrieval_methods.bm25 import Bm25Index, tokenize

__all__ = ["Bm25Index", "tokenize"]
