"""Step 4c wave 3.3 — rung 2 on the winner (merge) on the Uwazi golden (small instrument).

The Stage-3 verdict (results.md, 2026-10-13, decision commit-pending) locked merge;
rung 2 changes it ONE layer at a time (PLAN.md wave-3.3 pre-statement):

- merge-sent-1200: monster (over-budget paragraph) cuts prefer sentence ends
  (`.!?` + whitespace in the same ~0.8-budget cut window); no sentence end →
  the exact legacy word cut; overlap 0.15 still governs the shared band.
- merge-crumb-1200: every chunk's context header swap — "{title} — {heading
  line} (page n)" instead of "{title} — {template} (page n)" when the chunk's
  first paragraph sits in a heading section (preamble chunks keep today's
  header); a text-assembly layer, not counted against the budget, ids/packing
  unchanged.
- merge-sent-crumb-1200: both layers together (the interaction cell).

Arms × the 3 shortlisted models = 12 cells; the merge-1200 stores exist (same
slug) from sweep2_models/sweep31 and are reused — 9 new builds. Fixture facts:
378 monsters @1200 (14.9% of text mass) for the sentence lens; 1,134 typed
headings across 74/77 docs for the crumb lens.

privacyqa is skipped by pre-statement (largest paragraph 1,064 < 2400 — no
monster cuts to improve; 6/7 of its docs byte-equal fallback — the crumb is a
near-no-op there).

Run: `uv run uwazi-rag benchmark --spec benchmarks/sweep33_methods_uwazi.py`
"""

from uwazi_rag.use_cases.chunking_methods import MergeChunker
from uwazi_rag.use_cases.retrieval_methods import EmbeddingRetrieval
from uwazi_rag.use_cases.run_sweep import StoreCell, define_sweep

MODELS = [
    "bge-m3",
    "embeddinggemma",
    "snowflake-arctic-embed2",
]
ARMS = [
    ("merge-1200", MergeChunker(max_chars=1200)),
    ("merge-sent-1200", MergeChunker(max_chars=1200, sentence_cuts=True)),
    ("merge-crumb-1200", MergeChunker(max_chars=1200, breadcrumb=True)),
    ("merge-sent-crumb-1200", MergeChunker(max_chars=1200, sentence_cuts=True, breadcrumb=True)),
]

experiments = define_sweep(
    [
        StoreCell(label=f"{geo}-{tag.replace(':', '-')}", chunk_method=chunker, model=tag)
        for tag in MODELS
        for geo, chunker in ARMS
    ],
    [EmbeddingRetrieval()],
)
