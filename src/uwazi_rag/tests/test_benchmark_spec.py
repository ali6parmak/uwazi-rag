"""Benchmark-spec tests: TOML parsing, selection, store validity, plan + comparison.

Fully offline (AGENTS.md testing policy): TOML files on tmp_path, real
``NaiveVectorStore`` instances for the validity check, plain assertions. No
mocks — a store double here would bypass exactly the surface being tested.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import pytest

from uwazi_rag.adapters.naive_vector_store import NaiveVectorStore
from uwazi_rag.configuration import ROOT_PATH
from uwazi_rag.use_cases.benchmark import (
    BenchmarkSpecError,
    ExperimentResult,
    StoreSpec,
    describe_plan,
    format_chunk_cfg,
    parse_benchmark_toml,
    render_comparison,
    select_experiments,
    store_matches_spec,
)

VALID = """
[stores.baseline]
model = "bge-m3"
source = "data/naive_store.json"
max_chars = 1800
overlap = 0.15
header = true

[stores.merge-1200]
model = "bge-m3"
max_chars = 1200

[[experiments]]
name = "e1"
store = "baseline"

[[experiments]]
name = "e2"
store = "merge-1200"
"""


def _write(tmp_path: Path, text: str, name: str = "spec.toml") -> Path:
    path = tmp_path / name
    path.write_text(text, encoding="utf-8")
    return path


def test_parse_benchmark_toml_fills_defaults_and_keeps_the_file_name(tmp_path: Path) -> None:
    spec = parse_benchmark_toml(_write(tmp_path, VALID))

    assert spec.name == "spec"
    assert spec.stores["baseline"].is_source
    assert spec.stores["baseline"].source_path() == ROOT_PATH / "data/naive_store.json"
    assert spec.stores["merge-1200"].chunker == "merge"
    assert spec.stores["merge-1200"].max_chars == 1200
    assert spec.stores["merge-1200"].overlap == 0.15
    assert spec.stores["merge-1200"].header is True
    assert spec.experiments[0].retrieval == "embedding"
    assert spec.experiments[1].name == "e2"


def test_store_spec_source_path_resolves_absolute_and_errors_without_source() -> None:
    source = StoreSpec(slug="s", model="m", source="/tmp/hardcoded.json")
    assert source.source_path() == Path("/tmp/hardcoded.json")
    build = StoreSpec(slug="s", model="m")
    with pytest.raises(BenchmarkSpecError, match="no source"):
        build.source_path()


def test_parse_rejects_unknown_keys_dangling_references_and_empty_sections(tmp_path: Path) -> None:
    cases = [
        (
            '[stores.a]\nmodel = "m"\nstale = 1\n\n[[experiments]]\nname = "e"\nstore = "a"',
            r"unknown key\(s\) stale.*allowed: chunker, max_chars, overlap, header, model, source",
        ),
        (
            '[stores.a]\nmodel = "m"\n\n[[experiments]]\nname = "e"\nstore = "nope"',
            r"references store 'nope'",
        ),
        ('[stores.a]\nmodel = "m"', r"no \[\[experiments\]\]"),
        ("[[experiments]]\nname = 'e'\nstore = 'a'", r"no \[stores\.<slug>\]"),
        (
            '[stores.a]\nmodel = "m"\nchuncker = "merge"\n\n[[experiments]]\nname = "e"\nstore = "a"',
            r"unknown key\(s\) chuncker",
        ),
    ]
    for text, expected in cases:
        with pytest.raises(BenchmarkSpecError) as info:
            parse_benchmark_toml(_write(tmp_path, text, name=f"{abs(hash(text))}.toml"))
        assert re.search(expected, str(info.value)), (text, str(info.value))


def test_parse_rejects_unimplemented_strategies_and_junk_types(tmp_path: Path) -> None:
    with pytest.raises(BenchmarkSpecError, match="chunker 'section' is not implemented"):
        parse_benchmark_toml(
            _write(
                tmp_path,
                '[stores.a]\nmodel = "m"\nchunker = "section"\n\n[[experiments]]\nname = "e"\nstore = "a"',
                name="s1.toml",
            )
        )
    with pytest.raises(BenchmarkSpecError, match="retrieval 'bm25' is not implemented"):
        parse_benchmark_toml(
            _write(
                tmp_path,
                '[stores.a]\nmodel = "m"\n\n[[experiments]]\nname = "e"\nstore = "a"\nretrieval = "bm25"',
                name="s2.toml",
            )
        )
    with pytest.raises(BenchmarkSpecError, match="needs a model"):
        parse_benchmark_toml(_write(tmp_path, "[stores.a]\n\n[[experiments]]\nname = 'e'\nstore = 'a'", name="s3.toml"))
    with pytest.raises(BenchmarkSpecError, match="overlap"):
        parse_benchmark_toml(
            _write(
                tmp_path,
                '[stores.a]\nmodel = "m"\noverlap = 0.55\n\n[[experiments]]\nname = "e"\nstore = "a"',
                name="s4.toml",
            )
        )
    with pytest.raises(BenchmarkSpecError, match="max_chars"):
        parse_benchmark_toml(
            _write(
                tmp_path,
                '[stores.a]\nmodel = "m"\nmax_chars = 0\n\n[[experiments]]\nname = "e"\nstore = "a"',
                name="s5.toml",
            )
        )
    with pytest.raises(BenchmarkSpecError, match="header"):
        parse_benchmark_toml(
            _write(
                tmp_path,
                '[stores.a]\nmodel = "m"\nheader = "no"\n\n[[experiments]]\nname = "e"\nstore = "a"',
                name="s6.toml",
            )
        )
    with pytest.raises(BenchmarkSpecError, match="duplicated"):
        parse_benchmark_toml(
            _write(
                tmp_path,
                '[stores.a]\nmodel = "m"\n\n[[experiments]]\nname = "e"\nstore = "a"\n'
                '[[experiments]]\nname = "e"\nstore = "a"',
                name="s7.toml",
            )
        )


def test_select_experiments_filters_or_errors(tmp_path: Path) -> None:
    spec = _make_spec(tmp_path)
    assert [experiment.name for experiment in select_experiments(spec.experiments, only=None)] == ["e1", "e2"]
    assert [experiment.name for experiment in select_experiments(spec.experiments, only="e2")] == ["e2"]
    with pytest.raises(BenchmarkSpecError, match="no experiment named 'zz'"):
        select_experiments(spec.experiments, only="zz")


def _make_spec(tmp_path: Path) -> Any:
    return parse_benchmark_toml(_write(tmp_path, VALID, name="sel.toml"))


def test_store_matches_spec_checks_model_geometry_and_legacy_defaults() -> None:
    store = NaiveVectorStore(
        dimensions=2,
        embedding_model="m1",
        chunk_config={"target_max_chars": 900, "overlap_ratio": 0.1, "prepend_header": False},
    )
    assert store_matches_spec(store, StoreSpec(slug="s", model="m1", max_chars=900, overlap=0.1, header=False))
    assert not store_matches_spec(store, StoreSpec(slug="s", model="m2", max_chars=900, overlap=0.1, header=False))
    assert not store_matches_spec(store, StoreSpec(slug="s", model="m1", max_chars=800, overlap=0.1, header=False))
    assert not store_matches_spec(store, StoreSpec(slug="s", model="m1", max_chars=900, overlap=0.2, header=False))
    assert not store_matches_spec(store, StoreSpec(slug="s", model="m1", max_chars=900, overlap=0.1, header=True))

    # A legacy store (chunk_config absent) reads as Step 2 defaults — the committed
    # baseline reuse case — and as defaults-mismatch for any other geometry.
    legacy = NaiveVectorStore(dimensions=2, embedding_model="bge-m3", chunk_config=None)
    assert store_matches_spec(legacy, StoreSpec(slug="s", model="bge-m3"))
    assert not store_matches_spec(legacy, StoreSpec(slug="s", model="bge-m3", max_chars=1200))

    poisoned = NaiveVectorStore(
        dimensions=2,
        embedding_model="m1",
        chunk_config={"target_max_chars": 0, "overlap_ratio": 0.1, "prepend_header": True},
    )
    assert not store_matches_spec(poisoned, StoreSpec(slug="s", model="m1"))


def test_describe_plan_lists_the_grid_for_the_selected_experiments(tmp_path: Path) -> None:
    spec = _make_spec(tmp_path)
    selected = select_experiments(spec.experiments, only=None)
    store_paths = {"baseline": "data/naive_store.json", "merge-1200": "data/benchmark_stores/merge-1200.json"}

    lines = describe_plan(spec, selected, store_paths)
    text = "\n".join(lines)
    assert "2 experiment(s) over 2 store(s)" in text
    assert "baseline" in text and "reuse" in text and "data/naive_store.json" in text
    assert "merge-1200" in text and "build-or-skip" in text and "1200/0.15/on" in text
    assert "bge-m3 (merge)" in text
    assert "1. e1" in text and "2. e2" in text

    only_e2 = describe_plan(spec, select_experiments(spec.experiments, only="e2"), store_paths)
    assert "1 experiment(s) over 1 store(s)" in "\n".join(only_e2)
    assert not any("→ baseline" in line for line in only_e2)


def test_format_chunk_cfg_matches_the_scorecard_shorthand() -> None:
    assert format_chunk_cfg(max_chars=1800, overlap=0.15, header=True) == "1800/0.15/on"
    assert format_chunk_cfg(max_chars=600, overlap=0.0, header=False) == "600/0/off"


def _ok_result(name: str, build_seconds: float | None, run_seconds: float) -> ExperimentResult:
    return ExperimentResult(
        name=name,
        ok=True,
        model="bge-m3",
        cfg="1200/0.15/on",
        n=10,
        chunk_recall={1: 0.3, 5: 0.5, 10: 0.6},
        chunk_mrr=0.412,
        doc_recall={1: 0.7, 5: 0.9, 10: 1.0},
        doc_mrr=0.801,
        false_retrieval="0/3",
        build_seconds=build_seconds,
        run_seconds=run_seconds,
    )


def test_render_comparison_shares_one_row_per_experiment_and_marks_failures() -> None:
    results = [
        _ok_result("reused-store", None, 21.3),
        _ok_result("fresh-built", 141.7, 20.3),
        ExperimentResult(name="broken", ok=False, error="store X does not match its spec"),
    ]
    lines = render_comparison(results)
    text = "\n".join(lines)

    assert lines[0].startswith("| experiment | model | chunk cfg | n | ")
    for expected in (
        "chunk R@1",
        "chunk R@5",
        "chunk R@10",
        "chunk MRR",
        "doc R@1",
        "doc R@5",
        "doc R@10",
        "doc MRR",
        "false-retr",
        "build/score time",
    ):
        assert expected in lines[0]
    row_bare = (
        "| reused-store | bge-m3 | 1200/0.15/on | 10 | 30.0% | 50.0% | 60.0% | 0.412 |"
        " 70.0% | 90.0% | 100.0% | 0.801 | 0/3 |"
    )
    assert row_bare + " reuse / 21.3s |" in text
    assert row_bare.replace("reused-store", "fresh-built") + " 142s / 20.3s |" in text
    assert "> failed: broken — store X does not match its spec" in text
    # the failed row's metric cells are all dashes, no partial numbers
    assert "| broken | — | — | — |" in text


def test_render_comparison_omits_false_retrieval_for_non_cosine_methods() -> None:
    non_cosine = ExperimentResult(
        name="bm25",
        ok=True,
        model="bge-m3",
        cfg="1800/0.15/on",
        n=10,
        chunk_recall={1: 0.3, 5: 0.5, 10: 0.6},
        chunk_mrr=0.4,
        doc_recall={1: 0.7, 5: 0.9, 10: 1.0},
        doc_mrr=0.8,
        false_retrieval="—",
        run_seconds=3.0,
    )
    text = "\n".join(render_comparison([non_cosine]))
    assert "| bm25 |" in text and " | — | reuse / 3.0s |" in text
