"""Step 4 stage 5 — retrieval arms at the locked geometry on the cuad instrument.

Same race as benchmarks/sweep5_retrieval_uwazi.py (PLAN.md Step 4c Stage 5
pre-statement: one store cell × {embedding, bm25, rrf}) on the finalist
long-doc home (merge-2400, embeddinggemma Stage-4 store, reuse) — the
biggest corpus of the race (13,459 chunks, 4,046 golden rows): the home
where bm25's index build and rrf's double ranking cost the most. Scoring
only; let the bm25 arm take its minutes.

Run: `./.venv/bin/uwazi-rag benchmark --spec benchmarks/sweep5_retrieval_cuad.py`
"""

from uwazi_rag.use_cases.chunking_methods import MergeChunker
from uwazi_rag.use_cases.retrieval_methods import Bm25Retrieval, EmbeddingRetrieval, RrfRetrieval
from uwazi_rag.use_cases.run_sweep import StoreCell, define_sweep

dataset = "legalbenchrag-cuad"

CELLS = [
    StoreCell(label="merge-2400-embeddinggemma", chunk_method=MergeChunker(max_chars=2400), model="embeddinggemma"),
]
ARMS = [EmbeddingRetrieval(), Bm25Retrieval(), RrfRetrieval()]

experiments = define_sweep(CELLS, ARMS)
