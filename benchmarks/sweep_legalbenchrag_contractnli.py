"""Step 4a sweep — the legalbenchrag-contractnli instrument (ContractNLI NDAs).

95 mutual NDAs, 977 expert yes/no questions over 1,389 gold spans (CC BY 4.0).
Same line-paragraph synthesis as privacyqa at 90x the corpus; the ladder
checks whether tighter geometry helps NDAs' clause-hunting questions.

Run: uwazi-rag benchmark --spec benchmarks/sweep_legalbenchrag_contractnli.py
"""

from uwazi_rag.use_cases.chunking_methods import MergeChunker
from uwazi_rag.use_cases.retrieval_methods import EmbeddingRetrieval
from uwazi_rag.use_cases.run_sweep import StoreCell, define_sweep

dataset = "legalbenchrag-contractnli"

experiments = define_sweep(
    [
        StoreCell(label="baseline", chunk_method=MergeChunker(), model="bge-m3"),
        StoreCell(label="merge-1200", chunk_method=MergeChunker(max_chars=1200), model="bge-m3"),
        StoreCell(label="noheader", chunk_method=MergeChunker(header=False), model="bge-m3"),
    ],
    [EmbeddingRetrieval()],
)
