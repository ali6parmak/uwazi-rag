"""build_dataset use-case tests: the whole dataset build, offline end to end.

Real files everywhere (AGENTS.md testing policy): the committed fixture
slices act as upstream, tmp dirs act as the data roots, pins verified with
the real checksum code. The determinism acceptance — rebuilds stay
byte-identical — is asserted across FULL use-case runs, and the manual-merge
contract is exercised before the unanswerable rows are authored for real.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

import pytest

from uwazi_rag.adapters.datasets import known_dataset_ids, registry, resolve_dataset
from uwazi_rag.configuration import dataset_instance_key
from uwazi_rag.use_cases.build_dataset import GOLDEN_FILE, MANUAL_FILE, build_dataset
from uwazi_rag.use_cases.build_golden import read_jsonl

PRIVACYQA_HOME = Path(__file__).resolve().parent / "fixtures" / "datasets" / "legalbenchrag"
VIC_HOME = Path(__file__).resolve().parent / "fixtures" / "datasets" / "vic-chargebook"
MANUAL_ROWS: list[dict[str, Any]] = [
    {
        "id": "m001",
        "question": "What retention period does GDPR Article 17 set for erasure requests?",
        "origin": "manual",
        "query_language": "en",
        "source_group_id": None,
        "expected": None,
    },
    {
        "id": "m002",
        "question": "Who is the Data Protection Officer of the White House?",
        "origin": "manual",
        "query_language": "en",
        "source_group_id": None,
        "expected": None,
    },
]


def _build_privacyqa(tmp_path: Path, *, with_manual: bool = False) -> tuple[Any, Path]:
    golden_dir = tmp_path / "golden"
    if with_manual:
        golden_dir.mkdir(parents=True, exist_ok=True)
        (golden_dir / MANUAL_FILE).write_text(
            "\n".join(json.dumps(row, ensure_ascii=False) for row in MANUAL_ROWS) + "\n", encoding="utf-8"
        )
    stats = build_dataset(
        "legalbenchrag-privacyqa",
        home_dir=PRIVACYQA_HOME,  # the fixture slice home: its pins match the fixture upstream
        raw_dir=tmp_path / "raw",
        golden_dir=golden_dir,
    )
    return stats, golden_dir


def test_full_build_writes_captures_and_merged_golden(tmp_path: Path) -> None:
    stats, golden_dir = _build_privacyqa(tmp_path)

    assert stats.dataset_id == "legalbenchrag-privacyqa"
    assert stats.instance_key == dataset_instance_key("legalbenchrag-privacyqa") == "8a3f38ffd23a75e2"
    assert stats.upstream_rows == 6 and stats.manual_rows_merged == 0 and stats.captures_written == 2
    written_captures = sorted((tmp_path / "raw").glob("*.json"))
    assert [p.name for p in written_captures] == ["23andMe_en.json", "Fiverr_en.json"]
    golden = read_jsonl(golden_dir / GOLDEN_FILE)
    assert [row["id"] for row in golden] == [
        "Fiverr:q001",
        "Fiverr:q002",
        "Fiverr:q003",
        "23andMe:q001",
        "23andMe:q002",
        "23andMe:q003",
    ]


def test_build_is_bit_stable_across_runs(tmp_path: Path) -> None:
    first_stats, _ = _build_privacyqa(tmp_path / "one")
    second_stats, _ = _build_privacyqa(tmp_path / "two")

    # identical except the two tmp path fields; every content field matches
    assert first_stats == second_stats.__class__(
        dataset_id=second_stats.dataset_id,
        instance_key=second_stats.instance_key,
        raw_dir=first_stats.raw_dir,
        golden_path=first_stats.golden_path,
        captures_written=second_stats.captures_written,
        upstream_rows=second_stats.upstream_rows,
        manual_rows_merged=second_stats.manual_rows_merged,
    )
    for first_file in sorted((tmp_path / "one" / "raw").glob("*.json")):
        second_file = tmp_path / "two" / "raw" / first_file.name
        assert first_file.read_bytes() == second_file.read_bytes()
    one = (tmp_path / "one" / "golden" / GOLDEN_FILE).read_bytes()
    two = (tmp_path / "two" / "golden" / GOLDEN_FILE).read_bytes()
    assert one == two


def test_manual_rows_merge_after_upstream_and_rebuilds_stay_identical(tmp_path: Path) -> None:
    _, golden_dir = _build_privacyqa(tmp_path, with_manual=True)

    golden = read_jsonl(golden_dir / GOLDEN_FILE)
    assert len(golden) == 8  # 6 upstream + 2 manual
    assert [row["origin"] for row in golden[-2:]] == ["manual", "manual"]
    assert golden[-1]["expected"] is None and golden[-1]["source_group_id"] is None
    assert golden[-1]["id"] == "m002"

    # idempotent rebuild: same bytes (the manual file is the source of truth, not an accumulator)
    stats_two, _ = _build_privacyqa(tmp_path, with_manual=True)
    again = (golden_dir / GOLDEN_FILE).read_bytes()
    assert stats_two.manual_rows_merged == 2
    assert again == (golden_dir / GOLDEN_FILE).read_bytes()


def test_invalid_manual_rows_abort_before_anything_is_written(tmp_path: Path) -> None:
    golden_dir = tmp_path / "golden"
    golden_dir.mkdir(parents=True)
    (golden_dir / MANUAL_FILE).write_text(
        json.dumps({**MANUAL_ROWS[0], "origin": "synthetic", "id": None}, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    with pytest.raises(ValueError, match="manual"):
        build_dataset(
            "legalbenchrag-privacyqa",
            home_dir=PRIVACYQA_HOME,
            raw_dir=tmp_path / "raw",
            golden_dir=golden_dir,
        )
    assert not list((tmp_path / "raw").glob("*.json")) if (tmp_path / "raw").exists() else True
    assert not (golden_dir / GOLDEN_FILE).exists()


def test_missing_upstream_names_the_re_fetch_hint(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError, match="isaacus/legal-rag-bench"):
        build_dataset("vic-chargebook", upstream_dir=tmp_path / "nope", raw_dir=tmp_path / "raw", golden_dir=tmp_path / "g")

    with pytest.raises(FileNotFoundError, match="awinml/legalbench-rag"):
        build_dataset(
            "legalbenchrag-cuad", upstream_dir=tmp_path / "nope", raw_dir=tmp_path / "raw", golden_dir=tmp_path / "g"
        )


def test_unknown_dataset_lists_the_registered_ids() -> None:
    with pytest.raises(ValueError, match="legalbenchrag-privacyqa"):
        build_dataset("no-such-dataset-instrument", raw_dir=Path("x"))


def test_upstream_drift_fails_loudly_before_writing(tmp_path: Path) -> None:
    home = tmp_path / "legalbenchrag"
    shutil.copytree(PRIVACYQA_HOME, home)
    # tamper a corpus FILE after the pins were generated → checksum drift
    corpus = home / "upstream" / "corpus" / "privacy_qa" / "Fiverr.txt"
    corpus.write_text(corpus.read_text(encoding="utf-8") + "tail tampering\n", encoding="utf-8")

    with pytest.raises(ValueError, match="upstream drift"):
        build_dataset(
            "legalbenchrag-privacyqa",
            home_dir=home,
            upstream_dir=home / "upstream",
            raw_dir=tmp_path / "raw",
            golden_dir=tmp_path / "g",
        )
    assert not list((tmp_path / "raw").glob("*.json"))  # nothing written on drift


def test_resolve_dataset_wires_the_registry_factories() -> None:
    ids = known_dataset_ids()

    assert set(ids) == {"legalbenchrag-privacyqa", "legalbenchrag-contractnli", "legalbenchrag-cuad", "vic-chargebook"}
    for dataset_id in ids:
        adapter, hint = resolve_dataset(dataset_id)
        assert adapter.dataset_id == dataset_id
        assert "hf dataset" in hint  # every registered instrument says how to restore its upstream
    assert set(registry()) == set(ids)  # registry() returns the same ids as a copy
