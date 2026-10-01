import json

from uwazi_rag.configuration import FIXTURES_DIR
from uwazi_rag.use_cases.chunking import (
    OVERLAP_RATIO,
    TARGET_MAX_CHARS,
    TARGET_MIN_CHARS,
    _split_long,
    build_chunks,
    keepable,
)

FIXTURES = ["64hnagcpvk_en.json", "ar22d4v4i5s_en.json", "ar22d4v4i5s_es.json"]


def _capture(name: str) -> dict:
    capture: dict = json.loads((FIXTURES_DIR / name).read_text(encoding="utf-8"))
    return capture


def _chunks(name: str) -> list:
    capture = _capture(name)
    return build_chunks(
        capture["paragraphs"],
        instance_key=capture["instance_key"],
        shared_id=capture["shared_id"],
        language=capture["language"],
        file_id=capture["file"]["id"],
        entity_title=capture["title"],
        template_name=capture["template"]["name"],
    )


def test_no_text_is_lost_from_real_fixtures() -> None:
    for name in FIXTURES:
        capture = _capture(name)
        expected = "\n".join(p["text"].strip() for p in capture["paragraphs"] if keepable(p))
        actual = "\n".join("\n".join(chunk.text.split("\n")[1:]) for chunk in _chunks(name))
        assert actual == expected, name


def test_chunk_bodies_stay_within_target_max() -> None:
    for name in FIXTURES:
        bodies = [chunk.text.split("\n", 1)[1] for chunk in _chunks(name)]
        assert bodies, name
        assert max(len(body) for body in bodies) <= TARGET_MAX_CHARS, name


def test_chunks_have_a_context_header_with_title_and_page() -> None:
    for name in FIXTURES:
        capture = _capture(name)
        for chunk in _chunks(name):
            first_line = chunk.text.split("\n", 1)[0]
            assert first_line.startswith(capture["title"]), name
            if chunk.page_start is not None:
                assert first_line.endswith(f"(page {chunk.page_start})"), name
            assert capture["template"]["name"] in first_line, name


def test_identity_is_deterministic_and_sequential() -> None:
    for name in FIXTURES:
        capture = _capture(name)
        chunks = _chunks(name)
        assert [c.chunk_index for c in chunks] == list(range(len(chunks)))
        assert len({c.chunk_id for c in chunks}) == len(chunks)
        for chunk in chunks:
            assert chunk.chunk_id.startswith(capture["instance_key"])
            assert chunk.instance_key == capture["instance_key"]
            assert chunk.language == capture["language"]
            assert chunk.file_id == capture["file"]["id"]
        rebuilt = _chunks(name)
        assert [c.model_dump() for c in rebuilt] == [c.model_dump() for c in chunks]


def test_page_ranges_are_consistent() -> None:
    for name in FIXTURES:
        capture = _capture(name)
        pages = [p["pageNumber"] for p in capture["paragraphs"] if p.get("pageNumber") is not None and keepable(p)]
        for chunk in _chunks(name):
            if chunk.page_start is not None:
                assert chunk.page_start <= chunk.page_end
                assert chunk.page_start >= min(pages)
                assert chunk.page_end <= max(pages)


def test_long_paragraphs_split_with_about_fifteen_percent_overlap() -> None:
    long_text = "the witness testified about the raid " * 100  # 3700 chars, wordy
    pieces = _split_long(long_text)
    overlap_chars = int(TARGET_MAX_CHARS * OVERLAP_RATIO)
    assert len(pieces) >= 2
    assert all(len(piece) <= TARGET_MAX_CHARS for piece in pieces)
    for previous, following in zip(pieces, pieces[1:]):
        assert following[:overlap_chars] == previous[-overlap_chars:]


def test_short_paragraphs_stay_in_one_piece() -> None:
    assert _split_long("a short paragraph") == ["a short paragraph"]


def test_tiny_paragraphs_merge_into_a_single_bounded_chunk() -> None:
    paragraphs = [{"text": f"Paragraph {i} says something real and useful. " * 3, "pageNumber": i + 1} for i in range(8)]
    chunks = build_chunks(
        paragraphs,
        instance_key="2bf0fa1d7db9ecd6",
        shared_id="aaaaaa1111",
        language="en",
        file_id="ffffffff11",
        entity_title="Tiny doc",
        template_name="Report",
    )
    assert len(chunks) == 1
    assert TARGET_MIN_CHARS * 0.3 < len(chunks[0].text.split("\n", 1)[1]) < TARGET_MAX_CHARS


def test_page_furniture_and_empty_boxes_are_dropped() -> None:
    paragraphs = [
        {"type": "Picture", "pageNumber": 1, "text": ""},
        {"type": "Page header", "pageNumber": 2, "text": "Serie A No. 2"},
        {"type": "Page footer", "pageNumber": 2, "text": "www.example.org"},
        {"type": "Text", "pageNumber": 2, "text": "The real content lives here."},
    ]
    chunks = build_chunks(
        paragraphs,
        instance_key="2bf0fa1d7db9ecd6",
        shared_id="aaaaaa1111",
        language="en",
        file_id="ffffffff11",
        entity_title="Doc",
        template_name="Report",
    )
    assert len(chunks) == 1
    assert "Serie A No. 2" not in chunks[0].text
    assert "www.example.org" not in chunks[0].text
    assert "The real content" in chunks[0].text.split("\n", 1)[1]
    assert chunks[0].page_start == 2 and chunks[0].page_end == 2


def test_empty_input_produces_no_chunks() -> None:
    chunks = build_chunks(
        [{"type": "Picture", "pageNumber": 1, "text": ""}],
        instance_key="2bf0fa1d7db9ecd6",
        shared_id="aaaaaa1111",
        language="en",
        file_id="ffffffff11",
        entity_title="Doc",
        template_name="Report",
    )
    assert chunks == []
