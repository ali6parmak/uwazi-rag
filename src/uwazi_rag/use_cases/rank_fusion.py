"""Re-export shim: RRF moved to :mod:`uwazi_rag.use_cases.retrieval_methods.rrf`.

Kept so the shared grading path's imports (``eval_run``) and existing tests
stay untouched; new code should import from the retrieval_methods package.
"""

from uwazi_rag.use_cases.retrieval_methods.rrf import RRF_K, fused_ranking, rrf_scores

__all__ = ["RRF_K", "fused_ranking", "rrf_scores"]
