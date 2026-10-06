"""Step 4a — the pure mapping core the dataset instruments share.

Everything here is offline-pure (AGENTS.md testing policy): text in, spans and
house-format rows out. The impure sides (upstream file parsing, checksum
verification, capture writing) live in the per-dataset adapter modules and in
:mod:`uwazi_rag.use_cases.build_dataset` — but ALL of the science (paragraph
synthesis, span→anchor mapping, golden-row shape) is in this module so it can
be tested as a unit.

The core contract (each home's ``about.md``):

- upstream corpus reads are Python text-mode ``utf-8`` (``Path.read_text``),
  never ``utf-8-sig`` — gold char-spans are text-mode offsets;
- gold spans are half-open ``[start, end)`` and the dataset self-checks:
  ``text[start:end] == snippet["answer"]``. The adapters run exactly this
  check as their acceptance test — correctness is verified, not assumed;
- paragraph synthesis is OFFSET-PRESERVING: paragraphs partition the raw text
  exactly, so a character index keeps the same meaning on both sides (upstream
  spans and our captures), whatever the paragraph rule is;
- golden rows use the house format every downstream consumer already relies on
  (``build_golden.make_golden_rows`` shape), with ``origin="upstream"`` for
  expert-labeled upstream questions and ``origin="manual"`` for hand-authored
  unanswerables (``expected: null`` — the false-retrieval lens).
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from uwazi_rag.configuration import dataset_instance_key
from uwazi_rag.use_cases.chunking import keepable

# Paragraph spans into the raw text, half-open [start, end) — the unit every
# anchor computation and every capture's ``paragraphs`` list is built from.
ParagraphSpan = tuple[int, int]

# House golden-row origins beyond the Uwazi golden's "synthetic": dataset rows
# quote their upstream expert labels; "manual" stays hand-authored unanswerables.
UPSTREAM_ORIGIN = "upstream"
MANUAL_ORIGIN = "manual"


def synthesize_paragraphs(text: str) -> list[ParagraphSpan]:
    """Split raw corpus text into an offset-preserving line partition.

    LegalBench-RAG's corpus files carry no blank lines — single ``\\n`` breaks
    between physical lines make them the honest atomic unit the gold offsets
    give us. Each line's raw span covers its trailing newline, and the spans
    partition ``[0, len(text))`` exactly: concatenating the spans' text in
    order reproduces the input byte-for-byte, so any upstream char-span keeps
    its meaning on both sides. Whitespace-only segments (consecutive breaks,
    an empty tail after a trailing newline) partition faithfully and are
    filtered later by the chunker's keep rule — their slot stays (gaps kept),
    exactly like Uwazi capture paragraphs.
    """
    starts = [0] + [index + 1 for index, char in enumerate(text) if char == "\n"]
    return [
        (start, next_start) for start, next_start in zip(starts, [*starts[1:], len(text)], strict=True) if start < next_start
    ]


def anchor_paragraph_ids(paragraph_spans: Sequence[ParagraphSpan], span: ParagraphSpan) -> list[int]:
    """Map a raw char-span ``[start, end)`` to the paragraph ids it intersects (pure).

    Strict interval intersection: paragraph ``k`` anchors the span iff
    ``para_start < span_end and span_start < para_end`` — a span never
    anchors an empty intersection, so a span ending exactly at a paragraph's
    start (or starting exactly at one's end) stays honest. A span straddling
    a newline anchors both lines — the upstream boundary text belongs to
    both, and over-anchoring is the safe direction for coverage.
    Returns ids in paragraph order (ascending), deduplicated.
    """
    span_start, span_end = span
    if span_start > span_end:
        raise ValueError(f"span start {span_start} is past its end {span_end} — upstream label bug")
    ids = [index for index, (start, end) in enumerate(paragraph_spans) if start < span_end and span_start < end]
    if span_start < span_end and not ids:
        raise ValueError(f"span [{span_start}, {span_end}) intersects no paragraph — synthesis does not cover the text")
    return ids


def span_text(text: str, span: ParagraphSpan) -> str:
    """The upstream snippet's own self-check, as a function: ``text[start:end]``."""
    return text[span[0] : span[1]]


def content_anchor_ids(text: str, paragraph_spans: Sequence[ParagraphSpan], span: ParagraphSpan) -> list[int]:
    """Intersecting paragraph ids the CHUNKER would keep — the golden anchors (pure).

    ``chunking.keepable``'s contract is one rule, two consumers: golden anchors
    must be the exact paragraphs the chunker uses, else coverage denominators
    count slots nothing can ever cover. A span straddling a blank line
    intersects a whitespace-only slot — that slot is dropped here, while the
    content-bearing neighbors on both sides carry the anchor. Raises when a
    non-empty span anchors no content at all (label bug or uncovered text).
    """
    ids = [
        pid
        for pid in anchor_paragraph_ids(paragraph_spans, span)
        if keepable({"text": text[paragraph_spans[pid][0] : paragraph_spans[pid][1]]})
    ]
    if span[0] < span[1] and not ids:
        raise ValueError(f"span [{span[0]}, {span[1]}) anchors no content-bearing paragraph — refusing a hollow gold set")
    return ids


def capture_paragraphs(text: str, spans: Sequence[ParagraphSpan]) -> list[dict[str, Any]]:
    """The capture's ``paragraphs`` list for one synthesized document.

    Uwazi capture shape (raw field names, ``build_chunks``-readable): one
    ``{"text": ...}`` per paragraph span, position = list index. No pages —
    raw corpus text has none, so chunk headers carry no page suffix.
    """
    return [{"text": text[start:end]} for start, end in spans]


def make_expected_block(
    *, instance_key: str, shared_id: str, title: str, language: str, file_id: str, paragraph_ids: Sequence[int], text: str
) -> dict[str, Any]:
    """The golden row's ``expected`` object — key order matches the house format."""
    return {
        "instance_key": instance_key,
        "shared_id": shared_id,
        "title": title,
        "language": language,
        "file_id": file_id,
        "paragraph_ids": list(paragraph_ids),
        "text": text,
    }


def make_golden_row(
    *,
    row_id: str,
    question: str,
    origin: str,
    query_language: str,
    source_group_id: str | None,
    expected: dict[str, Any] | None,
) -> dict[str, Any]:
    """One golden row in the schema every downstream consumer relies on.

    Same shape as ``build_golden.make_golden_rows`` output; ``expected=None``
    pairs with ``source_group_id=None`` to mark an unanswerable row — the
    false-retrieval lens demands real, corpus-absent topics for these.
    """
    return {
        "id": row_id,
        "question": question,
        "origin": origin,
        "query_language": query_language,
        "source_group_id": source_group_id,
        "expected": expected,
    }


def make_dataset_capture(
    *,
    dataset_id: str,
    shared_id: str,
    language: str = "en",
    title: str,
    file_id: str,
    file_name: str | None,
    paragraphs: Sequence[Mapping[str, Any]],
    footnotes: str | None = None,
) -> dict[str, Any]:
    """Assemble one dataset capture — the Uwazi capture shape, upstream-stable.

    Key order and field names mirror ``fetch_document.raw_capture_json`` so
    ``load_captures``/``capture_to_chunks``/``row_golds`` treat dataset
    captures exactly like Uwazi ones. Two deliberate differences, both
    byte-stability requirements (PLAN.md Step 4a determinism):

    - ``template`` is the synthetic ``{"id": "dataset", "name": dataset_id}``
      — it names the instrument in chunk context headers;
    - ``fetched_at_utc`` is ``None`` — a dataset capture is derived from a
      pinned upstream revision, not fetched live, and rebuilds must stay
      byte-identical.

    ``footnotes`` (vic-chargebook only) rides along verbatim as a sidecar
    field: preserved for provenance and later experiments, never chunked.
    """
    capture: dict[str, Any] = {
        "instance_key": dataset_instance_key(dataset_id),
        "shared_id": shared_id,
        "language": language,
        "title": title,
        "template": {"id": "dataset", "name": dataset_id},
        "file": {"id": file_id, "name": file_name},
        "segmentation_status": "ready",
        "fetched_at_utc": None,
        "paragraphs": list(paragraphs),
    }
    if footnotes is not None:
        capture["footnotes"] = footnotes
    return capture


def manual_row_problems(rows: Sequence[Mapping[str, Any]], *, golden_rows: Sequence[Mapping[str, Any]]) -> list[str]:
    """Why a dataset's hand-authored unanswerable rows cannot merge (empty = mergeable).

    Dataset manual rows are ALL unanswerables (``expected`` and
    ``source_group_id`` both null) — the upstream instruments have no
    built-in false-retrieval lens, these rows are it. Strict like the house
    ``merge_manual_rows``: problems abort the build before anything is
    written, and every row must be a top real corpus-absent topic (checking
    that is a human grep job, recorded in the manual file's provenance).
    """
    problems: list[str] = []
    taken_ids = {str(row["id"]) for row in golden_rows if row.get("id")}
    taken_questions = {" ".join(str(row.get("question") or "").split()).casefold() for row in golden_rows}
    for number, row in enumerate(rows, start=1):
        where = f"manual.jsonl line {number}"
        if row.get("origin") != MANUAL_ORIGIN:
            problems.append(f"{where}: origin must be {MANUAL_ORIGIN!r} (has {row.get('origin')!r})")
        if row.get("expected") is not None or row.get("source_group_id") is not None:
            problems.append(f"{where}: dataset manual rows are unanswerables — expected and source_group_id must be null")
        question = row.get("question")
        if not isinstance(question, str) or not question.strip():
            problems.append(f"{where}: question must be a non-empty string")
        elif " ".join(question.split()).casefold() in taken_questions:
            problems.append(f"{where}: question already asked by the upstream rows")
        row_id = row.get("id")
        if row_id is None:
            problems.append(f"{where}: id is required for dataset manual rows (house style m<NNN>)")
        elif not isinstance(row_id, str) or not row_id.strip():
            problems.append(f"{where}: id must be a non-empty string when present")
        elif row_id in taken_ids:
            problems.append(f"{where}: id {row_id!r} is already used — ids must be unique")
        if row.get("query_language") != "en":
            problems.append(f"{where}: query_language must be 'en' (both instruments are English-only for now)")
    return problems


def merge_manual_rows(golden_rows: list[dict[str, Any]], manual_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    """Append validated hand-authored rows after the upstream rows (deterministic)."""
    return [*golden_rows, *(dict(row) for row in manual_rows)]
