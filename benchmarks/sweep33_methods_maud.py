"""Step 4c wave 3.3 — rung 2 on the winner (merge) on the maud finalist.

Same race as benchmarks/sweep33_methods_cuad.py (PLAN.md wave-3.3
pre-statement, user call 2026-10-13: ALL FOUR homes in one wave, readout =
ONE combined 3.3 verdict): arms {merge-2400 (reuse), merge-sent-2400,
merge-crumb-2400, merge-sent-crumb-2400} × the 3 shortlisted models.

maud is the monster home — the one whose rung-2 readout matters most: 7,454
paragraphs exceed the 2400 budget (52.1% of text mass, max 10,926), so the
sentence-boundary layer attacks the exact mechanism that made section-split
worth pricing in wave 3.2 (merge's own monster-piece quality → cov@3000 /
chunk R@1). Headings: 100% regex-headed docs — full crumb coverage; LBR
captures carry no page numbers, so the crumb line ends at the heading text.

4 arms × 3 models = 12 cells; 3 merge-2400 reuses + 9 new builds.
privacyqa stays out by pre-statement. Run: `uv run uwazi-rag benchmark
--spec benchmarks/sweep33_methods_maud.py`
"""

from uwazi_rag.use_cases.chunking_methods import MergeChunker
from uwazi_rag.use_cases.retrieval_methods import EmbeddingRetrieval
from uwazi_rag.use_cases.run_sweep import StoreCell, define_sweep

dataset = "legalbenchrag-maud"

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
