"""Step 4 stage 5 — retrieval arms at the locked geometry on the maud instrument.

Same race as benchmarks/sweep5_retrieval_uwazi.py (PLAN.md Step 4c Stage 5
pre-statement: one store cell × {embedding, bm25, rrf}) on the monster
long-doc home (merge-2400, embeddinggemma Stage-4 store, reuse) — 28,860
chunks over 1,676 golden rows; bge-m3's recorded Stage-4 home. The bm25 arm
indexes the whole store lexically; expect the slowest scoring of the stage.
Scoring only.

Run: `./.venv/bin/uwazi-rag benchmark --spec benchmarks/sweep5_retrieval_maud.py`
"""

from uwazi_rag.use_cases.chunking_methods import MergeChunker
from uwazi_rag.use_cases.retrieval_methods import Bm25Retrieval, EmbeddingRetrieval, RrfRetrieval
from uwazi_rag.use_cases.run_sweep import StoreCell, define_sweep

dataset = "legalbenchrag-maud"

CELLS = [
    StoreCell(label="merge-2400-embeddinggemma", chunk_method=MergeChunker(max_chars=2400), model="embeddinggemma"),
]
ARMS = [EmbeddingRetrieval(), Bm25Retrieval(), RrfRetrieval()]

experiments = define_sweep(CELLS, ARMS)
