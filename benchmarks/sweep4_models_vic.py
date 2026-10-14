"""Step 4 stage 4 — model re-race at the locked geometry on the vic-chargebook instrument.

The locked config passthrough-4096 (header on) — pre-chunked corpus, the
pass-through method makes each of the 4,876 upstream passages ONE chunk, so
currencies collapse to hit-rate/MRR by design and geometry has nothing to
turn; the model axis is the only live one (Stage 2 recorded snowflake the
vic winner). No incumbent store exists under the current slugs, so all four
model cells build fresh (cheap builds). Its 4 unanswerable golden rows are
new to the threshold ruler (coverage goes 16/25 → 20/25 here; privacyqa
completes it at 25/25).

Run: `./.venv/bin/uwazi-rag benchmark --spec benchmarks/sweep4_models_vic.py`
"""

from uwazi_rag.use_cases.chunking_methods import PassThroughChunker
from uwazi_rag.use_cases.retrieval_methods import EmbeddingRetrieval
from uwazi_rag.use_cases.run_sweep import StoreCell, define_sweep

dataset = "vic-chargebook"

MODELS = [
    "bge-m3",
    "embeddinggemma",
    "snowflake-arctic-embed2",
    "qwen3-embedding:8b",
]
ARMS = [
    ("passthrough-4096", PassThroughChunker()),
]

experiments = define_sweep(
    [
        StoreCell(label=f"{geo}-{tag.replace(':', '-')}", chunk_method=chunker, model=tag)
        for tag in MODELS
        for geo, chunker in ARMS
    ],
    [EmbeddingRetrieval()],
)
