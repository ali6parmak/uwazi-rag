"""Step 3.5 sweep 1 — chunk geometry, model fixed at bge-m3 (RECORDED; data/eval/results.md).

One store cell per geometry; the run grades the golden set through the shared
path and appends a comparison. Recorded verdict: 1800/0.15/header-on holds;
2400 strictly worse; 1200 a wash — Step 4 inherits the defaults.

Run: uwazi-rag benchmark --spec benchmarks/sweep1_chunking.py
"""

from uwazi_rag.use_cases.chunking_methods import MergeChunker
from uwazi_rag.use_cases.retrieval_methods import EmbeddingRetrieval
from uwazi_rag.use_cases.run_sweep import StoreCell, define_sweep

experiments = define_sweep(
    [
        StoreCell(label="baseline-1800-header", chunk_method=MergeChunker(), model="bge-m3"),
        StoreCell(label="merge-1200", chunk_method=MergeChunker(max_chars=1200), model="bge-m3"),
        StoreCell(label="merge-2400", chunk_method=MergeChunker(max_chars=2400), model="bge-m3"),
        StoreCell(label="merge-1800-noheader", chunk_method=MergeChunker(header=False), model="bge-m3"),
    ],
    [EmbeddingRetrieval()],
)
