"""Step 4 stage 4 — model re-race at the locked geometry on the privacyqa instrument.

The locked leader geometry merge-2400 (Stage 2 recorded bge-m3 its winner
home). No incumbent merge store exists under the current slugs — the Stage-2
dataset stores predate the readable-store rename — so `_ensure_store` builds
all four model cells fresh; the three shortlist models should land
bit-identical to their recorded sweep31 numbers (embeddings are
bit-stable across builds, verified in waves 3.3/3.4).

This home also completes the threshold ruler: its 5 unanswerable golden rows
have never been measured — the block carries their top-1s per model.

Run: `./.venv/bin/uwazi-rag benchmark --spec benchmarks/sweep4_models_privacyqa.py`
"""

from uwazi_rag.use_cases.chunking_methods import MergeChunker
from uwazi_rag.use_cases.retrieval_methods import EmbeddingRetrieval
from uwazi_rag.use_cases.run_sweep import StoreCell, define_sweep

dataset = "legalbenchrag-privacyqa"

MODELS = [
    "bge-m3",
    "embeddinggemma",
    "snowflake-arctic-embed2",
    "qwen3-embedding:8b",
]
ARMS = [
    ("merge-2400", MergeChunker(max_chars=2400)),
]

experiments = define_sweep(
    [
        StoreCell(label=f"{geo}-{tag.replace(':', '-')}", chunk_method=chunker, model=tag)
        for tag in MODELS
        for geo, chunker in ARMS
    ],
    [EmbeddingRetrieval()],
)
