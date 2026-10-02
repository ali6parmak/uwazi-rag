"""Retrieval-method tests: self-describing instances + parity with the shared ranking path.

Fully offline (AGENTS.md testing policy): tiny captures + the real chunker +
a real saved ``NaiveVectorStore`` + the tests' deterministic
``HashingEmbedding``. The equivalence assertions (a default-parameter method
instance's ranking == ``rank_rows``'s ranking) are the structural guarantee
that sweep numbers equal ``eval`` numbers — no mocks anywhere.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from uwazi_rag.adapters.naive_vector_store import NaiveVectorStore
from uwazi_rag.tests.hash_embedding import HashingEmbedding
from uwazi_rag.use_cases.eval_retrieval import ChunkConfig, first_gold_rank
from uwazi_rag.use_cases.eval_run import prepare_run, rank_rows
from uwazi_rag.use_cases.fetch_document import raw_capture_json
from uwazi_rag.use_cases.index_captures import index_captures
from uwazi_rag.use_cases.retrieval_methods import (
    Bm25Retrieval,
    EmbeddingRetrieval,
    RetrievalMethod,
    RrfRetrieval,
)

DIMENSIONS = 32
INSTANCE = "meth0123456789"

# Varied paragraph lengths across documents so BM25's length normalization (b)
# has something to bite on when settings change.
EN_PARAGRAPHS = [
    "Short opening line about the night raid on the village bridge.",
    "Witnesses described the night raid with exact times and unit insignia. " + "raid unit insignia " * 150,
    "The commission recorded the detentions in its annex and cross-checked the register.",
]
ES_PARAGRAPHS = [
    "Los testigos describieron el asalto nocturno al puente con horas y siglas de la unidad.",
    "La comisión registró las detenciones en su anexo y cotejó las entradas del registro. " * 2,
    "Las reparaciones se discutieron por separado en la sesión de cierre de la visita. " * 3,
]
DECOY_PARAGRAPHS = [
    "Maritime insurance arbitration clauses dominate the annexes of the shipping contract dispute.",
    "The carrier liability ceiling was renegotiated under the freight forwarding agreement. " * 4,
]


def _capture(shared_id: str, language: str, title: str, paragraph_texts: list[str]) -> dict[str, Any]:
    paragraphs = [{"type": "Text", "pageNumber": 1 + index // 2, "text": text} for index, text in enumerate(paragraph_texts)]
    return raw_capture_json(
        shared_id=shared_id,
        language=language,
        instance_key=INSTANCE,
        title=title,
        template_id="t0",
        template_name="IACHR Report",
        file_id=f"f1f1f1{shared_id}",
        file_name="report.pdf",
        segmentation_status="ready",
        paragraphs=paragraphs,
    )


@pytest.fixture()
def prepared(tmp_path: Path) -> Any:
    """A real prepared grading run: corpus → chunks → store → golden rows (offline)."""
    raw_dir = tmp_path / "raw"
    en = _capture("docen2222", "en", "Night Raid Report", EN_PARAGRAPHS)
    es = _capture("doces2222", "es", "Informe del asalto", ES_PARAGRAPHS)
    decoy = _capture("decoy2222", "en", "Shipping Contract Report", DECOY_PARAGRAPHS)
    raw_dir.mkdir(parents=True)
    for capture in (en, es, decoy):
        path = raw_dir / f"{capture['shared_id']}_{capture['language']}.json"
        path.write_text(json.dumps(capture, ensure_ascii=False), encoding="utf-8")

    store = NaiveVectorStore(
        dimensions=DIMENSIONS,
        embedding_model="hashing",
        chunk_config={"target_max_chars": 1800, "overlap_ratio": 0.15, "prepend_header": True},
    )
    index_captures(
        raw_dir=raw_dir, store=store, embedder=HashingEmbedding(dimensions=DIMENSIONS), expected_dimensions=DIMENSIONS
    )
    assert len(store) >= 3, "varied paragraph lengths must produce more than one chunk per capture"
    store_path = tmp_path / "store.json"
    store.save(store_path)

    rows = [
        {
            "id": "q-en",
            "question": EN_PARAGRAPHS[0],
            "origin": "synthetic",
            "query_language": "en",
            "source_group_id": "g-en",
            "expected": {
                "instance_key": INSTANCE,
                "shared_id": "docen2222",
                "language": "en",
                "title": "Night Raid Report",
                "file_id": "f1f1f1docen2222",
                "paragraph_ids": [0],
                "text": "irrelevant",
            },
        },
        {
            "id": "q-es",
            "question": ES_PARAGRAPHS[0],
            "origin": "synthetic",
            "query_language": "en",  # cross-language row: asked in en, gold is es
            "source_group_id": "g-es",
            "expected": {
                "instance_key": INSTANCE,
                "shared_id": "doces2222",
                "language": "es",
                "title": "Informe del asalto",
                "file_id": "f1f1f1doces2222",
                "paragraph_ids": [0],
                "text": "irrelevant",
            },
        },
        {"id": "q-un", "question": "quantum flux monitoring instrumentation grid", "origin": "manual", "expected": None},
    ]
    golden_path = tmp_path / "golden.jsonl"
    golden_path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows), encoding="utf-8")

    run = prepare_run(store_path=store_path, raw_dir=raw_dir, golden_path=golden_path)
    assert run.config == ChunkConfig()
    return run


def test_methods_are_self_describing() -> None:
    embedding, bm25, rrf = EmbeddingRetrieval(), Bm25Retrieval(), RrfRetrieval()

    assert embedding.name == "embedding"
    assert embedding.params() == {}
    assert embedding.describe() == "embedding"

    assert bm25.name == "bm25"
    assert bm25.params() == {"k1": 1.2, "b": 0.75}
    assert bm25.describe() == "bm25 k1=1.2 b=0.75"

    assert rrf.name == "rrf"
    assert rrf.params() == {"k": 60, "weights": [1.0, 1.0]}
    assert rrf.describe() == "rrf k=60 w=1.0/1.0"  # the exact results.md cell format

    custom = Bm25Retrieval(k1=0.5, b=0.1)
    assert custom.describe() == "bm25 k1=0.5 b=0.1"
    assert custom.params() == {"k1": 0.5, "b": 0.1}
    tuned = RrfRetrieval(k=30, weights=(2.0, 1.0))
    assert tuned.describe() == "rrf k=30 w=2.0/1.0"
    assert tuned.params() == {"k": 30, "weights": [2.0, 1.0]}


def test_only_embedding_is_cosine_calibrated() -> None:
    assert EmbeddingRetrieval().cosine_calibrated is True
    assert Bm25Retrieval().cosine_calibrated is False
    assert RrfRetrieval().cosine_calibrated is False


def test_embedding_method_delegates_to_the_shared_path(prepared: Any) -> None:
    embedder = HashingEmbedding(dimensions=DIMENSIONS)
    hits = EmbeddingRetrieval().rank(prepared, embedder=embedder)
    assert hits == rank_rows(prepared, retrieval="embedding", embedder=embedder)

    for gold in prepared.graded.golds:  # sanity: the verbatim question wins its own chunk
        assert first_gold_rank(hits[gold.row_id], gold.gold_chunk_ids) == 1, gold.row_id

    with pytest.raises(ValueError, match="needs an embedder"):
        EmbeddingRetrieval().rank(prepared, embedder=None)


def test_bm25_method_matches_the_shared_path_at_default_settings(prepared: Any) -> None:
    hits = Bm25Retrieval().rank(prepared)
    assert hits == rank_rows(prepared, retrieval="bm25")

    for gold in prepared.graded.golds:  # same-language gold first; cross-language may fail lexically
        if gold.row_id == "q-es":
            continue
        assert first_gold_rank(hits[gold.row_id], gold.gold_chunk_ids) == 1, gold.row_id


def test_bm25_settings_change_the_ranking(prepared: Any) -> None:
    default = Bm25Retrieval().rank(prepared)
    k1_zero = Bm25Retrieval(k1=0.0, b=1.0).rank(prepared)

    assert default.keys() == k1_zero.keys()
    assert any(default[row_id] != k1_zero[row_id] for row_id in default), "settings must flow into the ranking"


def test_rrf_method_matches_the_shared_path_at_default_settings(prepared: Any) -> None:
    embedder = HashingEmbedding(dimensions=DIMENSIONS)
    hits = RrfRetrieval().rank(prepared, embedder=embedder)
    assert hits == rank_rows(prepared, retrieval="rrf", embedder=embedder)

    with pytest.raises(ValueError, match="needs an embedder"):
        RrfRetrieval().rank(prepared, embedder=None)


def test_rrf_k_and_weights_change_the_fusion(prepared: Any) -> None:
    embedder = HashingEmbedding(dimensions=DIMENSIONS)
    default = RrfRetrieval().rank(prepared, embedder=embedder)
    tight = RrfRetrieval(k=1).rank(prepared, embedder=embedder)
    weighted = RrfRetrieval(weights=(2.0, 1.0)).rank(prepared, embedder=embedder)

    assert default.keys() == tight.keys() == weighted.keys()
    assert any(default[row_id] != tight[row_id] for row_id in default), "k must flow into the fusion scores"
    assert any(default[row_id] != weighted[row_id] for row_id in default), "weights must flow into the fusion scores"
    # a fused top-1 is a 1/(k + rank) sum, never the cosine
    assert default["q-en"][0].score <= 2 / (60 + 1) + 1e-12

    with pytest.raises(ValueError, match="exactly two arms"):
        RrfRetrieval(weights=(1.0, 1.0, 1.0))
    with pytest.raises(ValueError, match="weights must be >= 0"):
        RrfRetrieval(weights=(1.0, -1.0))
    with pytest.raises(ValueError, match="k must be >= 1"):
        RrfRetrieval(k=0)


def test_the_abc_enforces_name_and_rank() -> None:
    with pytest.raises(TypeError, match="name"):

        class Nameless(RetrievalMethod):
            def rank(self, prepared: Any, *, embedder: Any = None) -> dict[str, list]:  # pragma: no cover
                return {}

        Nameless()  # type: ignore[abstract]

    with pytest.raises(TypeError, match="rank"):

        class Rankless(RetrievalMethod):
            @property
            def name(self) -> str:  # pragma: no cover
                return "rankless"

        Rankless()  # type: ignore[abstract]
