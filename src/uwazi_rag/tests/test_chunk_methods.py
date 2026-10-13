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
from uwazi_rag.use_cases.chunking import TARGET_MAX_CHARS, _split_long, build_chunks, sentence_split
from uwazi_rag.use_cases.chunking_methods import (
    ChunkMethod,
    MergeChunker,
    SectionChunker,
    SectionSplitChunker,
    SegmentChunker,
    TypeMergeChunker,
)
from uwazi_rag.use_cases.chunking_methods.segment import SEGMENT_SPLIT_BUDGET
from uwazi_rag.use_cases.eval_retrieval import ChunkConfig, config_kwargs
from uwazi_rag.use_cases.headings import effective_types, is_heading, partition_sections
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


def test_section_chunker_repeats_the_heading_on_continuation_chunks() -> None:
    heading = "ARTICLE 1. DEFINITIONS"  # 22 chars
    paragraphs = [
        {"text": heading},
        {"text": "b" * 277},  # heading + this = exactly the 300 budget
        {"text": "c" * 299},  # overflows -> continuation chunk
        {"text": "ARTICLE 2. TERM"},
        {"text": "closing body"},
    ]
    capture = _synthetic_capture(paragraphs)
    chunks = SectionChunker(max_chars=300).chunk(capture)

    # Packing is unchanged: [0, 1] fits the budget exactly, [2] is the overflow.
    assert [chunk.paragraph_ids for chunk in chunks] == [[0, 1], [0, 2], [3, 4]]
    first, continuation, last = chunks
    assert first.text.split("\n")[1] == heading  # the heading opens its own chunk — no prefix needed
    assert continuation.text.split("\n", 1)[0].startswith("syn — DOCUMENT")  # doc-context header first
    section_text = continuation.text.split("\n", 1)[1]  # the section layer below the doc header
    assert section_text.split("\n")[0] == heading  # repeated heading line on top
    assert section_text.split("\n")[1] == "c" * 299
    assert continuation.paragraph_ids == [0, 2]  # the heading paragraph anchors its whole section
    assert len(section_text) == 22 + 1 + 299  # the repeated line is NOT counted against the budget
    assert last.text.split("\n")[1] == "ARTICLE 2. TERM"  # a section that fits is not prefixed
    assert chunks == capture_to_chunks(capture, **SectionChunker(max_chars=300).chunk_config())


def test_section_split_chunker_config_and_bytes() -> None:
    chunker = SectionSplitChunker(max_chars=1200)
    capture = _capture()

    assert chunker.name == "section-split"
    assert chunker.params() == {"max_chars": 1200, "header": True}
    assert chunker.chunk_config() == {
        "target_max_chars": 1200,
        "overlap_ratio": 0.15,  # merge-style: governs cuts inside a monster paragraph
        "prepend_header": True,
        "split_mode": "section-split",
    }
    assert chunker.describe() == "section-split 1200/on"
    assert chunker.chunk(capture) == capture_to_chunks(capture, **chunker.chunk_config())
    assert all(chunk.paragraph_ids for chunk in chunker.chunk(capture))


def test_section_split_word_splits_monsters_with_merge_style_overlap() -> None:
    heading = "SECTION 7. LIMITATION OF LIABILITY"  # 34 chars
    paragraphs = [
        {"text": heading},
        {"text": "w" * 4000},  # the monster: no internal boundary, over the 2400 budget
        {"text": "Normal short paragraph after the monster."},
    ]
    chunks = build_chunks(
        paragraphs,
        instance_key="k",
        shared_id="d",
        language="en",
        file_id="f",
        entity_title="T",
        template_name="X",
        target_max_chars=2400,
        prepend_header=False,
        split_mode="section-split",
    )
    assert [chunk.paragraph_ids for chunk in chunks] == [[0], [0, 1], [0, 1], [0, 2]]
    assert [len(chunk.text) for chunk in chunks] == [
        len(heading),
        len(heading) + 1 + 2400,
        len(heading) + 1 + 1960,
        len(heading) + 1 + len(paragraphs[2]["text"]),
    ]
    first, piece1, piece2, last = chunks
    assert first.text == heading  # the heading chunk itself is not prefixed
    assert piece1.text.split("\n")[0] == heading and piece2.text.split("\n")[0] == heading  # repeat on every piece
    assert last.text.split("\n")[0] == heading  # the trailing normal paragraph is a continuation too
    # the merge-style cut: the pieces share the 0.15-overlap band (0.15 * 2400 = 360 chars)
    assert piece1.text.split("\n", 1)[1][-360:] == piece2.text.split("\n", 1)[1][:360]


