"""Step 4c wave 3.3 — rung 2 on the winner (merge) on the contractnli instrument.

Same race as benchmarks/sweep33_methods_uwazi.py (PLAN.md wave-3.3
pre-statement: arms {merge incumbent, merge+sentence_cuts, merge+breadcrumb,
merge+both} × the 3 shortlisted models at the recorded leader geometry
merge-1200) on the second instrument that can measure rung 2 — 82 monster
paragraphs @1200 (12.7% of text mass) for the sentence lens, 92/95 docs
regex-headed for the crumb lens, 9 new builds (merge-1200 reuse).

privacyqa stays out by pre-statement (no monsters, 6/7 byte-equal fallback).
Finalists confirm on cuad/maud after these readouts.

Run: `uv run uwazi-rag benchmark --spec benchmarks/sweep33_methods_contractnli.py`
"""

from uwazi_rag.use_cases.chunking_methods import MergeChunker
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
