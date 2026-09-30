"""Step 3 tests: chunk + embed the captured corpus, offline on fixtures.

Uses the committed real captures (64hnagcpvk_en, ar22d4v4i5s_en/es) copied
into a tmp ``data/raw``-shaped dir, plus synthetic captures assembled through
the real ``raw_capture_json`` for the skip paths. Embeddings come from the
tests' deterministic ``HashingEmbedding`` — orchestration only, never
semantic quality (AGENTS.md testing policy).
"""

import json
from pathlib import Path

import pytest

from uwazi_rag.adapters.naive_vector_store import NaiveVectorStore
from uwazi_rag.configuration import FIXTURES_DIR
from uwazi_rag.tests.hash_embedding import HashingEmbedding
from uwazi_rag.use_cases.fetch_document import raw_capture_json
from uwazi_rag.use_cases.index_captures import (
    capture_to_chunks,
    index_captures,
    load_captures,
)

DIMENSIONS = 16
FIXTURES = ["64hnagcpvk_en.json", "ar22d4v4i5s_en.json", "ar22d4v4i5s_es.json"]


def _fixture(name: str) -> dict:
    capture: dict = json.loads((FIXTURES_DIR / name).read_text(encoding="utf-8"))
    return capture


def _capture_dir(tmp_path: Path, names: list[str]) -> Path:
    """Copy the committed fixtures into a fresh raw dir, capture-name shaped."""
    raw_dir = tmp_path / "raw" / "bdd5a7c445847b35"
    raw_dir.mkdir(parents=True)
    for name in names:
        capture = _fixture(name)
        (raw_dir / f"{capture['shared_id']}_{capture['language']}.json").write_text(
            json.dumps(capture, ensure_ascii=False), encoding="utf-8"
        )
    return raw_dir


def _store() -> NaiveVectorStore:
    return NaiveVectorStore(dimensions=DIMENSIONS, embedding_model="hash-test")


def _index(tmp_path: Path, names: list[str], *, batch_size: int = 2) -> tuple[Path, NaiveVectorStore]:
    raw_dir = _capture_dir(tmp_path, names)
    store = _store()
    index_captures(
        raw_dir=raw_dir,
        store=store,
        embedder=HashingEmbedding(DIMENSIONS),
        expected_dimensions=DIMENSIONS,
        batch_size=batch_size,
    )
    return raw_dir, store


def test_indexes_every_chunk_of_the_real_fixtures(tmp_path: Path) -> None:
    raw_dir = _capture_dir(tmp_path, FIXTURES)
    store = _store()
    stats = index_captures(
        raw_dir=raw_dir,
        store=store,
        embedder=HashingEmbedding(DIMENSIONS),
        expected_dimensions=DIMENSIONS,
        batch_size=3,
    )

    expected = [chunk for name in FIXTURES for chunk in capture_to_chunks(_fixture(name))]
    assert stats.captures_seen == 3
    assert stats.captures_indexed == 3
    assert stats.skipped_not_ready == 0
    assert stats.skipped_no_chunks == 0
    assert stats.chunks_indexed == len(expected)
    assert len(store) == len(expected)
    assert [chunk.chunk_id for chunk in store.chunks()] == [chunk.chunk_id for chunk in expected]


def test_reindexing_the_same_captures_is_idempotent(tmp_path: Path) -> None:
    raw_dir, store = _index(tmp_path, FIXTURES)
    before = [chunk.model_dump() for chunk in store.chunks()]

    stats_again = index_captures(
        raw_dir=raw_dir,
        store=store,
        embedder=HashingEmbedding(DIMENSIONS),
        expected_dimensions=DIMENSIONS,
        batch_size=5,
    )
    assert stats_again.chunks_indexed == len(before)
    assert len(store) == len(before)  # upsert overwrote, never duplicated
    assert [chunk.model_dump() for chunk in store.chunks()] == before


def test_load_captures_reads_every_json_sorted(tmp_path: Path) -> None:
    raw_dir = _capture_dir(tmp_path, FIXTURES)
    captures = load_captures(raw_dir)
    assert len(captures) == 3
    names = sorted(f"{capture['shared_id']}_{capture['language']}.json" for capture in captures)
    assert [path.name for path in sorted(raw_dir.glob("*.json"))] == names


