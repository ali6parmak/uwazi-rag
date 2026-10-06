"""legalbenchrag adapter tests: slicing a real upstream tree, offline (AGENTS.md testing policy).

Drives ``LegalBenchRagSource`` over the committed fixture slice (real corpus
files + a real benchmark slice + fixture pins) and over tmp copies of it for
the failure paths. Pins the contracts PLAN.md Step 4a names:

- the span self-check is the acceptance test (corrupt one answer → build aborts);
- offset-preserving synthesis → anchors by interval intersection (recomputed
  independently in the tests);
- determinism: two builds produce identical captures/golden rows;
- the NFC filename quirk resolves a benchmark reference that differs from disk.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import unicodedata
from pathlib import Path

import pytest

from uwazi_rag.adapters.datasets.core import anchor_paragraph_ids
from uwazi_rag.adapters.datasets.legalbenchrag import SOURCES, LegalBenchRagSource
from uwazi_rag.configuration import FIXTURES_DIR, dataset_instance_key
from uwazi_rag.use_cases.index_captures import capture_to_chunks

FIXTURE_HOME = FIXTURES_DIR / "datasets" / "legalbenchrag"


def _adapter(home: Path | None = None) -> LegalBenchRagSource:
    # no override → the fixture-slice home (its pins match the fixture slice)
    return LegalBenchRagSource("legalbenchrag-privacyqa", home_dir=home or FIXTURE_HOME)


def _write_pins(home: Path) -> None:
    """Regenerate a home's pins from its OWN upstream slice (real digest code, no mocking)."""
    upstream = home / "upstream"
    lines = ["# regenerated pins (fixture slice)"]
    for path in sorted((upstream / "benchmarks").glob("*.json")):
        lines.append(f"file   {path.relative_to(upstream)} {hashlib.sha256(path.read_bytes()).hexdigest()}")
    for directory in sorted(p for p in (upstream / "corpus").iterdir() if p.is_dir()):
        digest = hashlib.sha256()
        for corpus_file in sorted(directory.glob("*.txt")):
            digest.update(corpus_file.name.encode("utf-8"))
            digest.update(b"\0")
            digest.update(corpus_file.read_bytes())
        lines.append(f"corpus {directory.relative_to(upstream)} {digest.hexdigest()}")
    (home / "checksums.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def _line_spans(text: str) -> list[tuple[int, int]]:
    """The same offset-preserving partition, recomputed independently in the test."""
    starts = [0] + [index + 1 for index, char in enumerate(text) if char == "\n"]
    return [(start, next_) for start, next_ in zip(starts, [*starts[1:], len(text)], strict=True) if start < next_]


def _nfc(name: str) -> str:
    return unicodedata.normalize("NFC", name)


def test_source_ids_exclude_maud() -> None:
    assert set(SOURCES) == {"legalbenchrag-privacyqa", "legalbenchrag-contractnli", "legalbenchrag-cuad"}
    with pytest.raises(ValueError, match="MAUD is gated"):
        LegalBenchRagSource("legalbenchrag-maud")


def test_build_over_the_fixture_slice() -> None:
    result = _adapter().build(FIXTURE_HOME / "upstream")

    # two corpus files → two captures; six tests → six rows; 31 snippets self-checked
    assert set(result.captures) == {"23andMe_en.json", "Fiverr_en.json"}
    assert [row["id"] for row in result.golden_rows] == [
        "Fiverr:q001",
        "Fiverr:q002",
        "Fiverr:q003",
        "23andMe:q001",
        "23andMe:q002",
        "23andMe:q003",
    ]
    assert result.checks == 31
    assert all(row["origin"] == "upstream" for row in result.golden_rows)
    first = result.golden_rows[0]
    assert first["question"].startswith('Consider "Fiverr"')  # queries verbatim, upstream shape
    expected = first["expected"]
    assert expected["instance_key"] == dataset_instance_key("legalbenchrag-privacyqa")
    assert expected["file_id"] == "privacy_qa/Fiverr.txt"
    assert expected["language"] == "en"
    assert list(expected.keys()) == [
        "instance_key",
        "shared_id",
        "title",
        "language",
        "file_id",
        "paragraph_ids",
        "text",
    ]

    # capture shape: Uwazi-compatible, upstream-stable
    capture = result.captures["Fiverr_en.json"]
    assert capture["instance_key"] == expected["instance_key"]
    assert capture["segmentation_status"] == "ready"
    assert capture["fetched_at_utc"] is None
    assert capture["template"] == {"id": "dataset", "name": "legalbenchrag-privacyqa"}
    assert capture["file"] == {"id": "privacy_qa/Fiverr.txt", "name": "Fiverr.txt"}


def test_anchors_match_span_intersection_recomputed_from_the_slice() -> None:
    result = _adapter().build(FIXTURE_HOME / "upstream")
    tests = json.loads((FIXTURE_HOME / "upstream" / "benchmarks" / "privacy_qa.json").read_text(encoding="utf-8"))["tests"]

    for test in tests:
        file_path = _nfc(test["snippets"][0]["file_path"])
        span = _line_spans((FIXTURE_HOME / "upstream" / "corpus" / file_path).read_text(encoding="utf-8"))
        expected_anchors: list[int] = []
        for snippet in test["snippets"]:
            expected_anchors = sorted(
                set(expected_anchors) | set(anchor_paragraph_ids(span, (int(snippet["span"][0]), int(snippet["span"][1]))))
            )
        row = next(row for row in result.golden_rows if row["question"] == test["query"])
        assert row["expected"]["paragraph_ids"] == expected_anchors
        # anchors ascend, and every anchor line truly intersects one of the row's spans
        for paragraph_id in expected_anchors:
            start, end = span[paragraph_id]
            assert any(
                start < snippet_end and snippet_start < end
                for snippet in test["snippets"]
                for snippet_start, snippet_end in [(int(snippet["span"][0]), int(snippet["span"][1]))]
            )


def test_determinism_same_upstream_same_bytes(tmp_path: Path) -> None:
    first = _adapter().build(FIXTURE_HOME / "upstream")
    second = _adapter().build(FIXTURE_HOME / "upstream")

    assert first == second
    for name, capture in first.captures.items():
        one = json.dumps(capture, ensure_ascii=False, indent=2)
        two = json.dumps(second.captures[name], ensure_ascii=False, indent=2)
        assert one == two
    assert json.dumps(first.golden_rows, sort_keys=True) == json.dumps(second.golden_rows, sort_keys=True)


def test_corrupted_span_fails_the_self_check(tmp_path: Path) -> None:
    """The dataset's own check is the adapter's acceptance gate — tamper one answer, build aborts."""
    home = tmp_path / "legalbenchrag"
    shutil.copytree(FIXTURE_HOME, home)
    benchmarks = home / "upstream" / "benchmarks" / "privacy_qa.json"
    parsed = json.loads(benchmarks.read_text(encoding="utf-8"))
    parsed["tests"][0]["snippets"][0]["answer"] = "TAMPERED — does not match the span"
    benchmarks.write_text(json.dumps(parsed, ensure_ascii=False), encoding="utf-8")
    _write_pins(home)  # pins match the tampered file: only the span check can catch this

    with pytest.raises(ValueError, match="self-check"):
        _adapter(home).build(home / "upstream")


def test_nfd_referenced_file_is_resolved_through_nfc(tmp_path: Path) -> None:
    """The CUAD quirk, reconstructed: benchmark reference NFD, disk NFC — build must resolve it."""
    home = tmp_path / "legalbenchrag"
    upstream = home / "upstream"
    corpus_dir = upstream / "corpus" / "cuad"
    corpus_dir.mkdir(parents=True)
    disk_name = "LECLANCH\u00c9 S.A. - AGREEMENT.txt"  # NFC on disk
    text = "The Development Agreement grants broad license rights to the Joint Venture.\n"
    (corpus_dir / disk_name).write_text(text, encoding="utf-8")

    nfd_reference = "cuad/LECLANCHE\u0301 S.A. - AGREEMENT.txt"  # NFD in the benchmark JSON
    start, end = 4, 51  # "...Development Agreement grants broad license rights..."
    benchmarks_dir = upstream / "benchmarks"
    benchmarks_dir.mkdir()
    (benchmarks_dir / "cuad.json").write_text(
        json.dumps(
            {
                "tests": [
                    {
                        "query": "Consider the agreement; what license rights exist?",
                        "snippets": [{"file_path": nfd_reference, "span": [start, end], "answer": text[start:end]}],
                    }
                ]
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    _write_pins(home)

    adapter = LegalBenchRagSource("legalbenchrag-cuad", home_dir=home)
    result = adapter.build(upstream)

    assert result.checks == 1
    assert result.note == "1 filename(s) resolved through NFC normalization"
    capture = result.captures["LECLANCH\u00c9 S.A. - AGREEMENT_en.json"]
    assert capture["shared_id"] == "LECLANCH\u00c9 S.A. - AGREEMENT"
    assert capture["file"]["name"] == disk_name
    assert result.golden_rows[0]["id"] == "LECLANCH\u00c9 S.A. - AGREEMENT:q001"


def test_dataset_captures_chunk_through_the_shared_chunker() -> None:
    """The captures must be chunkable by the unchanged Step 2 machinery (identity preserved)."""
    result = _adapter().build(FIXTURE_HOME / "upstream")

    chunks = capture_to_chunks(result.captures["Fiverr_en.json"])
    assert chunks
    assert all(chunk.instance_key == dataset_instance_key("legalbenchrag-privacyqa") for chunk in chunks)
    assert all(chunk.language == "en" and chunk.file_id == "privacy_qa/Fiverr.txt" for chunk in chunks)
    assert all(chunk.paragraph_ids for chunk in chunks)  # provenance: every chunk names its line paragraphs
