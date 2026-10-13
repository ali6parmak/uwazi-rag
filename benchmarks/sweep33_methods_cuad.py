"""Step 4c wave 3.3 — rung 2 on the winner (merge) on the cuad finalist.

The Stage-3 verdict (results.md, 2026-10-13) locked merge; rung 2 changes it
ONE layer at a time (PLAN.md wave-3.3 pre-statement, user call 2026-10-13:
ALL FOUR homes in one wave — the readout is ONE combined 3.3 verdict block,
per the wave-3.2 precedent):

- merge-2400: the incumbent (merge-2400 stores exist from Stage 2, same slug,
  reused).
- merge-sent-2400: monster (over-budget paragraph) cuts prefer sentence ends
  (`.!?` + whitespace in the same ~0.8-budget cut window); no sentence end in
  the window → the exact legacy word cut; overlap 0.15 still governs; budget
  and packing unchanged. cuad is the middle monster home: 2,039 paragraphs
  over 2400 (26.6% of text mass, max 8,349).
- merge-crumb-2400: every chunk's context header swap — "{title} — {heading
  line}" instead of "{title} — {template}" (no page number on LBR captures)
  when the chunk's first paragraph sits in a heading section; 99.4% of cuad
  docs are regex-headed — full crumb coverage. Text-assembly layer, not
  counted against the budget; ids/packing unchanged.
- merge-sent-crumb-2400: both layers together (the interaction cell).

4 arms × 3 shortlisted models = 12 cells; 3 merge-2400 reuses + 9 new builds.
privacyqa stays out by pre-statement (no monsters; 6/7 byte-equal fallback).
Run: `uv run uwazi-rag benchmark --spec benchmarks/sweep33_methods_cuad.py`
"""

from uwazi_rag.use_cases.chunking_methods import MergeChunker
from uwazi_rag.use_cases.retrieval_methods import EmbeddingRetrieval
from uwazi_rag.use_cases.run_sweep import StoreCell, define_sweep

dataset = "legalbenchrag-cuad"

MODELS = [
    "bge-m3",
    "embeddinggemma",
    "snowflake-arctic-embed2",
]
ARMS = [
    ("merge-2400", MergeChunker(max_chars=2400)),
    ("merge-sent-2400", MergeChunker(max_chars=2400, sentence_cuts=True)),
    ("merge-crumb-2400", MergeChunker(max_chars=2400, breadcrumb=True)),
    ("merge-sent-crumb-2400", MergeChunker(max_chars=2400, sentence_cuts=True, breadcrumb=True)),
]

experiments = define_sweep(
    [
        StoreCell(label=f"{geo}-{tag.replace(':', '-')}", chunk_method=chunker, model=tag)
        for tag in MODELS
        for geo, chunker in ARMS
    ],
    [EmbeddingRetrieval()],
)
