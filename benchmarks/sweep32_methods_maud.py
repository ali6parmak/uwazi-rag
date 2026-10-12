"""Step 4c wave 3.2 — the chunking-method race on the maud instrument (finalist flagship).

Part of the FULL method grid on the two finalist homes (user call 2026-10-12:
run cuad + maud with every small-race method first, then record ONE combined
3.x verdict over all five homes — no separate wave-3.1 pick). segment stays
OUT by pre-statement: line-partitioned LBR captures are line-per-chunk for it
(72,050 keepable lines on maud) and its value was measured and disqualified on
uwazi (highest P@1 of all arms, collapsed chunk R@1 19.6-22.8%, lowest
cov@3000).

Arms at the recorded maud leader geometry (merge-2400; Stage 2: bge-m3 is the
doc-lens leader 94.6% @1 / 99.0% @10): merge-2400, section-2400 and
section-split-2400 - 3 arms x 3 shortlisted models = 9 cells. The merge-2400
stores exist for all three models from the Stage-2 dataset race (same slug)
and are reused - 6 new builds (the section-split-2400 build is the big one).

This is THE monster home: 7,454 paragraphs exceed the 2,400 budget (52.1% of
the text mass, max 10,926 chars) - plain section carries each whole (the
wave-0 scan's 7,454 over-budget section chunks), so the section-vs-
section-split deltas here decide the monster question for the lock.
Wave-0 facts: 150 docs; section partition median 2,071 chars, p95 12,896.

Run: `uv run uwazi-rag benchmark --spec benchmarks/sweep32_methods_maud.py`
"""

from uwazi_rag.use_cases.chunking_methods import MergeChunker, SectionChunker, SectionSplitChunker
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
    ("section-2400", SectionChunker(max_chars=2400)),
    ("section-split-2400", SectionSplitChunker(max_chars=2400)),
]

experiments = define_sweep(
    [
        StoreCell(label=f"{geo}-{tag.replace(':', '-')}", chunk_method=chunker, model=tag)
        for tag in MODELS
        for geo, chunker in ARMS
    ],
    [EmbeddingRetrieval()],
)