def test_skips_not_ready_and_textless_captures_not_fatal(tmp_path: Path) -> None:
    raw_dir = tmp_path / "raw" / "bdd5a7c445847b35"
    raw_dir.mkdir(parents=True)
    not_ready = raw_capture_json(
        shared_id="aaaa1111bbbb",
        language="en",
        instance_key="bdd5a7c445847b35",
        title="Still processing",
        template_id="5bfbb1a0471dd0fc16ada146",
        template_name="DOCUMENT",
        file_id="ffff0000",
        file_name="still.pdf",
        segmentation_status="processing",
        paragraphs=[{"type": "Text", "pageNumber": 1, "text": "Real text, not indexed yet."}],
        fetched_at_utc="2025-01-01T00:00:00+00:00",
    )
    textless = raw_capture_json(
        shared_id="cccc2222dddd",
        language="es",
        instance_key="bdd5a7c445847b35",
        title="Scanned pages only",
        template_id="5bfbb1a0471dd0fc16ada146",
        template_name="DOCUMENT",
        file_id="eeee1111",
        file_name="scan.pdf",
        segmentation_status="ready",
        paragraphs=[
            {"type": "Page header", "pageNumber": 1, "text": "repetitive header"},
            {"type": "Picture", "pageNumber": 1, "text": ""},
        ],
        fetched_at_utc="2025-01-01T00:00:00+00:00",
    )
    (raw_dir / "aaaa1111bbbb_en.json").write_text(json.dumps(not_ready), encoding="utf-8")
    (raw_dir / "cccc2222dddd_es.json").write_text(json.dumps(textless), encoding="utf-8")

    store = _store()
    stats = index_captures(
        raw_dir=raw_dir,
        store=store,
        embedder=HashingEmbedding(DIMENSIONS),
        expected_dimensions=DIMENSIONS,
    )
    assert stats.captures_seen == 2
    assert stats.captures_indexed == 0
    assert stats.skipped_not_ready == 1
    assert stats.skipped_no_chunks == 1
    assert stats.chunks_indexed == 0
    assert len(store) == 0


def test_embedder_dimension_mismatch_fails_before_any_upsert(tmp_path: Path) -> None:
    raw_dir = tmp_path / "raw" / "bdd5a7c445847b35"
    raw_dir.mkdir(parents=True)
    capture = _fixture("ar22d4v4i5s_en.json")
    (raw_dir / f"{capture['shared_id']}_en.json").write_text(json.dumps(capture, ensure_ascii=False), encoding="utf-8")

    store = _store()
    with pytest.raises(RuntimeError, match="EMBEDDING_DIMENSIONS"):
        index_captures(
            raw_dir=raw_dir,
            store=store,
            embedder=HashingEmbedding(8),  # wrong size vs expected_dimensions
            expected_dimensions=DIMENSIONS,
        )
    assert len(store) == 0  # fail-fast: nothing half-embedded


def test_limit_bounds_the_run_for_smoke_tests(tmp_path: Path) -> None:
    raw_dir = _capture_dir(tmp_path, FIXTURES)
    store = _store()
    stats = index_captures(
        raw_dir=raw_dir,
        store=store,
        embedder=HashingEmbedding(DIMENSIONS),
        expected_dimensions=DIMENSIONS,
        limit=1,
    )
    assert stats.captures_seen == 1
    expected = capture_to_chunks(_fixture(FIXTURES[0]))
    assert stats.chunks_indexed == len(expected) > 0


def test_broken_embedder_contract_is_caught(tmp_path: Path) -> None:
    raw_dir = _capture_dir(tmp_path, ["ar22d4v4i5s_en.json"])
    store = _store()

    class ShortEmbedder(HashingEmbedding):
        """A real embedder that breaks the port's count contract."""

        def embed(self, texts: list[str]) -> list[list[float]]:
            return super().embed(texts[:-1])  # one vector short

    with pytest.raises(RuntimeError, match="vectors for a batch"):
        index_captures(
            raw_dir=raw_dir,
            store=store,
            embedder=ShortEmbedder(DIMENSIONS),
            expected_dimensions=DIMENSIONS,
        )
