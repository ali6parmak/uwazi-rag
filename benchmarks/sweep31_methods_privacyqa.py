"""Step 4c wave 3.1 — the chunking-method race on the privacyqa instrument.

Three shortlisted models (user call 2026-10-11) × the privacyqa arms at the
recorded leader geometry (merge-2400, Stage 2: bge-m3's incumbent lead was
confirmed there). The wave-3.0 scan measured 1/7 privacyqa documents with any
heading — the SectionChunker mostly measures its headingless fallback here,
which is exactly the point of racing the arm on an almost-headingless corpus.

The merge-2400 stores already exist (Stage-2 model race, same slug) and are
reused. Run: `uv run uwazi-rag benchmark --spec
benchmarks/sweep31_methods_privacyqa.py`
"""

from uwazi_rag.use_cases.chunking_methods import MergeChunker, SectionChunker
from uwazi_rag.use_cases.retrieval_methods import EmbeddingRetrieval
from uwazi_rag.use_cases.run_sweep import StoreCell, define_sweep

dataset = "legalbenchrag-privacyqa"

MODELS = [
    "bge-m3",
    "embeddinggemma",
    "snowflake-arctic-embed2",
]
ARMS = [
    ("merge-2400", MergeChunker(max_chars=2400)),
    ("section-2400", SectionChunker(max_chars=2400)),
]

experiments = define_sweep(
    [
        StoreCell(label=f"{geo}-{tag.replace(':', '-')}", chunk_method=chunker, model=tag)
        for tag in MODELS
        for geo, chunker in ARMS
    ],
    [EmbeddingRetrieval()],
)
