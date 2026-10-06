"""Step 4a — the vic-chargebook adapter (Isaacus's Legal RAG Bench).

The home's ``about.md`` (``data/datasets/vic-chargebook/about.md``) is the
contract: 4,876 PRE-CHUNKED Markdown passages ``{id, text, title, footnotes}``
+ 100 expert questions, one labeled relevant passage per question — so
retrieval currencies collapse to hit-rate/MRR at passage level BY DESIGN
(the corpus arrives pre-chunked; grading a chunker here would grade upstream).

Captures are PER PASSAGE with one paragraph each — the passage is the atomic
retrieval unit — and the gold anchor is that passage's single paragraph
position (0). The ``footnotes`` field decision (the one about.md edit this
adapter records): footnotes ride along verbatim in the capture as a sidecar
field, preserved for provenance and later attach/drop experiments, but are
NEVER chunked — a passage is graded as upstream ships it, so the instrument
stays faithful to the published benchmark until a sweep argues otherwise.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from uwazi_rag.adapters.datasets.base import DatasetBuildResult
from uwazi_rag.adapters.datasets.core import (
    UPSTREAM_ORIGIN,
    make_dataset_capture,
    make_expected_block,
    make_golden_row,
)
from uwazi_rag.adapters.datasets.pins import PinCheck, verify_pins
from uwazi_rag.configuration import DATA_DIR, dataset_instance_key

DATASET_ID = "vic-chargebook"
HOME_DIR_NAME = DATASET_ID
CORPUS_FILE = "corpus.jsonl"
QA_FILE = "qa.jsonl"


class VicChargebook:
    """The pre-chunked pass-through instrument: passages in, captures + gold rows out."""

    def __init__(self, *, home_dir: Path | None = None) -> None:
        self._dataset_id = DATASET_ID
        self._home_dir = home_dir  # fixture-slice override, like LegalBenchRagSource's

    @property
    def dataset_id(self) -> str:
        return self._dataset_id

    def home_dir(self) -> Path:
        return self._home_dir if self._home_dir is not None else DATA_DIR / "datasets" / HOME_DIR_NAME

    def upstream_dir(self) -> Path:
        return self.home_dir() / "upstream"

    def pin_labels(self) -> set[str]:
        return {f"file:{CORPUS_FILE}", f"file:{QA_FILE}"}

    def verify(self, upstream_dir: Path) -> list[PinCheck]:
        return verify_pins(self.home_dir() / "checksums.txt", upstream_dir, labels=self.pin_labels())

    def build(self, upstream_dir: Path) -> DatasetBuildResult:
        """One capture per passage; one golden row per question (its gold = paragraph 0).

        Deterministic: passage order is the corpus file's order; question rows
        are grouped by their labeled passage (first-appearance order), numbered
        q1..qn within it; no clock anywhere in the bytes.
        """
        pin_checks = self.verify(upstream_dir)
        passages: dict[str, dict[str, Any]] = {}
        passage_order: list[str] = []
        for row in _rows(upstream_dir / CORPUS_FILE):
            passage_id = str(row["id"])
            if not passage_id or "/" in passage_id:
                raise ValueError(f"{CORPUS_FILE}: passage id {passage_id!r} must be non-empty and slash-free")
            if passage_id in passages:
                raise ValueError(f"{CORPUS_FILE}: passage id {passage_id!r} appears twice — ids must be unique")
            passages[passage_id] = row
            passage_order.append(passage_id)

        instance_key = dataset_instance_key(self._dataset_id)
        captures: dict[str, dict[str, Any]] = {}
        for passage_id in passage_order:
            passage = passages[passage_id]
            title = str(passage["title"])
            capture = make_dataset_capture(
                dataset_id=self._dataset_id,
                shared_id=passage_id,
                title=title,
                file_id=passage_id,
                file_name=title,
                paragraphs=[{"text": str(passage["text"])}],
                footnotes=str(passage.get("footnotes", "")),
            )
            captures[f"{passage_id}_en.json"] = capture

        rows_per_passage: dict[str, list[dict[str, Any]]] = {}
        resolved_labels = 0
        for question in _rows(upstream_dir / QA_FILE):
            passage_id = str(question["relevant_passage_id"])
            gold_passage = passages.get(passage_id)
            if gold_passage is None:
                raise FileNotFoundError(
                    f"{QA_FILE}: question {str(question['id'])!r} labels passage {passage_id!r}, "
                    "which is not in the corpus — refusing to build a dangling label"
                )
            resolved_labels += 1
            rows_per_passage.setdefault(passage_id, []).append(
                make_golden_row(
                    row_id=f"{passage_id}:q{len(rows_per_passage[passage_id]) + 1:03d}",
                    question=str(question["question"]),
                    origin=UPSTREAM_ORIGIN,
                    query_language="en",
                    source_group_id=passage_id,
                    expected=make_expected_block(
                        instance_key=instance_key,
                        shared_id=passage_id,
                        title=str(gold_passage["title"]),
                        language="en",
                        file_id=passage_id,
                        paragraph_ids=[0],
                        text=str(gold_passage["text"]),
                    ),
                )
            )

        with_footnotes = sum(1 for passage_id in passage_order if passages[passage_id].get("footnotes"))
        return DatasetBuildResult(
            captures=captures,
            golden_rows=[row for rows in rows_per_passage.values() for row in rows],
            pin_checks=pin_checks,
            checks=resolved_labels,  # every label resolved into the corpus
            note=(f"{with_footnotes} passage(s) carry sidecar footnotes — preserved in the capture, never chunked"),
        )


def _rows(jsonl_path: Path) -> list[dict[str, Any]]:
    """Parse one upstream JSONL file line by line (deterministic file order)."""
    rows: list[dict[str, Any]] = []
    for number, line in enumerate(jsonl_path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as error:
            raise ValueError(f"{jsonl_path.name} line {number}: not valid JSON ({error})") from error
        if not isinstance(value, dict):
            raise ValueError(f"{jsonl_path.name} line {number}: expected a JSON object")
        rows.append(value)
    if not rows:
        raise ValueError(f"{jsonl_path.name}: empty upstream file — refusing to build an empty dataset")
    return rows
