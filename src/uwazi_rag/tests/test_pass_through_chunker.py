"""Pass-through chunker tests: fixed corpora keep the provenance + science-guard contracts.

Fully offline (AGENTS.md testing policy): plain assertions over constructed
captures. Two contracts are pinned:

1. one keepable paragraph → one chunk, never merged/split — the fixed-corpus
   (vic-chargebook) semantics;
2. on single-paragraph captures the method is byte-equal to the shared-chunker
   path under its own config — the same equivalence ``MergeChunker`` is pinned
   to, which is what makes grading's byte-verify guard hold.
"""

from __future__ import annotations

from typing import Any

import pytest

from uwazi_rag.use_cases.chunking import _header, build_chunks
from uwazi_rag.use_cases.chunking_methods import MergeChunker, PassThroughChunker
from uwazi_rag.use_cases.index_captures import capture_to_chunks


def _capture(paragraphs: list[str], page: int | None = None) -> dict[str, Any]:
    return {
        "instance_key": "ik1234567890ab",
        "shared_id": "1.1-c1-s1",
        "language": "en",
        "title": "1.1 Introductory Remarks",
        "template": {"id": "dataset", "name": "vic-chargebook"},
        "file": {"id": "1.1-c1-s1", "name": "1.1 Introductory Remarks"},
        "segmentation_status": "ready",
        "fetched_at_utc": None,
        "paragraphs": ([{"text": text} if page is None else {"text": text, "pageNumber": page} for text in paragraphs]),
    }


def test_pass_through_defaults_and_self_description() -> None:
    chunker = PassThroughChunker()

    assert chunker.name == "passthrough"
    assert chunker.params() == {"max_chars": 4096, "header": True}
    assert chunker.chunk_config() == {"target_max_chars": 4096, "overlap_ratio": 0.0, "prepend_header": True}
    assert chunker.describe() == "passthrough 4096/on"
    with pytest.raises(ValueError, match="max_chars"):
        PassThroughChunker(max_chars=0)


def test_one_paragraph_is_one_chunk_never_merged() -> None:
    capture = _capture(["first passage body", "second passage body"])

    chunks = PassThroughChunker().chunk(capture)

    assert len(chunks) == 2
    assert chunks[0].text.endswith("first passage body")
    assert chunks[1].text.endswith("second passage body")
    assert [chunk.paragraph_ids for chunk in chunks] == [[0], [1]]
    # identity mirrors the shared chunker's format, index by PRODUCED position
    assert chunks[0].chunk_id == "ik1234567890ab:1.1-c1-s1:en:1.1-c1-s1:0000"
    assert chunks[1].chunk_id == "ik1234567890ab:1.1-c1-s1:en:1.1-c1-s1:0001"

    merged = MergeChunker(max_chars=4096, overlap=0.0).chunk(capture)
    assert len(merged) == 1  # merge WOULD join them — the divergence is the method's point


def test_byte_equality_with_the_shared_chunker_on_single_paragraph_captures() -> None:
    """The science guard on the vic-chargebook shape: 1 paragraph/capture → identical output."""
    long_body = "# 1.1 Introductory Remarks\n\n\n\n1. A number of studies into the jury system " * 10
    capture = _capture([long_body])

    chunks = PassThroughChunker().chunk(capture)
    assert chunks == capture_to_chunks(capture, **PassThroughChunker().chunk_config())
    assert chunks == build_chunks(
        capture["paragraphs"],
        instance_key=capture["instance_key"],
        shared_id=capture["shared_id"],
        language=capture["language"],
        file_id=capture["file"]["id"],
        entity_title=capture["title"],
        template_name=capture["template"]["name"],
        target_max_chars=4096,
        overlap_ratio=0.0,
        prepend_header=True,
    )
    header = _header("1.1 Introductory Remarks", "vic-chargebook", None)
    assert chunks[0].text == f"{header}\n{long_body.strip()}"  # context header + verbatim body
    assert chunks[0].paragraph_ids == [0]  # provenance contract, single anchor


def test_page_numbers_are_honored_and_header_optionally_off() -> None:
    capture = _capture(["body text"], page=3)

    with_header = PassThroughChunker().chunk(capture)
    assert with_header[0].page_start == 3 and with_header[0].page_end == 3
    assert " (page 3)" in with_header[0].text and with_header[0].text.startswith("1.1 Introductory Remarks — vic-chargebook")

    bare = PassThroughChunker(header=False).chunk(capture)
    assert bare[0].text == "body text"  # verbatim body, nothing else


def test_whitespace_only_paragraphs_are_skipped_and_empty_captures_yield_nothing() -> None:
    capture = _capture(["real body"])
    capture["paragraphs"] = [{"text": "\n\n"}, {"text": "real body"}]

    chunks = PassThroughChunker().chunk(capture)
    assert len(chunks) == 1
    assert chunks[0].paragraph_ids == [1]  # the whitespace segment kept its slot (gap kept)

    assert PassThroughChunker().chunk(_capture([])) == []
    assert PassThroughChunker().chunk({"paragraphs": []}) == []
