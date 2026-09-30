"""Step 3 tests: the search use case + rendering, offline on a real capture.

Chunks are built from the committed ``ar22d4v4i5s_es.json`` ( Spanish
captured, so cross-language hits prove themselves out-of-process later
against bge-m3) and embedded with the deterministic ``HashingEmbedding`` —
orchestration only, per the AGENTS.md testing policy.
"""

import json

import pytest

from uwazi_rag.adapters.naive_vector_store import NaiveVectorStore
from uwazi_rag.configuration import FIXTURES_DIR
from uwazi_rag.domain.search_hit import SearchHit
from uwazi_rag.tests.hash_embedding import HashingEmbedding
from uwazi_rag.use_cases.semantic_search import format_search_results, semantic_search

DIMENSIONS = 64
MODEL = "hash-test"


def _store_with_fixture_chunks() -> NaiveVectorStore:
    capture = json.loads((FIXTURES_DIR / "ar22d4v4i5s_es.json").read_text(encoding="utf-8"))
    from uwazi_rag.use_cases.index_captures import capture_to_chunks

    chunks = capture_to_chunks(capture)
    assert len(chunks) >= 3  # a real document, chunked
    embedder = HashingEmbedding(DIMENSIONS)
    store = NaiveVectorStore(dimensions=DIMENSIONS, embedding_model=MODEL)
    store.upsert(chunks, embedder.embed([chunk.text for chunk in chunks]))
    return store


def _embedder() -> HashingEmbedding:
    return HashingEmbedding(DIMENSIONS)


def test_identical_text_retrieves_itself_with_full_similarity() -> None:
    store = _store_with_fixture_chunks()
    target = store.chunks()[1]
    hits = semantic_search(query=target.text, store=store, embedder=_embedder(), k=5)
    assert hits[0].chunk.chunk_id == target.chunk_id
    assert hits[0].similarity == pytest.approx(1.0, abs=1e-9)


def test_hits_come_back_ordered_best_first() -> None:
    store = _store_with_fixture_chunks()
    hits = semantic_search(
        query="la Convención Americana sobre Derechos Humanos",
        store=store,
        embedder=_embedder(),
        k=3,
    )
    assert [hit.similarity for hit in hits] == sorted((hit.similarity for hit in hits), reverse=True)


def test_k_bounds_the_returned_hits() -> None:
    store = _store_with_fixture_chunks()
    hits = semantic_search(query="las reservas", store=store, embedder=_embedder(), k=2)
    assert len(hits) == 2
    assert all(isinstance(hit, SearchHit) for hit in hits)
    assert all(hit.similarity >= -1.0 and hit.similarity <= 1.0 for hit in hits)


def test_searches_are_deterministic_for_identical_queries() -> None:
    store = _store_with_fixture_chunks()
    first = semantic_search(query="la Corte", store=store, embedder=_embedder(), k=3)
    second = semantic_search(query="la Corte", store=store, embedder=_embedder(), k=3)
    assert [(hit.chunk.chunk_id, hit.similarity) for hit in first] == [
        (hit.chunk.chunk_id, hit.similarity) for hit in second
    ]


def test_empty_query_is_rejected_before_touching_the_embedder() -> None:
    store = _store_with_fixture_chunks()
    with pytest.raises(ValueError, match="query is empty"):
        semantic_search(query="   ", store=store, embedder=_embedder())


def test_format_renders_header_similarity_and_uwazi_link() -> None:
    store = _store_with_fixture_chunks()
    target = store.chunks()[0]
    hits = semantic_search(query=target.text, store=store, embedder=_embedder(), k=1)

    rendered = format_search_results(hits, base_url="https://example.org")
    header = target.text.split("\n", 1)[0]
    assert header in rendered
    assert f"https://example.org/{target.language}/entity/{target.shared_id}" in rendered
    assert "[cos +1.0000]" in rendered
    assert rendered.startswith("1. ")


def test_format_without_base_url_prints_no_link_and_handles_no_hits() -> None:
    store = _store_with_fixture_chunks()
    hits = semantic_search(query="la Corte", store=store, embedder=_embedder(), k=1)
    rendered = format_search_results(hits)
    assert "https://" not in rendered
    assert "entity/" not in rendered
    assert format_search_results([]).startswith("(no hits")
