"""Step 4a core-mapping tests: paragraph synthesis, span→anchor mapping, house rows.

Fully offline (AGENTS.md testing policy): strings in, spans/rows out, plain
assertions. The acceptance semantics (offset preservation, interval
intersection, golden-row shape) are the dataset adapters' shared science, so
they get their own pure test module.
"""

from __future__ import annotations

import json
from typing import Any

from uwazi_rag.adapters.datasets.core import (
    MANUAL_ORIGIN,
    UPSTREAM_ORIGIN,
    anchor_paragraph_ids,
    capture_paragraphs,
    make_dataset_capture,
    make_expected_block,
    make_golden_row,
    manual_row_problems,
    merge_manual_rows,
    span_text,
    synthesize_paragraphs,
)
from uwazi_rag.configuration import dataset_instance_key


def test_synthesize_partitions_the_text_exactly() -> None:
    text = "first line\nsecond line\nthird line"
    spans = synthesize_paragraphs(text)

    assert [(s, e) for s, e in spans] == [(0, 11), (11, 23), (23, 33)]
    # offset preservation: concatenating the spans reproduces the input byte-for-byte
    assert "".join(text[s:e] for s, e in spans) == text
    # each span's text ends at its newline (the newline belongs to its own line)
    assert text[11:23] == "second line\n"


def test_synthesize_trailing_newline_and_blank_segments() -> None:
    text = "a\n\n\nb"
    spans = synthesize_paragraphs(text)

    assert [text[s:e] for s, e in spans] == ["a\n", "\n", "\n", "b"]  # separator lines stay as own (empty) segments
    assert "".join(text[s:e] for s, e in spans) == text


def test_synthesize_empty_text_yields_no_paragraphs() -> None:
    assert synthesize_paragraphs("") == []
    # a lone newline is one whitespace-only segment — a partition slot the chunker will drop later
    assert synthesize_paragraphs("\n") == [(0, 1)]


def test_span_text_is_the_dataset_self_check() -> None:
    text = "Consider the answer here\nnext line"
    assert span_text(text, (0, 24)) == "Consider the answer here"
    assert span_text(text, (0, 25)) == "Consider the answer here\n"


def test_anchor_by_interval_intersection() -> None:
    spans = synthesize_paragraphs("alpha\nbeta\ngamma")  # (0,6) (6,11) (11,16)

    assert anchor_paragraph_ids(spans, (0, 5)) == [0]  # "alpha"
    assert anchor_paragraph_ids(spans, (2, 8)) == [0, 1]  # straddles the newline
    assert anchor_paragraph_ids(spans, (0, 16)) == [0, 1, 2]  # the whole text
    assert anchor_paragraph_ids(spans, (7, 10)) == [1]  # inside "beta"


def test_anchor_respects_half_open_boundaries() -> None:
    spans = synthesize_paragraphs("alpha\nbeta")  # line 0 = [0,6), line 1 = [6,10)

    assert anchor_paragraph_ids(spans, (0, 6)) == [0]  # ends exactly at line 1's start → line 0 only
    assert anchor_paragraph_ids(spans, (6, 10)) == [1]  # starts exactly at line 1's start


def test_anchor_rejects_impossible_and_unmapped_spans() -> None:
    spans = synthesize_paragraphs("alpha\nbeta")

    assert anchor_paragraph_ids(spans, (10, 10)) == []  # empty span: intersects nothing, no error
    # A partition covers everything, so an unmapped non-empty span is only
    # reachable when there are NO paragraphs to intersect (or a label bug).
    try:
        anchor_paragraph_ids([], (3, 9))
        raise AssertionError("expected ValueError")
    except ValueError as error:
        assert "no paragraph" in str(error)
    try:
        anchor_paragraph_ids(spans, (9, 3))  # start past end — upstream label bug
        raise AssertionError("expected ValueError")
    except ValueError as error:
        assert "past its end" in str(error)


def test_capture_paragraphs_and_expected_block_shape() -> None:
    text = "alpha\nbeta"
    paragraphs = capture_paragraphs(text, synthesize_paragraphs(text))

    assert paragraphs == [{"text": text[0:6]}, {"text": text[6:10]}]
    expected = make_expected_block(
        instance_key="ik",
        shared_id="doc",
        title="Doc",
        language="en",
        file_id="docs/doc.txt",
        paragraph_ids=[0, 1],
        text="alpha\nbeta",
    )
    assert list(expected.keys()) == [
        "instance_key",
        "shared_id",
        "title",
        "language",
        "file_id",
        "paragraph_ids",
        "text",
    ]


