"""Step 4a sweep — the legalbenchrag-privacyqa instrument (PrivacyQA Privacy Policies).

7 consumer-privacy-policy documents, 194 expert questions, 453 gold spans, all
MIT-licensed — the smallest legalbenchrag source, so it is the pipe validator:
whole chunk-method ladder × one model through the dataset sweep runner. The
corpus has no blank lines, so paragraphs are lines and the merge chunker is
the native geometry.

Run: uwazi-rag benchmark --spec benchmarks/sweep_legalbenchrag_privacyqa.py
(dataset legalbenchrag-privacyqa — captures data/raw/<sha1('dataset:'+id)[:16]>,
golden data/eval/datasets/legalbenchrag-privacyqa/golden.jsonl)
"""

from uwazi_rag.use_cases.chunking_methods import MergeChunker
from uwazi_rag.use_cases.retrieval_methods import EmbeddingRetrieval
from uwazi_rag.use_cases.run_sweep import StoreCell, define_sweep

dataset = "legalbenchrag-privacyqa"

experiments = define_sweep(
    [
        StoreCell(label="baseline", chunk_method=MergeChunker(), model="bge-m3"),
        StoreCell(label="merge-1200", chunk_method=MergeChunker(max_chars=1200), model="bge-m3"),
        StoreCell(label="merge-2400", chunk_method=MergeChunker(max_chars=2400), model="bge-m3"),
        StoreCell(label="noheader", chunk_method=MergeChunker(header=False), model="bge-m3"),
    ],
    [EmbeddingRetrieval()],
)
