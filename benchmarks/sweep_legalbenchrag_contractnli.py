"""Step 4a sweep — the legalbenchrag-contractnli instrument (ContractNLI NDAs).

95 mutual-NDA documents, 977 expert questions, 1,389 gold spans (CC BY 4.0).
Recorded bge-m3 findings: baseline led chunk R@k (35.7% @1), merge-1200 led
MRR/precision, and noheader COLLAPSED chunk retrieval (14.7% R@1 — the NDA
name in the header is the document identity the questions name). The MODEL
RACE holds the two informative geometries (baseline, merge-1200) and crosses
them with the 8-model roster. Dimensions measured 2026-10-07: bge-m3 1024,
qwen3-embedding 1024 (:8b 4096), nomic-v2-moe 768, embeddinggemma 768,
granite-embedding 384, snowflake-arctic-embed2 1024, mxbai-embed-large 1024.
bge-m3 stores under both geometries already exist and are reused.
"""

from uwazi_rag.use_cases.chunking_methods import MergeChunker
from uwazi_rag.use_cases.retrieval_methods import EmbeddingRetrieval
from uwazi_rag.use_cases.run_sweep import StoreCell, define_sweep

dataset = "legalbenchrag-contractnli"

MODEL_TAGS = [
    "bge-m3",
    "qwen3-embedding:0.6b",
    "qwen3-embedding:8b",
    "nomic-embed-text-v2-moe",
    "embeddinggemma",
    "granite-embedding",
    "snowflake-arctic-embed2",
    "mxbai-embed-large",
]
GEOMETRY = [
    ("baseline", MergeChunker()),
    ("merge-1200", MergeChunker(max_chars=1200)),
]

experiments = define_sweep(
    [
        StoreCell(label=f"{geo}-{tag.replace(':', '-')}", chunk_method=chunker, model=tag)
        for tag in MODEL_TAGS
        for geo, chunker in GEOMETRY
    ],
    [EmbeddingRetrieval()],
)
