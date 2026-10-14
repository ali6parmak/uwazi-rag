"""Step 4 stage 5 — retrieval arms at the locked geometry on the privacyqa instrument.

Same race as benchmarks/sweep5_retrieval_uwazi.py (PLAN.md Step 4c Stage 5
pre-statement: one store cell × {embedding, bm25, rrf}) on the short-corpus
home where the Stage-4 decider saturated at doc@10 = 100 — the ranking lens
is the only discriminating one here. Store cell = the locked merge-2400
geometry, embeddinggemma (the Stage-4 build, reuse). Scoring only.

Run: `./.venv/bin/uwazi-rag benchmark --spec benchmarks/sweep5_retrieval_privacyqa.py`
"""

from uwazi_rag.use_cases.chunking_methods import MergeChunker
from uwazi_rag.use_cases.retrieval_methods import Bm25Retrieval, EmbeddingRetrieval, RrfRetrieval
from uwazi_rag.use_cases.run_sweep import StoreCell, define_sweep

dataset = "legalbenchrag-privacyqa"

CELLS = [
    StoreCell(label="merge-2400-embeddinggemma", chunk_method=MergeChunker(max_chars=2400), model="embeddinggemma"),
]
ARMS = [EmbeddingRetrieval(), Bm25Retrieval(), RrfRetrieval()]

experiments = define_sweep(CELLS, ARMS)
