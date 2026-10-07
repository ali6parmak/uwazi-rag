"""Step 4a sweep — the legalbenchrag-maud instrument (MAUD merger agreements).

150 M&A documents (106 KB–1.01 MB, median 342 KB — 115 of 150 at 300 KB and
over) with 1,676 expert questions over 2,839 gold spans — cleared for
integration on license review 2026-10-07. The second long-document pressure
case, beyond cuad: whole-document geometry runs several times larger. Cells
stay to two geometries so a sweep stays within reach; the first recorded run
is baseline only, with merge-2400 as the pending long-doc race cell.
"""

from uwazi_rag.use_cases.chunking_methods import MergeChunker
from uwazi_rag.use_cases.retrieval_methods import EmbeddingRetrieval
from uwazi_rag.use_cases.run_sweep import StoreCell, define_sweep

dataset = "legalbenchrag-maud"

experiments = define_sweep(
    [
        StoreCell(label="baseline", chunk_method=MergeChunker(), model="bge-m3"),
        StoreCell(label="merge-2400", chunk_method=MergeChunker(max_chars=2400), model="bge-m3"),
    ],
    [EmbeddingRetrieval()],
)
