"""Step 4c wave 3.1 — the chunking-method race on the contractnli instrument.

Three shortlisted models (user call 2026-10-11) × three method arms at the
recorded leader geometry (merge-1200 — the geometry that led chunk R@1 in the
Step 3.5 sweep and carried the Stage-2 model race). The wave-3.0 scan measured
96.8% of contractnli documents with headings (~21 sections per doc, median 317
chars): this is the densest-heading LBR home, where the section method's
fine-grained partition has the most to prove or to lose.

- section-1200: heading partition, budget packing, headingless docs fall back
  byte-equal to merge; over-long paragraphs stay whole (82 here, 12.7% of
  text mass).
- section-split-1200: the same method word-splitting over-long paragraphs
  (merge-style 0.15 overlap) — the monster handler.

The merge-1200 stores already exist (Stage-2 model race, same slug) and are
reused. Run: `uv run uwazi-rag benchmark --spec
benchmarks/sweep31_methods_contractnli.py`
"""

from uwazi_rag.use_cases.chunking_methods import MergeChunker, SectionChunker, SectionSplitChunker
from uwazi_rag.use_cases.retrieval_methods import EmbeddingRetrieval
from uwazi_rag.use_cases.run_sweep import StoreCell, define_sweep

dataset = "legalbenchrag-contractnli"

MODELS = [
    "bge-m3",
    "embeddinggemma",
    "snowflake-arctic-embed2",
]
ARMS = [
    ("merge-1200", MergeChunker(max_chars=1200)),
    ("section-1200", SectionChunker(max_chars=1200)),
    ("section-split-1200", SectionSplitChunker(max_chars=1200)),
]

experiments = define_sweep(
    [
        StoreCell(label=f"{geo}-{tag.replace(':', '-')}", chunk_method=chunker, model=tag)
        for tag in MODELS
        for geo, chunker in ARMS
    ],
    [EmbeddingRetrieval()],
)