def test_section_split_is_byte_equal_to_section_without_monsters() -> None:
    paragraphs = [
        {"text": "Preamble of the agreement."},
        {"text": "ARTICLE 1. SCOPE"},
        {"text": "y" * 700},
        {"text": "z" * 50},
        {"text": "ARTICLE 2. TERM"},
    ]
    capture = _synthetic_capture(paragraphs)
    assert all(len(str(p["text"]).strip()) < 1200 for p in paragraphs)  # no monster at this budget
    assert SectionSplitChunker(max_chars=1200).chunk(capture) == SectionChunker(max_chars=1200).chunk(capture)


def test_section_chunker_headingless_document_is_byte_equal_to_merge() -> None:
    paragraphs = [{"text": "plain prose " * 130}, {"text": "more plain prose " * 5}]  # no heading anywhere
    capture = _synthetic_capture(paragraphs)

    section = SectionChunker(max_chars=1200).chunk(capture)
    merge = MergeChunker(max_chars=1200).chunk(capture)
    assert section == merge  # the graceful fallback is byte-equal, not approximately similar


def test_chunk_config_round_trips_every_method_through_the_science_guard() -> None:
    capture = _capture()
    methods: list[tuple[str, MergeChunker | SectionChunker | SectionSplitChunker | SegmentChunker | TypeMergeChunker]] = [
        ("merge", MergeChunker(max_chars=1200)),
        ("segment", SegmentChunker()),
        ("section", SectionChunker(max_chars=1200)),
        ("section-split", SectionSplitChunker(max_chars=1200)),
        ("type-merge", TypeMergeChunker(max_chars=1200)),
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


# ---------------------------------------------------------------------
# Step 4c wave 3.3 — rung 2 layers on the winner (offline, no mocks)
# ---------------------------------------------------------------------


def test_merge_rung2_flags_record_only_when_on() -> None:
    plain = MergeChunker(max_chars=1200)
    assert plain.params() == {"max_chars": 1200, "overlap": 0.15, "header": True}  # legacy identity intact
    assert "sentence_cuts" not in plain.chunk_config()
    assert "breadcrumb" not in plain.chunk_config()
    assert plain.describe() == "merge 1200/0.15/on"

    sent = MergeChunker(max_chars=1200, sentence_cuts=True)
    assert sent.params() == {"max_chars": 1200, "overlap": 0.15, "header": True, "layers": "sentences"}
    assert sent.chunk_config() == {
        "target_max_chars": 1200,
        "overlap_ratio": 0.15,
        "prepend_header": True,
        "sentence_cuts": True,
    }
    assert sent.describe() == "merge 1200/0.15/on +sentences"

    both = MergeChunker(max_chars=1200, sentence_cuts=True, breadcrumb=True)
    assert both.params() == {
        "max_chars": 1200,
        "overlap": 0.15,
        "header": True,
        "layers": "sentences-crumb",
    }
    assert both.describe() == "merge 1200/0.15/on +sentences +breadcrumb"

    with pytest.raises(ValueError, match="header"):
        MergeChunker(max_chars=1200, breadcrumb=True, header=False)


def test_sentence_split_prefers_sentence_ends_in_the_cut_window() -> None:
    text = " ".join(f"Sentence {number} tells a story." for number in range(1, 41))
    budget = 300
    overlap = int(budget * 0.15)

    pieces = sentence_split(text, budget, overlap)
    assert all(len(piece) <= budget for piece in pieces)
    for piece in pieces[:-1]:
        assert piece.endswith(".")  # every interior cut lands right after a sentence end
    assert pieces[1].startswith(pieces[0][-overlap:])  # the legacy overlap band is shared


def test_sentence_split_falls_back_to_the_exact_word_cut() -> None:
    unbreakable = "w" * 9000  # no spaces, no sentence ends — identical to the legacy cut
    assert sentence_split(unbreakable, 2400, 360) == _split_long(unbreakable, 2400, 360)

    # delimiters with no whitespace after them are not sentence ends — same fallback
    tricky = "a.b" * 3000
    assert sentence_split(tricky, 2400, 360) == _split_long(tricky, 2400, 360)


def test_merge_sentence_cuts_change_only_monster_piece_texts() -> None:
    monster = " ".join(f"Sentence {number} tells a story." for number in range(1, 121))
    paragraphs = [{"text": monster}]
    capture = _synthetic_capture(paragraphs)

    # the flags-off instance is byte-identical to the incumbent merge instance
    plain = MergeChunker(max_chars=1500, header=False).chunk(capture)
    assert plain == MergeChunker(max_chars=1500, header=False, sentence_cuts=False).chunk(capture)

    sent = MergeChunker(max_chars=1500, header=False, sentence_cuts=True).chunk(capture)
    assert [chunk.chunk_id for chunk in plain] == [chunk.chunk_id for chunk in sent]  # identity never moves
    assert [chunk.paragraph_ids for chunk in plain] == [chunk.paragraph_ids for chunk in sent]
    assert [chunk.text for chunk in plain] != [chunk.text for chunk in sent]  # the cuts moved to sentence ends
    assert all(len(chunk.text) <= 1500 for chunk in sent)
    assert sent  # the monster is over the 1500 budget — sentence cuts must engage
    for chunk in sent[:-1]:
        assert chunk.text.endswith(".")


def test_breadcrumb_replaces_the_template_slot_with_the_section() -> None:
    capture = _capture()  # the real Uwazi fixture — 23 typed headings
    plain = MergeChunker(max_chars=1200).chunk(capture)
    crumb = MergeChunker(max_chars=1200, breadcrumb=True).chunk(capture)

    assert [chunk.chunk_id for chunk in plain] == [chunk.chunk_id for chunk in crumb]  # identity never moves
    assert [chunk.paragraph_ids for chunk in plain] == [chunk.paragraph_ids for chunk in crumb]  # packing unchanged
    assert any(p.text != c.text for p, c in zip(plain, crumb))  # the fixture must gain crumbs

    # mirror the chunker's own crumb map from the shared partition — one rule, verified twice
    expected: dict[int, str] = {}
    for section in partition_sections(capture["paragraphs"]):
        head = section[0] if is_heading(capture["paragraphs"][section[0]]) else None
        if head is None:
            continue
        line = str(capture["paragraphs"][head]["text"]).splitlines()[0].strip()
        if line:
            expected.update((pid, line) for pid in section)
    for plain_chunk, crumb_chunk in zip(plain, crumb):
        expected_line = expected.get(plain_chunk.paragraph_ids[0])
        page = f" (page {plain_chunk.page_start})" if plain_chunk.page_start is not None else ""
        if expected_line is None:
            assert crumb_chunk.text.split("\n")[0] == plain_chunk.text.split("\n")[0]  # preamble: today's header
        else:
            assert crumb_chunk.text.split("\n")[0] == f"{capture['title']} — {expected_line}{page}"
            # the crumb is a header-slot swap: the body below it is untouched
            assert "\n".join(crumb_chunk.text.split("\n")[1:]) == "\n".join(plain_chunk.text.split("\n")[1:])


def test_build_chunks_rejects_rung2_flags_outside_merge() -> None:
    with pytest.raises(ValueError, match="sentence_cuts"):
        build_chunks(
            [{"text": "x"}],
            instance_key="k",
            shared_id="d",
            language="en",
            file_id="f",
            entity_title="T",
            template_name="X",
            split_mode="section",
            sentence_cuts=True,
        )
    with pytest.raises(ValueError, match="breadcrumb"):
        build_chunks(
            [{"text": "x"}],
            instance_key="k",
            shared_id="d",
            language="en",
            file_id="f",
            entity_title="T",
            template_name="X",
            split_mode="segment",
            breadcrumb=True,
        )
    with pytest.raises(ValueError, match="prepend_header"):
        build_chunks(
            [{"text": "x"}],
            instance_key="k",
            shared_id="d",
            language="en",
            file_id="f",
            entity_title="T",
            template_name="X",
            prepend_header=False,
            breadcrumb=True,
        )


def test_chunk_config_round_trips_the_rung2_layers() -> None:
    stored = MergeChunker(max_chars=1200, sentence_cuts=True, breadcrumb=True).chunk_config()
    config = ChunkConfig.from_store(stored)
    assert config.split_mode == "merge" and config.sentence_cuts and config.breadcrumb

    capture = _capture()
    assert MergeChunker(max_chars=1200, sentence_cuts=True, breadcrumb=True).chunk(capture) == capture_to_chunks(
        capture, **config_kwargs(config)
    )

    with pytest.raises(ValueError, match="store chunk_config is invalid"):
        ChunkConfig.from_store(
            {
                "target_max_chars": 1200,
                "overlap_ratio": 0.15,
                "prepend_header": True,
                "sentence_cuts": True,
                "split_mode": "section",
            }
        )

    legacy = ChunkConfig.from_store({"target_max_chars": 1200, "overlap_ratio": 0.15, "prepend_header": True})
    assert legacy.sentence_cuts is False and legacy.breadcrumb is False  # stores before wave 3.3

    type_stored = TypeMergeChunker(max_chars=1200, breadcrumb=True).chunk_config()
    type_config = ChunkConfig.from_store(type_stored)
    assert type_config.split_mode == "type-merge" and type_config.breadcrumb
    assert TypeMergeChunker(max_chars=1200, breadcrumb=True).chunk(capture) == capture_to_chunks(
        capture, **config_kwargs(type_config)
    )


# ---------------------------------------------------------------------
# Step 4c wave 3.4 — the type-aware merge arm (offline, no mocks)
# ---------------------------------------------------------------------


def test_type_merge_chunker_config_and_bytes() -> None:
    chunker = TypeMergeChunker(max_chars=1200)
    capture = _capture()

    assert chunker.name == "type-merge"
    assert chunker.params() == {"max_chars": 1200, "overlap": 0.15, "header": True}
    assert chunker.chunk_config() == {
        "target_max_chars": 1200,
        "overlap_ratio": 0.15,
        "prepend_header": True,
        "split_mode": "type-merge",
    }
    assert chunker.describe() == "type-merge 1200/0.15/on"
    assert chunker.chunk(capture) == capture_to_chunks(capture, **chunker.chunk_config())
    assert all(chunk.paragraph_ids for chunk in chunker.chunk(capture))
    assert chunker.chunk(capture) != MergeChunker(max_chars=1200).chunk(capture)  # the fixture mixes types


def test_type_merge_runs_break_at_content_type_changes() -> None:
    paragraphs = [
        {"text": "Body text one.", "type": "text"},
        {"text": "Footnote alpha.", "type": "footnote"},
        {"text": "Body text two.", "type": "text"},
    ]
    base: dict[str, Any] = {
        "instance_key": "k",
        "shared_id": "d",
        "language": "en",
        "file_id": "f",
        "entity_title": "T",
        "template_name": "X",
        "target_max_chars": 300,
        "prepend_header": False,
    }
    typed = build_chunks(paragraphs, **base, split_mode="type-merge")
    assert [chunk.paragraph_ids for chunk in typed] == [[0], [1], [2]]  # one run per type

    merged = build_chunks(paragraphs, **base, split_mode="merge")
    assert [chunk.paragraph_ids for chunk in merged] == [[0, 1, 2]]  # merge packs the three blindly together


def test_type_merge_glues_header_and_title_to_the_run_they_preface() -> None:
    paragraphs = [
        {"text": "Body text one.", "type": "text"},
        {"text": "I. SUMMARY", "type": "section header"},
        {"text": "Title box", "type": "title"},
        {"text": "Body text two.", "type": "text"},
    ]
    base: dict[str, Any] = {
        "instance_key": "k",
        "shared_id": "d",
        "language": "en",
        "file_id": "f",
        "entity_title": "T",
        "template_name": "X",
        "target_max_chars": 300,
        "prepend_header": False,
    }
    glue_chunks = build_chunks(paragraphs, **base, split_mode="type-merge")
    assert [chunk.paragraph_ids for chunk in glue_chunks] == [[0, 1, 2, 3]]  # header+title ride the body run
    assert glue_chunks == build_chunks(paragraphs, **base, split_mode="merge")  # single-type → byte-equal

    trailing = build_chunks(
        [
            {"text": "Body text one.", "type": "text"},
            {"text": "I. END", "type": "section header"},
        ],
        **base,
        split_mode="type-merge",
    )
    assert [chunk.paragraph_ids for chunk in trailing] == [[0], [1]]  # a trailing glue run keeps its own type


def test_type_merge_is_byte_equal_to_merge_on_typeless_documents() -> None:
    paragraphs = [{"text": "plain prose " * 130}, {"text": "more plain prose " * 5}]  # LBR-shaped: no types at all
    capture = _synthetic_capture(paragraphs)
    assert TypeMergeChunker(max_chars=1200).chunk(capture) == MergeChunker(max_chars=1200).chunk(capture)


def test_effective_types_glue_forward_to_the_body_they_preface() -> None:
    paragraphs = [
        {"text": "a", "type": "text"},
        {"text": "F.", "type": "footnote"},
        {"text": "H", "type": "section header"},
        {"text": "b", "type": "text"},
        {"text": "T", "type": "title"},
    ]
    effective = effective_types(paragraphs)
    # the header glues forward to the body text; the trailing title keeps its own type
    assert effective == {0: "text", 1: "footnote", 2: "text", 3: "text", 4: "title"}


def test_type_merge_composes_with_breadcrumb() -> None:
    chunker = TypeMergeChunker(max_chars=1200, breadcrumb=True)
    assert chunker.params() == {"max_chars": 1200, "overlap": 0.15, "header": True, "layers": "crumb"}
    assert chunker.chunk_config() == {
        "target_max_chars": 1200,
        "overlap_ratio": 0.15,
        "prepend_header": True,
        "split_mode": "type-merge",
        "breadcrumb": True,
    }
    assert chunker.describe() == "type-merge 1200/0.15/on +breadcrumb"

    with pytest.raises(ValueError, match="header"):
        TypeMergeChunker(max_chars=1200, breadcrumb=True, header=False)

    capture = _capture()  # the real fixture: 23 typed headings + footnote/list-item runs
    plain = TypeMergeChunker(max_chars=1200).chunk(capture)
    crumb = TypeMergeChunker(max_chars=1200, breadcrumb=True).chunk(capture)
    assert [chunk.chunk_id for chunk in plain] == [chunk.chunk_id for chunk in crumb]  # identity never moves
    assert [chunk.paragraph_ids for chunk in plain] == [chunk.paragraph_ids for chunk in crumb]  # runs unchanged
    assert any(p.text != c.text for p, c in zip(plain, crumb))  # the fixture gains crumbs
    for plain_chunk, crumb_chunk in zip(plain, crumb):
        if crumb_chunk.text != plain_chunk.text:
            # the crumb swaps the header's template slot only — the body below is untouched
            assert "\n".join(crumb_chunk.text.split("\n")[1:]) == "\n".join(plain_chunk.text.split("\n")[1:])
            assert crumb_chunk.text.split("\n")[0].startswith(f"{capture['title']} — ")
