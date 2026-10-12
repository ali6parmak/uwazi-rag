"""Chunking-method tests: the ABC contract + every method face (Step 3.5, Step 4c wave 3.1).

Fully offline (AGENTS.md testing policy): the committed capture fixture +
plain assertions. Each ``ChunkMethod`` subclass is asserted byte-equal to
``capture_to_chunks``/``build_chunks`` directly — exactly the equivalence the
store science guard relies on when grading re-chunks captures through the
recorded ``chunk_config`` (``ChunkConfig.from_store`` → ``config_kwargs``).
No mocks.
"""

from __future__ import annotations

import json
from typing import Any

import pytest

from uwazi_rag.configuration import FIXTURES_DIR
from uwazi_rag.domain.chunk import Chunk
from uwazi_rag.use_cases.chunking import TARGET_MAX_CHARS, build_chunks
from uwazi_rag.use_cases.chunking_methods import ChunkMethod, MergeChunker, SectionChunker, SegmentChunker
from uwazi_rag.use_cases.chunking_methods.segment import SEGMENT_SPLIT_BUDGET
from uwazi_rag.use_cases.eval_retrieval import ChunkConfig, config_kwargs
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


# ---------------------------------------------------------------------
# Step 4c wave 3.1 — the method race's two new faces (offline, no mocks)
# ---------------------------------------------------------------------


def _synthetic_capture(paragraphs: list[dict[str, Any]], *, shared_id: str = "syn") -> dict[str, Any]:
    """A raw-shaped capture (field names mirror fetch_document.raw_capture_json)."""
    return {
        "instance_key": "k1",
        "shared_id": shared_id,
        "language": "en",
        "title": shared_id,
        "template": {"id": "tmpl1", "name": "DOCUMENT"},
        "file": {"id": f"{shared_id}.pdf", "name": f"{shared_id}.pdf"},
        "segmentation_status": "ready",
        "fetched_at_utc": None,
        "paragraphs": paragraphs,
    }


def test_segment_chunker_config_and_bytes() -> None:
    chunker = SegmentChunker()
    capture = _capture()

    assert chunker.name == "segment"
    assert chunker.params() == {"max_chars": SEGMENT_SPLIT_BUDGET, "header": True}
    assert chunker.chunk_config() == {
        "target_max_chars": SEGMENT_SPLIT_BUDGET,
        "overlap_ratio": 0.0,
        "prepend_header": True,
        "split_mode": "segment",
    }
    assert chunker.describe() == f"segment {SEGMENT_SPLIT_BUDGET}/on"
    # The science guard, by construction: the recorded config re-chunks byte-identically.
    assert chunker.chunk(capture) == capture_to_chunks(capture, **chunker.chunk_config())
    assert all(chunk.paragraph_ids for chunk in chunker.chunk(capture))


def test_segment_chunker_is_one_chunk_per_segment_overlong_split_overlap_zero() -> None:
    long_text = "word " * 999 + "word"  # 4999 chars, over the split budget
    paragraphs = [
        {"text": "x" * 200},
        {"text": "First short segment."},
        {"text": long_text},
    ]
    chunks = build_chunks(
        paragraphs,
        instance_key="k",
        shared_id="d",
        language="en",
        file_id="f",
        entity_title="T",
        template_name="X",
        target_max_chars=SEGMENT_SPLIT_BUDGET,
        prepend_header=False,
        split_mode="segment",
    )
    bodies = [chunk.text for chunk in chunks]
    assert bodies[0] == "x" * 200 and bodies[1] == "First short segment."  # the two short segments stay whole
    long_pieces = bodies[2:]
    assert len(long_pieces) >= 2  # the over-long segment shattered into several chunks
    assert all(len(piece) <= SEGMENT_SPLIT_BUDGET for piece in long_pieces)
    assert "".join(long_pieces) == long_text  # overlap 0: pieces concatenate to the exact text
    assert all(chunk.paragraph_ids == [2] for chunk in chunks[2:])  # provenance points at one segment
    assert [chunk.chunk_index for chunk in chunks] == list(range(len(chunks)))


def test_section_chunker_config_and_bytes() -> None:
    chunker = SectionChunker(max_chars=1200)
    capture = _capture()  # the real Uwazi fixture — 23 typed headings

    assert chunker.name == "section"
    assert chunker.params() == {"max_chars": 1200, "header": True}
    assert chunker.chunk_config() == {
        "target_max_chars": 1200,
        "overlap_ratio": 0.15,  # the headingless fallback's merge overlap
        "prepend_header": True,
        "split_mode": "section",
    }
    assert chunker.describe() == "section 1200/on"
    assert chunker.chunk(capture) == capture_to_chunks(capture, **chunker.chunk_config())
    assert all(chunk.paragraph_ids for chunk in chunker.chunk(capture))


def test_section_chunker_splits_at_headings_on_typeless_documents() -> None:
    paragraphs = [
        {"text": "Preamble " * 20},
        {"text": "ARTICLE 1. SCOPE"},
        {"text": "y" * 700},
        {"text": "z" * 50},
        {"text": "ARTICLE 2. TERM"},
    ]
    capture = _synthetic_capture(paragraphs)
    chunks = SectionChunker(max_chars=1200).chunk(capture)

    assert [chunk.paragraph_ids for chunk in chunks] == [[0], [1, 2, 3], [4]]  # headings start sections
    assert chunks[1].text.split("\n")[1] == "ARTICLE 1. SCOPE"  # the heading text rides in its section
    assert chunks[2].text.split("\n")[1] == "ARTICLE 2. TERM"
    assert chunks == capture_to_chunks(capture, **SectionChunker(max_chars=1200).chunk_config())


def test_section_chunker_headingless_document_is_byte_equal_to_merge() -> None:
    paragraphs = [{"text": "plain prose " * 130}, {"text": "more plain prose " * 5}]  # no heading anywhere
    capture = _synthetic_capture(paragraphs)

    section = SectionChunker(max_chars=1200).chunk(capture)
    merge = MergeChunker(max_chars=1200).chunk(capture)
    assert section == merge  # the graceful fallback is byte-equal, not approximately similar


def test_chunk_config_round_trips_every_method_through_the_science_guard() -> None:
    capture = _capture()
    methods: list[tuple[str, MergeChunker | SectionChunker | SegmentChunker]] = [
        ("merge", MergeChunker(max_chars=1200)),
        ("segment", SegmentChunker()),
        ("section", SectionChunker(max_chars=1200)),
    ]
    for label, method in methods:
        stored = method.chunk_config()
        config = ChunkConfig.from_store(stored)
        assert config.split_mode == label, method.name
        assert method.chunk(capture) == capture_to_chunks(capture, **config_kwargs(config)), method.name

    legacy = ChunkConfig.from_store({"target_max_chars": 1200, "overlap_ratio": 0.15, "prepend_header": True})
    assert legacy.split_mode == "merge"  # stores recorded before Step 4c carry no split key


def test_build_chunks_rejects_an_unknown_split_mode() -> None:
    with pytest.raises(ValueError, match="split_mode"):
        build_chunks(
            [{"text": "x"}],
            instance_key="k",
            shared_id="d",
            language="en",
            file_id="f",
            entity_title="T",
            template_name="X",
            split_mode="bogus",
        )
    with pytest.raises(ValueError, match="split_mode"):
        build_chunks(
            [{"text": "x"}],
            instance_key="k",
            shared_id="d",
            language="en",
            file_id="f",
            entity_title="T",
            template_name="X",
            split_mode="SEGMENT",  # case-sensitive, like every recorded config value
        )
