"""Step 4a sweep — the vic-chargebook instrument (Isaacus's Legal RAG Bench).

4,876 pre-chunked passages of the Victorian Criminal Charge Book, 100 expert
questions (one labeled passage each — 5 passages carry two questions), CC
BY-NC-SA 4.0. The corpus arrives chunked: the pass-through chunk method makes
each passage ONE chunk, currencies collapse to hit-rate/MRR by design (the
home's about.md documents this), and the question set is deliberately
lexically-dissimilar from its gold — the honest precision label we have.

Run: uwazi-rag benchmark --spec benchmarks/sweep_vic_chargebook.py
"""

from uwazi_rag.use_cases.chunking_methods import PassThroughChunker
from uwazi_rag.use_cases.retrieval_methods import EmbeddingRetrieval
from uwazi_rag.use_cases.run_sweep import StoreCell, define_sweep

dataset = "vic-chargebook"

experiments = define_sweep(
    [
        StoreCell(label="baseline", chunk_method=PassThroughChunker(), model="bge-m3"),
        StoreCell(label="noheader", chunk_method=PassThroughChunker(header=False), model="bge-m3"),
    ],
    [EmbeddingRetrieval()],
)
