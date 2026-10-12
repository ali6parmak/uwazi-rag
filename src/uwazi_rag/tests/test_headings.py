import json
from pathlib import Path

import pytest

from uwazi_rag.configuration import FIXTURES_DIR
from uwazi_rag.use_cases.chunking import build_chunks
from uwazi_rag.use_cases.headings import (
    ALL_CAPS_MAX_CHARS,
    is_heading,
    pack_sections,
    partition_sections,
    section_chars,
)
from uwazi_rag.use_cases.scan_headings import scan_home, scan_report

# --- the detector's frozen rules (PLAN.md Step 4c wave 3.0) -------------------------


def test_typed_paragraphs_head_by_type_not_content() -> None:
    assert is_heading({"text": "anything at all", "type": "Section header"})
    assert is_heading({"text": "still anything", "type": "section header"})  # matched case-insensitively
    assert is_heading({"text": "the document's own name", "type": "Title"})
    assert not is_heading({"text": "ARTICLE 5. DEFINITIONS", "type": "text"})  # types take precedence
    assert not is_heading({"text": "PART A", "type": "Page header"})
    assert not is_heading({"text": "See article 4 above", "type": "footnote"})


def test_typeless_marker_lines() -> None:
    assert is_heading({"text": "ARTICLE 5.2 — SCOPE"})
    assert is_heading({"text": "SECTION 1."})
    assert is_heading({"text": "§4 Deliverables"})
    assert is_heading({"text": "PART II"})
    assert is_heading({"text": "RECITALS:"})  # markers may carry terminal punctuation
    assert is_heading({"text": "SECTION"})  # a bare marker heads too
    # the \b guards the MARKER rule only: the caps rule still independently heads short
    # all-caps lines like "PARTIES" — both are headings under the frozen rules
    assert is_heading({"text": "PARTIES"})
    assert not is_heading({"text": "PARTIES and conditions"})  # suffix fails the marker rule, caps is out (mixed case)
    assert is_heading({"text": "ARTICLES OF ASSOCIATION"})  # via the caps rule, not the marker rule
    assert not is_heading({"text": "PARTLY cloudy skies"})  # mixed case — neither rule fires
    assert not is_heading({"text": "Article 5"})  # markers are uppercase only
    assert not is_heading({"text": "then SECTION 4 applies"})  # line-initial only


def test_typeless_ordinal_lines() -> None:
    assert is_heading({"text": "2.3 DEFINITIONS AND SCOPE"})
    assert is_heading({"text": "7 Term"})
    assert is_heading({"text": "1."})
    assert is_heading({"text": "10.1.2 Scope of supply"})
    assert is_heading({"text": "2019"})  # the pre-stated ordinal regex is literal — a bare year heads
    assert not is_heading({"text": "23andMe collects and stores the following"})  # word-bounded (option b, 2026-10-11)
    assert not is_heading({"text": "a2 file"})
    assert not is_heading({"text": "v2.0"})
    assert not is_heading({"text": "Terms 2.3 apply"})  # ordinals too are line-initial


def test_typeless_all_caps_lines() -> None:
    assert is_heading({"text": "SCOPE OF WORK AND DEFINITIONS"})
    assert is_heading({"text": "OK"})
    assert is_heading({"text": "SCOPE OF WORK\nbody prose stays unexamined"})  # first line only
    assert not is_heading({"text": "Scope of Work"})
    assert not is_heading({"text": "DEFINITIONS AND INTERPRETATION."})  # terminal punctuation is prose
    assert not is_heading({"text": "EXHIBITS AND SCHEDULES,"})
    assert not is_heading({"text": "WHEREAS:"})
    assert not is_heading({"text": "---"})
    assert not is_heading({"text": ""})
    assert not is_heading({"text": "   \n"})
    assert not is_heading({})
    assert not is_heading({"text": 5})  # non-string text never raises
    assert is_heading({"text": "A" * ALL_CAPS_MAX_CHARS})
    assert not is_heading({"text": "A" * (ALL_CAPS_MAX_CHARS + 1)})
    assert is_heading({"text": "12"})  # ordinal, not the caps rule (digits carry no letters)


def test_partition_sections_honors_types_and_gaps() -> None:
    paragraphs = [
        {"text": "Page header", "type": "Page header"},
        {"text": "Intro paragraph", "type": "text"},
        {"text": "Section header para", "type": "section header"},
        {"text": "Body", "type": "text"},
    ]
    assert partition_sections(paragraphs) == [[1], [2, 3]]  # dropped paragraph keeps its gap


