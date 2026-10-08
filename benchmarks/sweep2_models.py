"""Step 3.5 sweep 2 — embedding models at the default chunk geometry.

All cells share the Step 2 constants MergeChunker() ships with
(1800/0.15/header on); one store per model — cosine never mixes embedding
spaces. Recorded verdict (5 models, 2026-10-02/05): nomic-embed-text-v2-moe
wins chunk-level, cross-language and doc R@10; bge-m3 keeps manual chunk R@1
as standby — see the recorded comparison in data/eval/results.md (pre-4a
records: git history).

2026-10-07 race extension: the roster grows to 8 model tags — granite-
embedding (384d), snowflake-arctic-embed2 (1024d) and mxbai-embed-large
(1024d) join; the recorded bge/qwen/nomic/gemma stores were cleared as
disposable caches and rebuild in minutes at 2,850 chunks (qwen3-8b is the
slow one).

nomic-embed-text:v1.5 is deliberately NOT shortlisted (English-centric).

Run: uwazi-rag benchmark --spec benchmarks/sweep2_models.py
"""

from uwazi_rag.use_cases.chunking_methods import MergeChunker
from uwazi_rag.use_cases.retrieval_methods import EmbeddingRetrieval
from uwazi_rag.use_cases.run_sweep import StoreCell, define_sweep

GEOMETRY = [
    ("merge-1800", MergeChunker()),
    ("merge-1200", MergeChunker(max_chars=1200)),
    ("merge-2400", MergeChunker(max_chars=2400)),
]

MODEL_TAGS = [
    "bge-m3",
    "nomic-embed-text-v2-moe",
    "qwen3-embedding:8b",
    "embeddinggemma",
    "granite-embedding",
    "snowflake-arctic-embed2",
    "mxbai-embed-large",
]

experiments = define_sweep(
    [
        StoreCell(label=f"{geo}-{tag.replace(':', '-')}", chunk_method=chunker, model=tag)
        for tag in MODEL_TAGS
        for geo, chunker in GEOMETRY
    ],
    [EmbeddingRetrieval()],
)
