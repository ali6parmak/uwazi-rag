"""Step 3 tests: the naive vector store, offline on hand-computed vectors.

Real implementation (the store) plus plain assertions — no mocks, no
network (AGENTS.md testing policy). Vectors are 2–3 dimensional by hand so
cosine values are exactly predictable.
"""

from pathlib import Path

import pytest

from uwazi_rag.adapters.naive_vector_store import (
    NaiveStoreMismatchError,
    NaiveVectorStore,
)
from uwazi_rag.domain.chunk import Chunk


def _chunk(index: int, *, shared_id: str = "aaaa1111") -> Chunk:
    instance_key, language, file_id = "bdd5a7c445847b35", "en", "6a75b7b3"
    return Chunk(
        chunk_id=f"{instance_key}:{shared_id}:{language}:{file_id}:{index:04d}",
        instance_key=instance_key,
        shared_id=shared_id,
        language=language,
        file_id=file_id,
        chunk_index=index,
        text=f"Header (page {index + 1})\nbody {index}",
        page_start=index + 1,
        page_end=index + 1,
    )


def _store(dimensions: int = 2) -> NaiveVectorStore:
    return NaiveVectorStore(dimensions=dimensions, embedding_model="test-model")


def test_cosine_orders_hand_vectors_exactly() -> None:
    store = _store()
    store.upsert(
        [_chunk(0), _chunk(1), _chunk(2)],
        [[1.0, 0.0], [0.0, 1.0], [0.6, 0.8]],
    )
    hits = store.search([1.0, 0.0], k=2)
    assert [chunk.chunk_index for chunk, _ in hits] == [0, 2]
    assert hits[0][1] == pytest.approx(1.0)
    assert hits[1][1] == pytest.approx(0.6)


def test_top_k_is_respected_and_never_overflows_the_store() -> None:
    store = _store()
    store.upsert([_chunk(i) for i in range(3)], [[1.0, 0.0], [0.9, 0.1], [0.0, 1.0]])
    assert len(store.search([1.0, 0.0], k=2)) == 2
    assert len(store.search([1.0, 0.0], k=50)) == 3
    # similar direction first, still strictly by similarity
    hits = store.search([1.0, 0.0], k=3)
    assert hits[0][0].chunk_index == 0
    assert hits[0][1] >= hits[1][1] >= hits[2][1]


def test_search_on_an_empty_store_returns_no_hits() -> None:
    assert _store().search([1.0, 0.0]) == []


def test_upsert_overwrites_by_chunk_identity_never_duplicates() -> None:
    store = _store()
    store.upsert([_chunk(0)], [[1.0, 0.0]])
    store.upsert([_chunk(0)], [[0.0, 1.0]])  # same chunk_id, new vector
    assert len(store) == 1
    hits = store.search([0.0, 1.0], k=5)
    assert len(hits) == 1 and hits[0][1] == pytest.approx(1.0)


def test_dimension_mismatches_are_rejected_loudly() -> None:
    store = _store(dimensions=2)
    with pytest.raises(ValueError, match="shape"):
        store.upsert([_chunk(0)], [[1.0, 2.0, 3.0]])
    with pytest.raises(ValueError, match="shape"):
        store.search([1.0, 0.0, 0.0])
    assert len(store) == 0  # nothing half-committed


def test_zero_vectors_score_zero_instead_of_nan() -> None:
    store = _store()
    store.upsert([_chunk(0)], [[0.0, 0.0]])
    hits = store.search([1.0, 0.0], k=5)
    assert hits[0][1] == 0.0


