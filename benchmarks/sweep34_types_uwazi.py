"""Step 4c wave 3.4 — the type-aware merge arm on the Uwazi golden (small instrument).

PLAN.md Step 4c wave 3.4 (user call 2026-10-13, raced after the wave-3.3
readouts): merge's exact packing arithmetic — budget 1200, 0.15-overlap monster
cuts, header on — plus ONE rule: a packing run breaks when a keepable
paragraph's content type changes; "section header"/"title" are glue (they take
the effective type of the body run they preface — the user's "same types merge
together; header and title may go together"), and the wave-3.3 breadcrumb
composes with the arm (same user call). One change at a time is kept by the
2×2: {merge, type-merge} × {plain, +breadcrumb} — both main effects read
cleanly (type-vs-merge, crumb-vs-no-crumb) plus the interaction.

Uwazi-only by nature: every dataset home is a single-type ("text" everywhere)
corpus → type-merge is byte-equal to merge there by construction. The
pre-statement scan (offline, pure, 2026-10-13) on this home: merge 4,488
chunks → ~5,565 type-merge chunks (+24%; 2,033 effective type boundaries —
footnotes ×2,690 and list items ×813 are what the runs separate from body
text).

Race: 4 arms × the 3 shortlisted models = 12 cells; the merge-1200 and
merge-crumb-1200 stores (same slugs) are reused from sweep33 — 6 new builds.
Run: `uv run uwazi-rag benchmark --spec benchmarks/sweep34_types_uwazi.py`
"""

from uwazi_rag.use_cases.chunking_methods import MergeChunker, TypeMergeChunker
from uwazi_rag.use_cases.retrieval_methods import EmbeddingRetrieval
from uwazi_rag.use_cases.run_sweep import StoreCell, define_sweep

MODELS = [
    "bge-m3",
    "embeddinggemma",
    "snowflake-arctic-embed2",
]
ARMS = [
    ("merge-1200", MergeChunker(max_chars=1200)),
    ("merge-crumb-1200", MergeChunker(max_chars=1200, breadcrumb=True)),
    ("type-merge-1200", TypeMergeChunker(max_chars=1200)),
    ("type-merge-crumb-1200", TypeMergeChunker(max_chars=1200, breadcrumb=True)),
]

experiments = define_sweep(
    [
        StoreCell(label=f"{geo}-{tag.replace(':', '-')}", chunk_method=chunker, model=tag)
        for tag in MODELS
        for geo, chunker in ARMS
    ],
    [EmbeddingRetrieval()],
)