def test_partition_sections_typeless_marker_split() -> None:
    paragraphs = [
        {"text": "Preamble"},
        {"text": "ARTICLE 1. DEFINITIONS"},
        {"text": "body one"},
        {"text": "SECTION 2. TERM"},
        {"text": "body two"},
    ]
    assert partition_sections(paragraphs) == [[0], [1, 2], [3, 4]]  # every heading starts a new section


def test_partition_sections_no_headings_is_one_section() -> None:
    assert partition_sections([{"text": "a"}, {"text": "b"}, {"text": "c"}]) == [[0, 1, 2]]


def test_partition_sections_leading_heading_makes_no_empty_first_section() -> None:
    assert partition_sections([{"text": "ARTICLE 1."}, {"text": "body"}]) == [[0, 1]]


def test_pack_sections_splits_at_paragraph_boundaries_at_the_budget() -> None:
    paragraphs = [{"text": "x" * 500}, {"text": "y" * 500}, {"text": "z" * 500}]
    assert pack_sections([[0, 1, 2]], paragraphs, 1200) == [[0, 1], [2]]


def test_pack_sections_over_budget_paragraph_stays_whole() -> None:
    paragraphs = [{"text": "x" * 1500}]
    assert pack_sections([[0]], paragraphs, 1200) == [[0]]  # no boundary inside the paragraph
    assert section_chars(paragraphs, [0]) == 1500  # the accepted over-budget cost the scan counts


def test_pack_sections_validates_budget() -> None:
    with pytest.raises(ValueError):
        pack_sections([[0]], [{"text": "x"}], 0)


def test_pack_matches_the_merge_grouping_when_there_are_no_headings() -> None:
    paragraphs = [{"text": "x" * 700}, {"text": "y" * 400}]
    packed = pack_sections([[0, 1]], paragraphs, 1200)
    merged = build_chunks(
        paragraphs,
        instance_key="k",
        shared_id="d",
        language="en",
        file_id="f",
        entity_title="T",
        template_name="X",
        target_max_chars=1200,
        overlap_ratio=0.15,
        prepend_header=False,
    )
    assert packed == [[0, 1]]
    assert [chunk.paragraph_ids for chunk in merged] == packed


# --- the offline scan (wave 3.0) ----------------------------------------------------


def _write_capture(home: Path, capture: dict) -> None:
    path = home / f"{capture['shared_id']}_{capture['language']}.json"
    path.write_text(json.dumps(capture), encoding="utf-8")


def _typeless_capture(instance: str, shared_id: str, paragraphs: list[dict]) -> dict:
    return {
        "instance_key": instance,
        "shared_id": shared_id,
        "language": "en",
        "title": shared_id,
        "template": {"id": "dataset", "name": "test-dataset"},
        "file": {"id": f"corpus/{shared_id}.txt", "name": f"{shared_id}.txt"},
        "segmentation_status": "ready",
        "fetched_at_utc": None,
        "paragraphs": paragraphs,
    }


def _typed_capture(instance: str, shared_id: str, paragraphs: list[dict]) -> dict:
    return {
        "instance_key": instance,
        "shared_id": shared_id,
        "language": "en",
        "title": shared_id,
        "template": {"id": "tmpl1", "name": "DOCUMENT"},
        "file": {"id": f"{shared_id}", "name": f"{shared_id}.pdf"},
        "segmentation_status": "ready",
        "fetched_at_utc": None,
        "paragraphs": paragraphs,
    }


def _tmp_raw(tmp_path: Path) -> tuple[Path, Path, Path]:
    """A raw dir with two single-instance homes: one typeless dataset doc, one typed Uwazi doc."""
    raw = tmp_path / "raw"
    typeless = raw / "aaaa"
    typed = raw / "zzzz"
    typeless.mkdir(parents=True)
    typed.mkdir()
    # Typeless dataset doc: a heading mid-merge-chunk, so the section partition differs.
    _write_capture(
        typeless,
        _typeless_capture(
            "aaaa",
            "a1",
            [
                {"text": "Preamble of the agreement."},
                {"text": "ARTICLE 1. SCOPE"},
                {"text": "y" * 700},
                {"text": "z" * 50},
                {"text": "ARTICLE 2. TERM"},
            ],
        ),
    )
    # Typed Uwazi doc: dropped box, typed heading — the same divergence through types.
    _write_capture(
        typed,
        _typed_capture(
            "zzzz",
            "b1",
            [
                {"text": "Header box", "type": "Page header"},
                {"text": "Intro", "type": "text"},
                {"text": "Chapter head", "type": "section header"},
                {"text": "Body text", "type": "text"},
            ],
        ),
    )
    return raw, typeless, typed


