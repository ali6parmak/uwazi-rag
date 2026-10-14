"""Step 4 stage 5 — retrieval arms at the locked geometry on the vic-chargebook instrument.

Same race as benchmarks/sweep5_retrieval_uwazi.py (PLAN.md Step 4c Stage 5
pre-statement: one store cell × {embedding, bm25, rrf}) on the pre-chunked
passthrough home (4096/on, embeddinggemma Stage-4 build, reuse) — the
deliberately lexically-dissimilar instrument: the honest case for checking
whether bm25 hurts fusion instead of helping it. Currencies collapse to
hit-rate/MRR by design. Scoring only.

Run: `./.venv/bin/uwazi-rag benchmark --spec benchmarks/sweep5_retrieval_vic.py`
"""

from uwazi_rag.use_cases.chunking_methods import PassThroughChunker
from uwazi_rag.use_cases.retrieval_methods import Bm25Retrieval, EmbeddingRetrieval, RrfRetrieval
from uwazi_rag.use_cases.run_sweep import StoreCell, define_sweep

dataset = "vic-chargebook"

CELLS = [
    StoreCell(label="passthrough-4096-embeddinggemma", chunk_method=PassThroughChunker(), model="embeddinggemma"),
]
ARMS = [EmbeddingRetrieval(), Bm25Retrieval(), RrfRetrieval()]

experiments = define_sweep(CELLS, ARMS)