def test_instance_key_filter_narrows_the_scan() -> None:
    store = _store()
    store.upsert(
        [_chunk(0), _chunk(1)],
        [[1.0, 0.0], [0.9, 0.1]],
    )
    other = _chunk(0, shared_id="zzzz9999").model_copy(
        update={
            "chunk_id": "2bf0fa1d7db9ecd6:zzzz9999:en:6a75b7b3:0000",
            "instance_key": "2bf0fa1d7db9ecd6",
            "shared_id": "zzzz9999",
        }
    )
    store.upsert([other], [[0.0, 1.0]])
    hits = store.search([1.0, 0.0], k=10, instance_key="bdd5a7c445847b35")
    assert {chunk.instance_key for chunk, _ in hits} == {"bdd5a7c445847b35"}
    assert store.search([1.0, 0.0], k=10, instance_key="nope") == []


def test_save_load_round_trip_preserves_everything(tmp_path: Path) -> None:
    store = NaiveVectorStore(dimensions=3, embedding_model="test-model")
    chunks = [_chunk(0), _chunk(1)]
    store.upsert(chunks, [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])
    path = tmp_path / "nested" / "naive.json"
    store.save(path)

    loaded = NaiveVectorStore.load(path, embedding_model="test-model", dimensions=3)
    assert len(loaded) == len(store) == 2
    assert loaded.embedding_model == "test-model"
    assert loaded.created_at_utc == store.created_at_utc
    assert [chunk.model_dump() for chunk in loaded.chunks()] == [chunk.model_dump() for chunk in store.chunks()]
    first = loaded.search([1.0, 0.0, 0.0], k=1)
    assert first[0][0].chunk_id == chunks[0].chunk_id
    assert first[0][1] == pytest.approx(1.0, abs=1e-12)
    second = loaded.search([0.0, 1.0, 0.0], k=1)
    assert second[0][0].chunk_id == chunks[1].chunk_id
    assert second[0][1] == pytest.approx(1.0, abs=1e-12)


def test_load_with_a_different_model_or_dims_is_refused(tmp_path: Path) -> None:
    store = _store(dimensions=2)
    store.upsert([_chunk(0)], [[1.0, 0.0]])
    path = tmp_path / "naive.json"
    store.save(path)

    with pytest.raises(NaiveStoreMismatchError, match="build-index"):
        NaiveVectorStore.load(path, embedding_model="other-model")
    with pytest.raises(NaiveStoreMismatchError, match="build-index"):
        NaiveVectorStore.load(path, dimensions=8)


def test_loading_a_non_store_file_is_refused(tmp_path: Path) -> None:
    path = tmp_path / "junk.json"
    path.write_text('{"schema": "something_else"}', encoding="utf-8")
    with pytest.raises(NaiveStoreMismatchError, match="naive_store_v1"):
        NaiveVectorStore.load(path)


def test_chunk_config_survives_save_and_load(tmp_path: Path) -> None:
    """The graded chunk config rides along the store file (Step 3.5)."""
    store = _store(dimensions=2)
    store.chunk_config = {"target_max_chars": 900, "overlap_ratio": 0.3, "prepend_header": False}
    store.upsert([_chunk(0)], [[1.0, 0.0]])
    path = tmp_path / "naive.json"
    store.save(path)

    loaded = NaiveVectorStore.load(path)
    assert loaded.chunk_config == {"target_max_chars": 900, "overlap_ratio": 0.3, "prepend_header": False}


def test_legacy_store_without_chunk_config_loads_empty(tmp_path: Path) -> None:
    """Entries persisted before ``paragraph_ids``/``chunk_config`` existed still load."""
    import json

    store = _store(dimensions=2)
    store.upsert([_chunk(0)], [[1.0, 0.0]])
    path = tmp_path / "legacy.json"
    store.chunk_config = None
    store.save(path)

    # Simulate the pre-provenance legacy shape: no chunk_config key, no
    # paragraph_ids on entries (like the committed baseline store on disk).
    data = json.loads(path.read_text(encoding="utf-8"))
    data.pop("chunk_config", None)
    for entry in data["entries"]:
        entry["chunk"].pop("paragraph_ids", None)
    path.write_text(json.dumps(data), encoding="utf-8")

    loaded = NaiveVectorStore.load(path)
    assert loaded.chunk_config is None
    assert loaded.chunks()[0].paragraph_ids == []
