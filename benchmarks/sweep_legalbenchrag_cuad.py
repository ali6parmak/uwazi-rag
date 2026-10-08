"""Step 4a sweep — the legalbenchrag-cuad instrument (CUAD contract exhibits).

462 SEC-filing contract documents (to 338 KB), 4,042 expert questions, 6,247
gold spans (CC BY 4.0) — the heavy long-document pressure source: recorded
baseline doc R@1 98.7% against chunk R@1 7.7%, the split the merge-2400 cell
was declared to probe. The bge-m3 baseline store is recorded and reused; the
MODEL RACE holds the two informative geometries (baseline, merge-2400) and
crosses them with the 8-model roster — ~16,000 chunks per baseline cell, so
the qwen3-8b cells (4096-dim) are the run's heaviest. Dimensions measured
2026-10-07: bge-m3 1024, qwen3-embedding 1024 (:8b 4096), nomic-v2-moe 768,
embeddinggemma 768, granite-embedding 384, snowflake-arctic-embed2 1024,
mxbai-embed-large 1024.
"""

from uwazi_rag.use_cases.chunking_methods import MergeChunker
from uwazi_rag.use_cases.retrieval_methods import EmbeddingRetrieval
from uwazi_rag.use_cases.run_sweep import StoreCell, define_sweep

dataset = "legalbenchrag-cuad"

MODEL_TAGS = [
    "bge-m3",
    "qwen3-embedding:8b",
    "nomic-embed-text-v2-moe",
    "embeddinggemma",
    "granite-embedding",
    "snowflake-arctic-embed2",
    "mxbai-embed-large",
]
GEOMETRY = [
    ("baseline", MergeChunker()),
    ("merge-2400", MergeChunker(max_chars=2400)),
]

experiments = define_sweep(
    [
        StoreCell(label=f"{geo}-{tag.replace(':', '-')}", chunk_method=chunker, model=tag)
        for tag in MODEL_TAGS
        for geo, chunker in GEOMETRY
    ],
    [EmbeddingRetrieval()],
)
