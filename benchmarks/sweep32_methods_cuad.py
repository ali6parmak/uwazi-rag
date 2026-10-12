"""Step 4c wave 3.2 — the chunking-method race on the cuad instrument (finalist).

Part of the FULL method grid on the two finalist homes (user call 2026-10-12:
run cuad + maud with every small-race method first, then record ONE combined
3.x verdict over all five homes — no separate wave-3.1 pick). segment stays
OUT by pre-statement: cuad/maud are line-partitioned LBR captures, so segment
mode is line-per-chunk there (~71k-line stores on cuad) and its value was
measured and disqualified on uwazi (highest P@1 of all arms, collapsed chunk
R@1 19.6-22.8%, lowest cov@3000).

Arms at the recorded cuad leader geometry (merge-2400; Stage 2: all models
95-100% doc@10, split on chunk lenses with gemma leading): merge-2400,
section-2400 and section-split-2400 - 3 arms x 3 shortlisted models = 9 cells.
The merge-2400 stores exist for all three models from the Stage-2 dataset race
(same slug) and are reused - 6 new builds.

Wave-0 + census facts: 462 docs; section partition median 341 chars;
~32.7k section chunks vs 13.5k merge chunks at 2400; 2,039 monster paragraphs
over 2400 chars (26.6% of text mass, max 8,349) - section-split is IN PLAY
here, not a tail case.

Run: `uv run uwazi-rag benchmark --spec benchmarks/sweep32_methods_cuad.py`
"""

from uwazi_rag.use_cases.chunking_methods import MergeChunker, SectionChunker, SectionSplitChunker
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