def test_golden_row_keeps_the_house_schema() -> None:
    expected = make_expected_block(
        instance_key="ik", shared_id="doc", title="Doc", language="en", file_id="f", paragraph_ids=[2], text="t"
    )
    row = make_golden_row(
        row_id="doc:q001",
        question="q?",
        origin=UPSTREAM_ORIGIN,
        query_language="en",
        source_group_id="doc",
        expected=expected,
    )

    assert list(row.keys()) == ["id", "question", "origin", "query_language", "source_group_id", "expected"]
    assert json.dumps(row, ensure_ascii=False)  # JSON-safe

    unanswerable = make_golden_row(
        row_id="m001", question="q?", origin=MANUAL_ORIGIN, query_language="en", source_group_id=None, expected=None
    )
    assert unanswerable["expected"] is None and unanswerable["source_group_id"] is None


def test_dataset_capture_mirrors_the_uwazi_shape_with_the_dataset_identity() -> None:
    capture = make_dataset_capture(
        dataset_id="legalbenchrag-privacyqa",
        shared_id="Fiverr",
        title="Fiverr",
        file_id="privacy_qa/Fiverr.txt",
        file_name="Fiverr.txt",
        paragraphs=[{"text": "a"}],
    )

    assert capture["instance_key"] == dataset_instance_key("legalbenchrag-privacyqa")
    assert capture["instance_key"] == "8a3f38ffd23a75e2"  # sha1("dataset:legalbenchrag-privacyqa")[:16]
    assert capture["template"] == {"id": "dataset", "name": "legalbenchrag-privacyqa"}
    assert capture["segmentation_status"] == "ready"
    assert capture["fetched_at_utc"] is None  # upstream-derived: no clock → byte-stable rebuilds
    assert list(capture.keys()) == [
        "instance_key",
        "shared_id",
        "language",
        "title",
        "template",
        "file",
        "segmentation_status",
        "fetched_at_utc",
        "paragraphs",
    ]
    assert "footnotes" not in capture  # legalbenchrag carries no such field


def test_dataset_capture_sidecar_footnotes_only_when_present() -> None:
    capture = make_dataset_capture(
        dataset_id="vic-chargebook",
        shared_id="1.1-c1-s1",
        title="1.1 Introductory Remarks",
        file_id="1.1-c1-s1",
        file_name="1.1 Introductory Remarks",
        paragraphs=[{"text": "body"}],
        footnotes="[^1]: See, e.g.",
    )
    assert capture["footnotes"] == "[^1]: See, e.g."

    none_sidecar = make_dataset_capture(
        dataset_id="vic-chargebook",
        shared_id="x",
        title="x",
        file_id="x",
        file_name="x",
        paragraphs=[{"text": "b"}],
        footnotes=None,
    )
    assert "footnotes" not in none_sidecar


def test_manual_row_problems_is_strict_but_accepts_good_unanswerables() -> None:
    golden = [
        make_golden_row(
            row_id="doc:q001",
            question="what here?",
            origin=UPSTREAM_ORIGIN,
            query_language="en",
            source_group_id="doc",
            expected=make_expected_block(
                instance_key="ik", shared_id="doc", title="t", language="en", file_id="f", paragraph_ids=[0], text="t"
            ),
        )
    ]
    good = {
        "id": "m001",
        "question": "What does the GDPR say about biometric data here?",
        "origin": "manual",
        "query_language": "en",
        "source_group_id": None,
        "expected": None,
    }
    assert manual_row_problems([good], golden_rows=golden) == []

    duplicates = dict(good, question="what here?")  # normalized duplicate of an upstream question
    bad_cases: list[dict[str, Any]] = [
        {**good, "origin": "synthetic"},
        {**good, "id": None},
        {**good, "id": "doc:q001"},  # collides with an upstream id
        {**good, "expected": {"anything": 1}},
        {**good, "source_group_id": "doc"},
        {**good, "query_language": "es"},
        {**good, "question": "  "},
        duplicates,
    ]
    problems = manual_row_problems(bad_cases, golden_rows=golden)
    assert len(problems) == len(bad_cases)
    assert "origin must be 'manual'" in problems[0]
    assert "id is required" in problems[1]
    assert "already used" in problems[2]
    assert "must be null" in problems[3]
    assert "must be null" in problems[4]
    assert "query_language" in problems[5]
    assert "question must be" in problems[6]
    assert "already asked" in problems[7]


def test_merge_manual_rows_appends_after_upstream() -> None:
    golden = [
        {
            "id": "a:q001",
            "question": "q",
            "origin": "upstream",
            "query_language": "en",
            "source_group_id": "a",
            "expected": None,
        }
    ]
    manual = [
        {
            "id": "m001",
            "question": "q2",
            "origin": "manual",
            "query_language": "en",
            "source_group_id": None,
            "expected": None,
        }
    ]

    merged = merge_manual_rows(golden, manual)
    assert merged[0] is golden[0] and merged[1] == manual[0]
    # upstream untouched — the merge is a copy, never a mutation
    assert len(golden) == 1
