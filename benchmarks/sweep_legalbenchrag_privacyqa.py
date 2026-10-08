"""Step 4a sweep — the legalbenchrag-privacyqa instrument (PrivacyQA Privacy Policies).

7 consumer-privacy-policy documents, 194 expert questions, 453 gold spans, all
MIT-licensed — the smallest legalbenchrag source, so it is the pipe validator.
Original recorded verdicts came from bge-m3 over the full chunk-method ladder
(merge-2400 led every chunk/paragraph lens; doc-level saturated at 7 docs), so
the MODEL RACE holds geometry at the two informative cells — baseline and the
merge-2400 leader — and crosses them with the 8-model roster. Dimensions
measured 2026-10-07: bge-m3 1024, qwen3-embedding 1024 (:8b 4096), nomic-v2-moe
768, embeddinggemma 768, granite-embedding 384, snowflake-arctic-embed2 1024,
mxbai-embed-large 1024. bge-m3 stores under both geometries already exist and
are reused (rescored in this run's fresh blocks).

Run: uwazi-rag benchmark --spec benchmarks/sweep_legalbenchrag_privacyqa.py
(dataset legalbenchrag-privacyqa — captures data/raw/<sha1('dataset:'+id)[:16]>,
golden data/eval/datasets/legalbenchrag-privacyqa/golden.jsonl)
"""

from uwazi_rag.use_cases.chunking_methods import MergeChunker
from uwazi_rag.use_cases.retrieval_methods import EmbeddingRetrieval
from uwazi_rag.use_cases.run_sweep import StoreCell, define_sweep

dataset = "legalbenchrag-privacyqa"

MODEL_TAGS = [
    "bge-m3",
    "qwen3-embedding:8b",
    "nomic-embed-text-v2-moe",
    "embeddinggemma",
    "granite-embedding",
    "snowflake-arctic-embed2",
    "mxbai-embed-large",
]
GEOMETRY = [
    ("baseline", MergeChunker()),
    ("merge-2400", MergeChunker(max_chars=2400)),
]

experiments = define_sweep(
    [
        StoreCell(label=f"{geo}-{tag.replace(':', '-')}", chunk_method=chunker, model=tag)
        for tag in MODEL_TAGS
        for geo, chunker in GEOMETRY
    ],
    [EmbeddingRetrieval()],
)
