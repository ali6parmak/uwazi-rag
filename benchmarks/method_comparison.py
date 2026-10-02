"""Step 3.5 method comparison on the SAME stores the sweeps cover (RECORDED; data/eval/results.md).

Every cell graded through the three ranking methods: embedding-only vs pure
BM25 vs RRF fusion of the two. m002/m003 (in-text number probes) are the rows
hybrid should fix; m001/m011/m012 (header-driven) and m013-m015 (unanswerable)
are the calibration witnesses. Recorded verdict: embedding-only ships for
Step 4; BM25/RRF stay benchmarked — fusion needs language-awareness first.

Run: uwazi-rag benchmark --spec benchmarks/method_comparison.py
"""

from uwazi_rag.use_cases.chunking_methods import MergeChunker
from uwazi_rag.use_cases.retrieval_methods import Bm25Retrieval, EmbeddingRetrieval, RrfRetrieval
from uwazi_rag.use_cases.run_sweep import StoreCell, define_sweep

GEOMETRY = MergeChunker()  # the Step 2 defaults: 1800/0.15/header on

experiments = define_sweep(
    [
        StoreCell(label="baseline", chunk_method=GEOMETRY, model="bge-m3"),
        StoreCell(label="merge-2400", chunk_method=MergeChunker(max_chars=2400), model="bge-m3"),
        StoreCell(label="merge-1200", chunk_method=MergeChunker(max_chars=1200), model="bge-m3"),
        StoreCell(label="merge-1800-noheader", chunk_method=MergeChunker(header=False), model="bge-m3"),
        StoreCell(label="qwen3-06b", chunk_method=GEOMETRY, model="qwen3-embedding:0.6b"),
        StoreCell(label="nomic-v2-moe", chunk_method=GEOMETRY, model="nomic-embed-text-v2-moe"),
    ],
    [EmbeddingRetrieval(), Bm25Retrieval(), RrfRetrieval()],
)
