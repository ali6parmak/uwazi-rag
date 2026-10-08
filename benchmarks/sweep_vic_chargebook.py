"""Step 4a sweep — the vic-chargebook instrument (Isaacus's Legal RAG Bench).

4,876 pre-chunked passages of the Victorian Criminal Charge Book, 100 expert
questions (one labeled passage each — 5 passages carry two questions), CC
BY-NC-SA 4.0. The corpus arrives chunked: the pass-through chunk method makes
each passage ONE chunk, currencies collapse to hit-rate/MRR by design (the
home's about.md documents this), and the question set is deliberately
lexically-dissimilar from its gold — the honest precision label we have.
bge-m3 recorded 16% @1 / 42% @10. The MODEL RACE crosses the pass-through
pair (header on/off) with the 8-model roster; geometry has nothing to turn
here — the model axis is the only live one. Dimensions measured 2026-10-07:
bge-m3 1024, qwen3-embedding 1024 (:8b 4096), nomic-v2-moe 768,
embeddinggemma 768, granite-embedding 384, snowflake-arctic-embed2 1024,
mxbai-embed-large 1024. bge-m3 stores already exist and are reused.
"""

from uwazi_rag.use_cases.chunking_methods import PassThroughChunker
from uwazi_rag.use_cases.retrieval_methods import EmbeddingRetrieval
from uwazi_rag.use_cases.run_sweep import StoreCell, define_sweep

dataset = "vic-chargebook"

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
    ("baseline", PassThroughChunker()),
    ("noheader", PassThroughChunker(header=False)),
]

experiments = define_sweep(
    [
        StoreCell(label=f"{geo}-{tag.replace(':', '-')}", chunk_method=chunker, model=tag)
        for tag in MODEL_TAGS
        for geo, chunker in GEOMETRY
    ],
    [EmbeddingRetrieval()],
)
