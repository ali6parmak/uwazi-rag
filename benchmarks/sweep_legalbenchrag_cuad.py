"""Step 4a sweep — the legalbenchrag-cuad instrument (CUAD contract exhibits).

462 SEC-filing contract documents (to 338 KB), 4,042 expert questions, 6,247
gold spans (CC BY 4.0) — the heavy source: ~16,000 chunks per geometry cell,
and long-document pressure the 77-capture harness never had. Cells stay to
two geometries so a full sweep stays within an hour; the first recorded run is
baseline only.

Run: uwazi-rag benchmark --spec benchmarks/sweep_legalbenchrag_cuad.py
"""

from uwazi_rag.use_cases.chunking_methods import MergeChunker
from uwazi_rag.use_cases.retrieval_methods import EmbeddingRetrieval
from uwazi_rag.use_cases.run_sweep import StoreCell, define_sweep

dataset = "legalbenchrag-cuad"

experiments = define_sweep(
    [
        StoreCell(label="baseline", chunk_method=MergeChunker(), model="bge-m3"),
        StoreCell(label="merge-2400", chunk_method=MergeChunker(max_chars=2400), model="bge-m3"),
    ],
    [EmbeddingRetrieval()],
)
