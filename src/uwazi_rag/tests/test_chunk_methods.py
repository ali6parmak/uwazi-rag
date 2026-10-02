"""Chunking-method tests: the ABC contract + ``MergeChunker`` as the one chunker's face.

Fully offline (AGENTS.md testing policy): the committed capture fixture +
plain assertions. ``MergeChunker.chunk`` is asserted byte-equal to
``capture_to_chunks``/``build_chunks`` directly — exactly the equivalence the
store science guard relies on when grading re-chunks captures. No mocks.
"""

from __future__ import annotations

import json
from typing import Any

import pytest

from uwazi_rag.configuration import FIXTURES_DIR
from uwazi_rag.domain.chunk import Chunk
from uwazi_rag.use_cases.chunking import TARGET_MAX_CHARS
from uwazi_rag.use_cases.chunking_methods import ChunkMethod, MergeChunker
from uwazi_rag.use_cases.index_captures import capture_to_chunks

FIXTURE_CAPTURE = FIXTURES_DIR / "64hnagcpvk_en.json"


def _capture() -> dict:
    capture: dict = json.loads(FIXTURE_CAPTURE.read_text(encoding="utf-8"))
    return capture


def test_merge_chunker_defaults_are_the_step2_constants() -> None:
    chunker = MergeChunker()

    assert chunker.name == "merge"
    assert chunker.params() == {"max_chars": 1800, "overlap": 0.15, "header": True}
    assert chunker.chunk_config() == {"target_max_chars": 1800, "overlap_ratio": 0.15, "prepend_header": True}
    assert chunker.describe() == "merge 1800/0.15/on"
    assert chunker.max_chars == TARGET_MAX_CHARS


def test_merge_chunker_settings_are_constructor_params() -> None:
    tight = MergeChunker(max_chars=1200)
    assert tight.describe() == "merge 1200/0.15/on"
    assert tight.params() == {"max_chars": 1200, "overlap": 0.15, "header": True}

    bare = MergeChunker(header=False)
    assert bare.describe() == "merge 1800/0.15/off"
    assert bare.chunk_config()["prepend_header"] is False

    zero_overlap = MergeChunker(overlap=0.0)
    assert zero_overlap.describe() == "merge 1800/0/on"


def test_merge_chunker_chunk_equals_the_shared_chunker() -> None:
    capture = _capture()

    assert MergeChunker().chunk(capture) == capture_to_chunks(capture)
    assert MergeChunker().chunk(capture) == capture_to_chunks(capture, **MergeChunker().chunk_config())
    assert MergeChunker(max_chars=600, header=False).chunk(capture) == capture_to_chunks(
        capture, target_max_chars=600, overlap_ratio=0.15, prepend_header=False
    )
    assert MergeChunker(max_chars=600).chunk(capture) == capture_to_chunks(capture, target_max_chars=600)

    chunks = MergeChunker().chunk(capture)  # provenance contract holds on real captured data
    assert chunks
    assert all(chunk.paragraph_ids for chunk in chunks)


def test_merge_chunker_validates_geometry_eagerly() -> None:
    with pytest.raises(ValueError, match="max_chars"):
        MergeChunker(max_chars=0)
    with pytest.raises(ValueError, match="overlap"):
        MergeChunker(overlap=0.5)
    with pytest.raises(ValueError, match="overlap"):
        MergeChunker(overlap=-0.1)


def test_the_abc_enforces_name_and_chunk() -> None:
    class NoName(ChunkMethod):
        def _chunk(self, capture: dict) -> list[Chunk]:  # pragma: no cover
            return []

    class NoChunk(ChunkMethod):
        @property
        def name(self) -> str:  # pragma: no cover
            return "no-chunk"

    with pytest.raises(TypeError):
        NoName()  # type: ignore[abstract]
    with pytest.raises(TypeError):
        NoChunk()  # type: ignore[abstract]


def test_chunk_enforces_the_paragraph_ids_provenance_contract() -> None:
    class Bare(ChunkMethod):
        """A deliberately provenance-less strategy — the ABC must refuse it."""

        @property
        def name(self) -> str:
            return "bare"

        def chunk_config(self) -> dict[str, Any]:  # pragma: no cover
            return {}

        def _chunk(self, capture: dict) -> list[Chunk]:
            if not capture.get("paragraphs"):
                return []
            return [
                Chunk(
                    chunk_id="k:x:en:f:0000",
                    instance_key="k",
                    shared_id="x",
                    language="en",
                    file_id="f",
                    chunk_index=0,
                    text="body",
                    paragraph_ids=[],
                )
            ]

    with pytest.raises(ValueError, match="paragraph_ids"):
        Bare().chunk(_capture())

    assert Bare().chunk({"paragraphs": []}) == []  # an empty capture violates nothing
