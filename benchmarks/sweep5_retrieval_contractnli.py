"""Step 4 stage 5 — retrieval arms at the locked geometry on the contractnli instrument.

Same race as benchmarks/sweep5_retrieval_uwazi.py (PLAN.md Step 4c Stage 5
pre-statement: one store cell × {embedding, bm25, rrf}) on the instrument
where embeddinggemma is the Stage-4 home winner (merge-1200, reuse) — the
clause-language home where lexical probes (section numbers, defined terms)
should favor bm25 if they favor anything. Scoring only.

Run: `./.venv/bin/uwazi-rag benchmark --spec benchmarks/sweep5_retrieval_contractnli.py`
"""

from uwazi_rag.use_cases.chunking_methods import MergeChunker
from uwazi_rag.use_cases.retrieval_methods import Bm25Retrieval, EmbeddingRetrieval, RrfRetrieval
from uwazi_rag.use_cases.run_sweep import StoreCell, define_sweep

dataset = "legalbenchrag-contractnli"

CELLS = [
    StoreCell(label="merge-1200-embeddinggemma", chunk_method=MergeChunker(max_chars=1200), model="embeddinggemma"),
]
ARMS = [EmbeddingRetrieval(), Bm25Retrieval(), RrfRetrieval()]

experiments = define_sweep(CELLS, ARMS)
