"""Step 3.5 sweep 2 — embedding models at the default chunk geometry (RECORDED; data/eval/results.md).

All cells share the Step 2 constants MergeChunker() ships with
(1800/0.15/header on); one store per model — cosine never mixes embedding
spaces. Recorded verdict: nomic-embed-text-v2-moe wins chunk-level,
cross-language and doc R@10; bge-m3 keeps manual chunk R@1 as standby.

nomic-embed-text:v1.5 is deliberately NOT shortlisted (English-centric).

Run: uwazi-rag benchmark --spec benchmarks/sweep2_models.py
"""

from uwazi_rag.use_cases.chunking_methods import MergeChunker
from uwazi_rag.use_cases.retrieval_methods import EmbeddingRetrieval
from uwazi_rag.use_cases.run_sweep import StoreCell, define_sweep

experiments = define_sweep(
    [
        StoreCell(label="baseline", chunk_method=MergeChunker(), model="bge-m3"),
        StoreCell(label="qwen3-06b", chunk_method=MergeChunker(), model="qwen3-embedding:0.6b"),
        StoreCell(label="nomic-v2-moe", chunk_method=MergeChunker(), model="nomic-embed-text-v2-moe"),
    ],
    [EmbeddingRetrieval()],
)
