"""Step 4 stage 4 — model re-race at the locked geometry on the live Uwazi home.

PLAN.md Step 4c Stage 4 (pre-stated 2026-10-14): the method axis is frozen
(the lock: merge, header on, overlap 0.15); this race re-prices the model
axis on it. Four models × the one locked cell per model — the three Stage-2
shortlist models reuse the sweep33 incumbent stores (same slugs), and
qwen3-embedding:8b (4,096 dims, re-checked after Step 3.5's 1800-geometry
race) builds fresh. This home is the production default path by the lock
(INDEX_MAX_CHARS = 1200) — its verdict weighs first.

False-retr is read in BOTH views per the threshold-derivation block
(2026-10-14): the common-0.55 hit counts and each model's per-row
unanswerable top-1s against its proposed cut (qwen's cut derives post-race
from its own block — its only earlier rows came at the old geometry).

Run: `./.venv/bin/uwazi-rag benchmark --spec benchmarks/sweep4_models_uwazi.py`
"""

from uwazi_rag.use_cases.chunking_methods import MergeChunker
from uwazi_rag.use_cases.retrieval_methods import EmbeddingRetrieval
from uwazi_rag.use_cases.run_sweep import StoreCell, define_sweep

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
