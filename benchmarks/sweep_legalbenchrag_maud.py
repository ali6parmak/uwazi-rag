"""Step 4a sweep — the legalbenchrag-maud instrument (MAUD merger agreements).

150 M&A documents (106 KB–1.01 MB, median 342 KB — 115 of 150 at 300 KB and
over), 1,676 expert questions, 2,839 gold spans — cleared for integration on
license review 2026-10-07. The second long-document pressure case (beyond
cuad): bge-m3's merge geometry has not been recorded here yet, so every cell
below is a fresh build. The MODEL RACE holds the long-doc pair (baseline,
merge-2400 — the pending long-doc race cells on cuad's shape) and crosses
them with the 8-model roster. Dimensions measured 2026-10-07: bge-m3 1024,
qwen3-embedding 1024 (:8b 4096), nomic-v2-moe 768, embeddinggemma 768,
granite-embedding 384, snowflake-arctic-embed2 1024, mxbai-embed-large 1024.
Heaviest corpus in the set (~38k chunks at 1800): the qwen3-8b cells alone
rebuild near an hour each; run in its own window, resume with --only.

Run: uwazi-rag benchmark --spec benchmarks/sweep_legalbenchrag_maud.py
(dataset legalbenchrag-maud — captures data/raw/4961ebee611362f6, golden
data/eval/datasets/legalbenchrag-maud/golden.jsonl)
"""

from uwazi_rag.use_cases.chunking_methods import MergeChunker
from uwazi_rag.use_cases.retrieval_methods import EmbeddingRetrieval
from uwazi_rag.use_cases.run_sweep import StoreCell, define_sweep

dataset = "legalbenchrag-maud"

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
