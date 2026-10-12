"""Step 4c wave 3.1 — the chunking-method race on the Uwazi golden (small instrument).

Three shortlisted models (user call 2026-10-11: bge-m3, embeddinggemma,
snowflake-arctic-embed2) × three method arms at the recorded uwazi leader
geometry (merge-1200; Stage-2 chunk leaders all ran @1200). The merge-1200
stores already exist from sweep2_models — same slug, so they are reused, not
rebuilt (only the segment/section stores build).

- segment-2400: one DLA segmentation segment per chunk (merge-off); an
  over-long segment still word-splits at ~2400 with overlap 0 — the
  pre-stated method budget, fixed (uwazi-only arm; on the line-partitioned
  dataset captures this degenerates to line-per-chunk).
- section-1200: heading partition (typed Uwazi heading types first), interior
  spans packed at 1200 like the merge competitor; headingless docs fall back
  byte-equal to merge.

False-retr at the single global 0.55 is directional only (the gate tracks the
model, not the geometry). Readout lenses: the Stage-2 headline set + a
chunk-count column. Run: `uv run uwazi-rag benchmark --spec
benchmarks/sweep31_methods_uwazi.py`
"""

from uwazi_rag.use_cases.chunking_methods import MergeChunker, SectionChunker, SegmentChunker
from uwazi_rag.use_cases.retrieval_methods import EmbeddingRetrieval
from uwazi_rag.use_cases.run_sweep import StoreCell, define_sweep

MODELS = [
    "bge-m3",
    "embeddinggemma",
    "snowflake-arctic-embed2",
]
ARMS = [
    ("merge-1200", MergeChunker(max_chars=1200)),
    ("segment-2400", SegmentChunker()),
    ("section-1200", SectionChunker(max_chars=1200)),
]

experiments = define_sweep(
    [
        StoreCell(label=f"{geo}-{tag.replace(':', '-')}", chunk_method=chunker, model=tag)
        for tag in MODELS
        for geo, chunker in ARMS
    ],
    [EmbeddingRetrieval()],
)
