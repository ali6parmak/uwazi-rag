"""Step 4 stage 4 — model re-race at the locked geometry on the contractnli instrument.

The locked leader geometry merge-1200 (Stage 2 recorded embeddinggemma its
winner home). The three Stage-2 shortlist models reuse the sweep33 incumbent
stores (same slugs); qwen3-embedding:8b (4,096 dims) builds fresh. Its 5
unanswerable rows are already on the threshold ruler (bge max 0.5987, gemma
0.6348, snowflake 0.5421 — the 2026-10-14 derivation block).

Run: `./.venv/bin/uwazi-rag benchmark --spec benchmarks/sweep4_models_contractnli.py`
"""

from uwazi_rag.use_cases.chunking_methods import MergeChunker
from uwazi_rag.use_cases.retrieval_methods import EmbeddingRetrieval
from uwazi_rag.use_cases.run_sweep import StoreCell, define_sweep

dataset = "legalbenchrag-contractnli"

MODELS = [
    "bge-m3",
    "embeddinggemma",
    "snowflake-arctic-embed2",
    "qwen3-embedding:8b",
]
ARMS = [
    ("merge-1200", MergeChunker(max_chars=1200)),
]

experiments = define_sweep(
    [
        StoreCell(label=f"{geo}-{tag.replace(':', '-')}", chunk_method=chunker, model=tag)
        for tag in MODELS
        for geo, chunker in ARMS
    ],
    [EmbeddingRetrieval()],
)
