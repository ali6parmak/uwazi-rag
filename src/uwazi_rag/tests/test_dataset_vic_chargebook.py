"""vic-chargebook adapter tests: per-passage captures + labeled gold, offline on a real slice.

Drives ``VicChargebook`` over the committed fixture slice (real corpus rows —
including a footnotes-carrying passage — plus the real qa rows that label
them). Pins the adapter contract: one capture per passage, ONE paragraph per
capture, gold anchor = paragraph 0, footnotes preserved-but-never-chunked,
rows grouped by labeled passage, deterministic bytes.
"""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

import pytest

from uwazi_rag.adapters.datasets.vic_chargebook import DATASET_ID, VicChargebook
from uwazi_rag.configuration import FIXTURES_DIR, dataset_instance_key
from uwazi_rag.use_cases.index_captures import capture_to_chunks

FIXTURE_HOME = FIXTURES_DIR / "datasets" / "vic-chargebook"


def _adapter(home: Path | None = None) -> VicChargebook:
    # no override → the fixture-slice home (its pins match the fixture slice)
    return VicChargebook(home_dir=home or FIXTURE_HOME)


def _write_pins(home: Path) -> None:
    """Regenerate pins from the home's own upstream slice (real digest code)."""
    lines = ["# regenerated pins (fixture slice)"]
    for name in ("corpus.jsonl", "qa.jsonl"):
        path = home / "upstream" / name
        lines.append(f"file {name} {hashlib.sha256(path.read_bytes()).hexdigest()}")
    (home / "checksums.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def test_build_over_the_fixture_slice() -> None:
    result = _adapter().build(FIXTURE_HOME / "upstream")

    corpus_rows = len((FIXTURE_HOME / "upstream" / "corpus.jsonl").read_text(encoding="utf-8").splitlines())
    qa_rows = len((FIXTURE_HOME / "upstream" / "qa.jsonl").read_text(encoding="utf-8").splitlines())
    assert len(result.captures) == corpus_rows
    assert len(result.golden_rows) == qa_rows == result.checks

    capture = result.captures[f"{result.golden_rows[0]['expected']['shared_id']}_en.json"]
    assert capture["instance_key"] == dataset_instance_key(DATASET_ID)
    assert capture["template"] == {"id": "dataset", "name": DATASET_ID}
    assert capture["segmentation_status"] == "ready"
    assert capture["fetched_at_utc"] is None
    assert len(capture["paragraphs"]) == 1  # one passage = one paragraph, by contract
    assert "footnotes" in capture  # the sidecar decision: preserved, never chunked

    row = result.golden_rows[0]
    expected = row["expected"]
    assert row["origin"] == "upstream" and row["query_language"] == "en" and row["source_group_id"] == expected["shared_id"]
    assert expected["file_id"] == expected["shared_id"]  # the passage is its own file, one-to-one
    assert expected["paragraph_ids"] == [0]  # the labeled passage IS the sole anchor
    assert expected["text"] == capture["paragraphs"][0]["text"]  # gold text = the passage, verbatim


def test_rows_group_by_labeled_passage_with_increasing_q_index(tmp_path: Path) -> None:
    """A passage with two questions gets q001/q002 — real code over a constructed second question."""
    home = tmp_path / "vic-chargebook"
    shutil.copytree(FIXTURE_HOME, home)
    qa_path = home / "upstream" / "qa.jsonl"
    questions = [json.loads(line) for line in qa_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    doubled = dict(questions[0], id="999")  # same passage asked twice (ids unique)
    qa_path.write_text("\n".join(json.dumps(q, ensure_ascii=False) for q in [*questions, doubled]) + "\n", encoding="utf-8")
    _write_pins(home)

    result = _adapter(home).build(home / "upstream")
    first_passage = str(questions[0]["relevant_passage_id"])
    ids = [row["id"] for row in result.golden_rows if row["expected"]["shared_id"] == first_passage]

    assert ids.count(f"{first_passage}:q001") == 1
    assert f"{first_passage}:q002" in ids


def test_dangling_label_aborts_the_build(tmp_path: Path) -> None:
    """A question whose labeled passage is not in the corpus refuses to build."""
    home = tmp_path / "vic-chargebook"
    shutil.copytree(FIXTURE_HOME, home)
    qa_path = home / "upstream" / "qa.jsonl"
    questions = [json.loads(line) for line in qa_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    questions[0]["relevant_passage_id"] = "no-such-passage-id"
    qa_path.write_text("\n".join(json.dumps(q, ensure_ascii=False) for q in questions) + "\n", encoding="utf-8")
    _write_pins(home)

    with pytest.raises(FileNotFoundError, match="dangling label"):
        _adapter(home).build(home / "upstream")


def test_determinism_same_upstream_same_bytes() -> None:
    first = _adapter().build(FIXTURE_HOME / "upstream")
    second = _adapter().build(FIXTURE_HOME / "upstream")

    assert first == second  # dataclass equality across capture maps, rows, pins, counts


def test_dataset_captures_chunk_through_the_shared_chunker() -> None:
    """Pass-through chunking: every capture yields exactly one chunk anchored to paragraph 0."""
    result = _adapter().build(FIXTURE_HOME / "upstream")

    for capture in list(result.captures.values())[:5]:
        chunks = capture_to_chunks(capture, target_max_chars=4096, overlap_ratio=0.0, prepend_header=True)
        assert len(chunks) == 1  # one passage, no split (all fixture passages ≤ 4096 chars)
        assert chunks[0].paragraph_ids == [0]
        assert chunks[0].instance_key == dataset_instance_key(DATASET_ID)
        assert chunks[0].text == f"{capture['title']} — {DATASET_ID}\n{capture['paragraphs'][0]['text'].strip()}"
