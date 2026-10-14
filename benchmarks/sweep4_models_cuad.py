"""Step 4 stage 4 — model re-race at the locked geometry on the cuad instrument.

The locked leader geometry merge-2400 (Stage 2 recorded embeddinggemma its
winner home). The three Stage-2 shortlist models reuse the sweep33 incumbent
stores (same slugs); qwen3-embedding:8b (4,096 dims) builds fresh — expect
the slow, large build of this race after maud (~13.4k chunks at 4,096 dims).

Run: `./.venv/bin/uwazi-rag benchmark --spec benchmarks/sweep4_models_cuad.py`
"""

from uwazi_rag.use_cases.chunking_methods import MergeChunker
from uwazi_rag.use_cases.retrieval_methods import EmbeddingRetrieval
from uwazi_rag.use_cases.run_sweep import StoreCell, define_sweep

dataset = "legalbenchrag-cuad"

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