def test_scan_home_counts_deterministically(tmp_path: Path) -> None:
    _, typeless, typed = _tmp_raw(tmp_path)

    scan_a = scan_home(typeless)
    assert scan_a.dataset_id == "test-dataset"
    assert scan_a.budget == 1200  # unknown dataset id → the recorded uwazi leader default
    assert not scan_a.out_of_scope
    assert scan_a.captures == 1 and scan_a.captures_ready == 1 and scan_a.docs == 1
    assert scan_a.headings == 2 and scan_a.docs_with_headings == 1
    assert scan_a.heading_sources == {"type": 0, "regex": 2}
    # a1: sections [[0],[1,2,3],[4]] → 3 section chunks vs merge's one all-in chunk
    assert scan_a.section_chunks == 3 and scan_a.merge_chunks == 1
    assert scan_a.sections == 3
    assert scan_a.sections_over_budget == 0 and scan_a.sections_still_over_budget == 0
    assert scan_a.docs_partition_differs == 1
    assert [sample.doc for sample in scan_a.samples] == ["a1", "a1"]
    assert scan_a.paragraph_types == {"": 5}  # the whole home is typeless
    assert scan_a.section_chars_median is not None and scan_a.section_chars_p95 is not None

    scan_b = scan_home(typed)
    assert scan_b.dataset_id is None
    assert scan_b.budget == 1200
    assert scan_b.docs == 1 and scan_b.headings == 1 and scan_b.docs_with_headings == 1
    assert scan_b.heading_sources == {"type": 1, "regex": 0}
    assert scan_b.section_chunks == 2 and scan_b.merge_chunks == 1
    assert scan_b.docs_partition_differs == 1
    assert scan_b.samples and scan_b.samples[0].source == "type: section header"
    assert scan_b.paragraph_types == {"page header": 1, "text": 2, "section header": 1}


def test_scan_report_is_deterministic_and_labels_homes(tmp_path: Path) -> None:
    raw, _, _ = _tmp_raw(tmp_path)
    report = scan_report(raw)
    assert report == scan_report(raw)  # same data, same bytes — the record depends on it
    assert "test-dataset" in report and "uwazi (other)" in report  # a fixture key never matches the live .env instance
    assert "the gate does not apply here" in report  # no contract dataset in this fixture run
    assert "| test-dataset | 1200 | 1 | 1 | 100.0% | 1 | 100.0% | 100.0% | 3 | 26/768 | 3 | 1 | +2 |" in report
    assert "| uwazi (other) | 1200 | 1 | 1 | 100.0% | 1 | 100.0% | 100.0% | 2 |" in report
    assert "- paragraph-type census: text ×2, page header ×1, section header ×1" in report


def test_scan_home_uses_the_recorded_leader_geometry(tmp_path: Path) -> None:
    contractnli_home = tmp_path / "contractnli"
    contractnli_home.mkdir()
    capture = _typeless_capture("k1", "c1", [{"text": "plain text only"}])
    capture["template"] = {"id": "dataset", "name": "legalbenchrag-contractnli"}
    _write_capture(contractnli_home, capture)
    assert scan_home(contractnli_home).budget == 1200

    cuad_home = tmp_path / "cuad"
    cuad_home.mkdir()
    capture = _typeless_capture("k2", "c2", [{"text": "plain text only"}])
    capture["template"] = {"id": "dataset", "name": "legalbenchrag-cuad"}
    _write_capture(cuad_home, capture)
    assert scan_home(cuad_home).budget == 2400

    vic_home = tmp_path / "vic"
    vic_home.mkdir()
    capture = _typeless_capture("k3", "v1", [{"text": "passage"}])
    capture["template"] = {"id": "dataset", "name": "vic-chargebook"}
    _write_capture(vic_home, capture)
    vic = scan_home(vic_home)
    assert vic.budget == 4096 and vic.out_of_scope


def test_scan_on_real_captured_fixture_finds_typed_headings() -> None:
    scan = scan_home(FIXTURES_DIR)
    assert scan.dataset_id is None  # the fixtures are Uwazi captures, not a dataset home
    assert scan.captures == 3 and scan.captures_ready == 3 and scan.docs == 3
    assert scan.heading_sources["regex"] == 0  # typed paragraphs take precedence — regex never fires
    assert scan.heading_sources["type"] == scan.headings >= 23  # 22 section headers + 1 title on 64hnagcpvk
    assert scan.docs_partition_differs >= 1  # a typed heading inside a merged body chunk moves the partition
    assert scan.samples and scan.samples[0].source.startswith("type: ")
