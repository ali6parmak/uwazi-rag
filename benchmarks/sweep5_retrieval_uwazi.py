"""Step 4 stage 5 — retrieval arms at the locked geometry on the live Uwazi home.

PLAN.md Step 4c Stage 5 (pre-stated 2026-10-14): the last retrieval-axis
question before Step 5 — does lexical (bm25) or rank-fused (rrf) retrieval
beat semantic-only at the locked chunking? One store cell — the locked
merge-1200 geometry at the Stage-4 production default model embeddinggemma
(the sweep33 store, reuse) — × three arms: embedding (cosine-calibrated
incumbent), bm25 k1=1.2 b=0.75, rrf k=60 w=1/1. Scoring only: no builds, no
new embeddings beyond the embedding arm's query embeds. This home decides
first — it is the production default path.

False-retr is measured ONLY on the embedding arm (bm25/rrf are not
cosine-calibrated — recorded unmeasured, never guessed; the hybrid
answer-gate is a Step-6 design question).

Run: `./.venv/bin/uwazi-rag benchmark --spec benchmarks/sweep5_retrieval_uwazi.py`
"""

from uwazi_rag.use_cases.chunking_methods import MergeChunker
from uwazi_rag.use_cases.retrieval_methods import Bm25Retrieval, EmbeddingRetrieval, RrfRetrieval
from uwazi_rag.use_cases.run_sweep import StoreCell, define_sweep

CELLS = [
    StoreCell(label="merge-1200-embeddinggemma", chunk_method=MergeChunker(max_chars=1200), model="embeddinggemma"),
]
ARMS = [EmbeddingRetrieval(), Bm25Retrieval(), RrfRetrieval()]

experiments = define_sweep(CELLS, ARMS)
