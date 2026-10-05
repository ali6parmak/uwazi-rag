"""Sweep-runner tests: the whole orchestration helper, driven offline end-to-end.

Real files everywhere (AGENTS.md testing policy): tmp captures + real chunker
+ real ``NaiveVectorStore`` stores + the deterministic ``HashingEmbedding``
factory (its ``.model`` is ``"hashing"`` and the cells all name that model, so
the store-model guard passes honestly). No mocks, no Ollama, no Uwazi — the
assertion set covers build-or-skip caching via readable content-derived store
names (slugs + corpus digest8), plan/results.md
appends with visible settings, failure recording, selection, and number parity
between a sweep experiment and the shared grading path.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import pytest

from uwazi_rag import configuration
from uwazi_rag.adapters.naive_vector_store import NaiveVectorStore
from uwazi_rag.ports.embedding_port import EmbeddingPort
from uwazi_rag.tests.hash_embedding import HashingEmbedding
from uwazi_rag.use_cases.chunking_methods import MergeChunker
from uwazi_rag.use_cases.eval_retrieval import score_rows
from uwazi_rag.use_cases.eval_run import prepare_run, rank_rows
from uwazi_rag.use_cases.fetch_document import raw_capture_json
from uwazi_rag.use_cases.retrieval_methods import Bm25Retrieval, EmbeddingRetrieval, RrfRetrieval
from uwazi_rag.use_cases.run_sweep import (
    StoreCell,
    SweepExperiment,
    SweepSpecError,
    corpus_digest,
    define_sweep,
    load_sweep_spec,
    run_sweep,
    select_sweep_experiments,
    store_file_name,
)

DIMENSIONS = 32
INSTANCE = "sweep0123456789"

EN_PARAGRAPHS = [
    "Short opening line about the night raid on the village bridge.",
    "Witnesses described the night raid with exact times and unit insignia. " + "raid unit insignia " * 150,
    "The commission recorded the detentions in its annex and cross-checked the register.",
]
ES_PARAGRAPHS = [
    "Los testigos describieron el asalto nocturno al puente con horas y siglas de la unidad.",
    "La comisión registró las detenciones en su anexo y cotejó las entradas del registro. " * 2,
]
DECOY_PARAGRAPHS = [
    "Maritime insurance arbitration clauses dominate the annexes of the shipping contract dispute.",
    "The carrier liability ceiling was renegotiated under the freight forwarding agreement. " * 4,
]


def _capture(shared_id: str, language: str, title: str, paragraph_texts: list[str]) -> dict[str, Any]:
    paragraphs = [{"type": "Text", "pageNumber": 1 + index // 2, "text": text} for index, text in enumerate(paragraph_texts)]
    return raw_capture_json(
        shared_id=shared_id,
        language=language,
        instance_key=INSTANCE,
        title=title,
        template_id="t0",
        template_name="IACHR Report",
        file_id=f"f1f1f1{shared_id}",
        file_name="report.pdf",
        segmentation_status="ready",
        paragraphs=paragraphs,
    )


def _factory(_model: str) -> EmbeddingPort:
    """Real embedder factory (the tests' deterministic one); cells name its model."""
    return HashingEmbedding(dimensions=DIMENSIONS)


@pytest.fixture()
def grid(tmp_path: Path) -> tuple[Path, Path, Path, Path, list[SweepExperiment]]:
    """The tiny corpus + golden file + default sweep: 2 cells × 2 retrieval methods."""
    raw_dir = tmp_path / "raw"
    en = _capture("docen3333", "en", "Night Raid Report", EN_PARAGRAPHS)
    es = _capture("doces3333", "es", "Informe del asalto", ES_PARAGRAPHS)
    decoy = _capture("decoy3333", "en", "Shipping Contract Report", DECOY_PARAGRAPHS)
    raw_dir.mkdir(parents=True)
    for capture in (en, es, decoy):
        path = raw_dir / f"{capture['shared_id']}_{capture['language']}.json"
        path.write_text(json.dumps(capture, ensure_ascii=False), encoding="utf-8")

    rows = [
        {
            "id": "q-en",
            "question": EN_PARAGRAPHS[0],
            "origin": "synthetic",
            "query_language": "en",
            "source_group_id": "g-en",
            "expected": {
                "instance_key": INSTANCE,
                "shared_id": "docen3333",
                "language": "en",
                "title": "Night Raid Report",
                "file_id": "f1f1f1docen3333",
                "paragraph_ids": [0],
                "text": "irrelevant",
            },
        },
        {
            "id": "q-es",
            "question": ES_PARAGRAPHS[0],
            "origin": "synthetic",
            "query_language": "en",  # cross-language row: asked in en, gold is es
            "source_group_id": "g-es",
            "expected": {
                "instance_key": INSTANCE,
                "shared_id": "doces3333",
                "language": "es",
                "title": "Informe del asalto",
                "file_id": "f1f1f1doces3333",
                "paragraph_ids": [0],
                "text": "irrelevant",
            },
        },
        {"id": "q-un", "question": "quantum flux monitoring instrumentation grid", "origin": "manual", "expected": None},
    ]
    golden_path = tmp_path / "golden.jsonl"
    golden_path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows), encoding="utf-8")

    cells = [
        StoreCell(label="a-default", chunk_method=MergeChunker(), model="hashing"),
        StoreCell(label="b-noheader", chunk_method=MergeChunker(header=False), model="hashing"),
    ]
    experiments = define_sweep(cells, [EmbeddingRetrieval(), Bm25Retrieval()])
    return tmp_path, raw_dir, golden_path, tmp_path / "results.md", experiments


def _run(
    grid: tuple[Path, Path, Path, Path, list[SweepExperiment]],
    results_path: Path,
    **kwargs: Any,
) -> int:
    tmp_path, raw_dir, golden_path, _default_results, experiments = grid
    return run_sweep(
        name="unit-grid",
        experiments=experiments,
        embedder_factory=_factory,
        source=raw_dir,
        stores_dir=tmp_path / "benchmark_stores",
        results_path=results_path,
        golden_path=golden_path,
        **kwargs,
    )


def _comparison_rows(text: str, name: str) -> list[str]:
    """A comparison-table data row (lines starting with the experiment name)."""
    return [line for line in text.splitlines() if line.startswith(f"| {name} |")]


def test_run_sweep_builds_grades_and_appends_the_full_run(
    grid: tuple[Path, Path, Path, Path, list[SweepExperiment]],
) -> None:
    tmp_path, _raw_dir, _golden, results_path, _experiments = grid
    stores_dir = tmp_path / "benchmark_stores"

    code = _run(grid, results_path)
    assert code == 0

    store_files = sorted(stores_dir.glob("*.json"))
    assert len(store_files) == 2  # two cells → two fingerprint-addressed stores
    for store_file in store_files:
        loaded = NaiveVectorStore.load(store_file)
        assert loaded.embedding_model == "hashing"
        assert loaded.chunk_config in (
            MergeChunker().chunk_config(),
            MergeChunker(header=False).chunk_config(),
        )

    text = results_path.read_text(encoding="utf-8")
    collapsed = re.sub(r" +", " ", text)
    # resolved plan at run start, settings visible
    assert "— benchmark unit-grid — resolved plan" in text
    assert "merge 1800/0.15/on × hashing" in collapsed
    assert "merge 1800/0.15/off × hashing" in collapsed
    assert "plan    : unit-grid — 4 experiment(s) over 2 store cell(s)" in text
    # one labeled block per experiment, graded facts + retrieval settings from the instances
    assert "benchmark unit-grid: a-default-embedding" in text
    assert "benchmark unit-grid: b-noheader-bm25" in text
    assert "retrieval: embedding" in text
    assert "retrieval: bm25 k1=1.2 b=0.75" in text
    assert "false-retrieval is cosine-specific" in text  # the non-cosine note survives
    # comparison table: settings in the cells, no failures
    assert "| a-default-embedding | hashing | 1800/0.15/on | embedding | " in text
    assert "| a-default-bm25 | hashing | 1800/0.15/on | bm25 k1=1.2 b=0.75 | " in text
    assert "> failed:" not in text
    assert "— benchmark unit-grid — comparison (4 experiments)" in text


def test_second_run_skips_valid_stores_and_reproduces_the_numbers(
    grid: tuple[Path, Path, Path, Path, list[SweepExperiment]],
) -> None:
    tmp_path, _raw_dir, _golden, results_path, _experiments = grid
    first_results = tmp_path / "results-first.md"
    assert _run(grid, first_results) == 0
    assert _run(grid, results_path) == 0

    first = first_results.read_text(encoding="utf-8")
    second = results_path.read_text(encoding="utf-8")
    for name in ("a-default-embedding", "a-default-bm25", "b-noheader-embedding", "b-noheader-bm25"):
        first_rows = [line for line in first.splitlines() if line.startswith(f"| {name} |")]
        second_rows = [line for line in second.splitlines() if line.startswith(f"| {name} |")]
        assert len(first_rows) == 1 and len(second_rows) == 1
        first_cells = first_rows[0].split(" | ")
        second_cells = second_rows[0].split(" | ")
        assert first_cells[:-1] == second_cells[:-1], name  # identical graded numbers
        assert second_cells[-1].startswith("reuse /")  # the store was skipped, not rebuilt


def test_rebuilt_stores_yield_identical_numbers(
    grid: tuple[Path, Path, Path, Path, list[SweepExperiment]],
) -> None:
    tmp_path, _raw_dir, _golden, results_path, _experiments = grid
    first_results = tmp_path / "results-first.md"
    assert _run(grid, first_results) == 0

    for store_file in (tmp_path / "benchmark_stores").glob("*.json"):
        store_file.unlink()

    assert _run(grid, results_path) == 0  # the sweep reclaims them silently — caching is invisible

    first = first_results.read_text(encoding="utf-8")
    again = results_path.read_text(encoding="utf-8")
    for name in ("a-default-embedding", "b-noheader-bm25"):
        first_row = next(line for line in first.splitlines() if line.startswith(f"| {name} |")).split(" | ")
        again_row = next(line for line in again.splitlines() if line.startswith(f"| {name} |")).split(" | ")
        assert first_row[:-1] == again_row[:-1], name  # deterministic rebuild → identical numbers


def test_dry_run_prints_the_plan_and_writes_nothing(
    grid: tuple[Path, Path, Path, Path, list[SweepExperiment]],
) -> None:
    tmp_path, _raw_dir, _golden, results_path, _experiments = grid

    assert _run(grid, results_path, dry_run=True) == 0
    assert not results_path.exists()
    assert not (tmp_path / "benchmark_stores").exists() or not list((tmp_path / "benchmark_stores").glob("*.json"))


def test_only_selects_one_experiment(
    grid: tuple[Path, Path, Path, Path, list[SweepExperiment]],
) -> None:
    tmp_path, _raw_dir, _golden, results_path, _experiments = grid

    assert _run(grid, results_path, only="a-default-bm25") == 0
    stores_dir = tmp_path / "benchmark_stores"
    assert len(list(stores_dir.glob("*.json"))) == 1  # only the selected cell's store was built

    text = results_path.read_text(encoding="utf-8")
    plan = text.split("— comparison")[0]
    assert "plan    : unit-grid — 1 experiment(s) over 1 store cell(s)" in plan
    rows = [line for line in text.splitlines() if line.startswith("| a-default-bm25 |")]
    assert len(rows) == 1
    assert not any(line.startswith("| b-noheader") for line in text.splitlines() if line.startswith("| b-noheader-bm"))

    with pytest.raises(SweepSpecError, match="no experiment named 'no-such'"):
        _run(grid, results_path, only="no-such")


def test_store_failures_are_recorded_and_the_run_continues(
    tmp_path: Path,
) -> None:
    raw_dir = tmp_path / "raw"
    en = _capture("docen3333", "en", "Night Raid Report", EN_PARAGRAPHS)
    raw_dir.mkdir(parents=True)
    (raw_dir / "docen3333_en.json").write_text(json.dumps(en, ensure_ascii=False), encoding="utf-8")
    golden_path = tmp_path / "golden.jsonl"
    golden_path.write_text(
        json.dumps(
            {
                "id": "q-en",
                "question": EN_PARAGRAPHS[0],
                "origin": "synthetic",
                "query_language": "en",
                "expected": {
                    "instance_key": INSTANCE,
                    "shared_id": "docen3333",
                    "language": "en",
                    "title": "Night Raid Report",
                    "file_id": "f1f1f1docen3333",
                    "paragraph_ids": [0],
                    "text": "irrelevant",
                },
            }
        ),
        encoding="utf-8",
    )
    results_path = tmp_path / "results.md"

    experiments = define_sweep(
        [
            StoreCell(label="good", chunk_method=MergeChunker(), model="hashing"),
            StoreCell(label="bad-model", chunk_method=MergeChunker(), model="not-the-embedder"),
        ],
        [EmbeddingRetrieval()],
    )
    code = run_sweep(
        name="unit-fail",
        experiments=experiments,
        embedder_factory=_factory,
        source=raw_dir,
        stores_dir=tmp_path / "benchmark_stores",
        results_path=results_path,
        golden_path=golden_path,
    )

    assert code == 1  # one of two experiments failed
    text = results_path.read_text(encoding="utf-8")
    assert "FAILED: " in text
    assert "must be the embedder's own" in text
    assert "> failed: bad-model-embedding" in text
    assert "| good-embedding | hashing | 1800/0.15/on | embedding | " in text
    assert "| bad-model-embedding | — | — | — | — |" in text  # the failed row's metric cells are dashes
    assert sorted(
        NaiveVectorStore.load(path).chunk_config is not None for path in (tmp_path / "benchmark_stores").glob("*.json")
    ) == [True]


def test_stale_and_corrupt_stores_are_rebuilt(
    grid: tuple[Path, Path, Path, Path, list[SweepExperiment]],
) -> None:
    tmp_path, raw_dir, _golden, results_path, experiments = grid
    stores_dir = tmp_path / "benchmark_stores"
    digest = corpus_digest(raw_dir)
    cell_a = experiments[0].cell
    a_path = stores_dir / store_file_name(cell_a, digest)

    # a corrupt file at the slug-named path (a torn write): rebuilt, not fatal
    stores_dir.mkdir(parents=True, exist_ok=True)
    a_path.write_text('{"schema": "nope"}', encoding="utf-8")
    assert _run(grid, results_path) == 0
    assert NaiveVectorStore.load(a_path).chunk_config == MergeChunker().chunk_config()

    # a stale file that claims a different geometry: rebuilt to the plan's config
    stale = NaiveVectorStore(
        dimensions=DIMENSIONS,
        embedding_model="hashing",
        chunk_config={"target_max_chars": 600, "overlap_ratio": 0.1, "prepend_header": True},
    )
    stale.save(a_path)
    stale_results = tmp_path / "results-stale.md"
    assert _run(grid, stale_results) == 0
    rebuilt = NaiveVectorStore.load(a_path)
    assert rebuilt.chunk_config == MergeChunker().chunk_config()

    text = stale_results.read_text(encoding="utf-8")
    a_rows = [line for line in text.splitlines() if line.startswith("| a-default-embedding |")]
    assert a_rows and not a_rows[0].split(" | ")[-1].startswith("reuse /")


def test_store_names_carry_method_model_and_corpus(
    grid: tuple[Path, Path, Path, Path, list[SweepExperiment]],
) -> None:
    """The readable scheme: ``<method-slug(params)>__<model-slug>-<corpus-digest8>.json`` — settled Step 3.6."""
    tmp_path, raw_dir, _golden, _results, experiments = grid
    digest = corpus_digest(raw_dir)
    cell = experiments[0].cell

    name = store_file_name(cell, digest)
    assert name == f"merge-1800-0.15-on__hashing-{digest[:8]}.json"  # method settings + model + corpus digest8
    # deterministic — and label-free: two cells with the same (method, model) share one file
    assert store_file_name(cell, digest) == name
    assert store_file_name(StoreCell(label="x", chunk_method=cell.chunk_method, model=cell.model), digest) == name
    # model, settings and corpus each move the name
    assert store_file_name(StoreCell(label="x", chunk_method=cell.chunk_method, model="other"), digest) != name
    other = store_file_name(StoreCell(label="x", chunk_method=MergeChunker(max_chars=600), model="hashing"), digest)
    assert other.startswith("merge-600-0.15-on__hashing-") and other != name
    assert store_file_name(cell, "0" * 64).endswith("__hashing-00000000.json")  # corpus side

    # and the sweep's store file lands exactly at the slug-derived path
    results_path = tmp_path / "results-fp.md"
    assert _run(grid, results_path, only=experiments[0].name) == 0
    assert (tmp_path / "benchmark_stores" / name).exists()

    # corpus digest is sensitive to content, not just names
    (raw_dir / "extra_en.json").write_text(
        json.dumps(_capture("extraen1", "en", "Extra", ["extra text"]), ensure_ascii=False), encoding="utf-8"
    )
    assert corpus_digest(raw_dir) != digest
    (raw_dir / "extra_en.json").write_text(
        json.dumps(_capture("extraen1", "en", "Extra", ["other extra text"]), ensure_ascii=False), encoding="utf-8"
    )
    assert corpus_digest(raw_dir) != digest


def test_define_sweep_guardrails_and_product_order(
    grid: tuple[Path, Path, Path, Path, list[SweepExperiment]],
) -> None:
    _tmp, _raw, _golden, _results, experiments = grid

    assert [experiment.name for experiment in experiments] == [
        "a-default-embedding",
        "a-default-bm25",
        "b-noheader-embedding",
        "b-noheader-bm25",
    ]  # row-major: cells outer, retrievals inner
    assert select_sweep_experiments(experiments, only=None) == experiments

    three = define_sweep(
        [StoreCell(label="one", chunk_method=MergeChunker(), model="m")],
        [EmbeddingRetrieval(), Bm25Retrieval(), RrfRetrieval()],
    )
    assert [experiment.name for experiment in three] == ["one-embedding", "one-bm25", "one-rrf"]

    with pytest.raises(SweepSpecError, match="duplicated"):
        define_sweep(
            [
                StoreCell(label="one", chunk_method=MergeChunker(), model="m"),
                StoreCell(label="one", chunk_method=MergeChunker(), model="m"),
            ],
            [EmbeddingRetrieval()],
        )
    with pytest.raises(SweepSpecError, match="at least one store cell"):
        define_sweep([], [EmbeddingRetrieval()])
    with pytest.raises(SweepSpecError, match="at least one retrieval method"):
        define_sweep([StoreCell(label="one", chunk_method=MergeChunker(), model="m")], [])
    with pytest.raises(SweepSpecError, match="non-empty label"):
        define_sweep([StoreCell(label=" ", chunk_method=MergeChunker(), model="m")], [EmbeddingRetrieval()])


SCRIPT_IMPORTS = """
from uwazi_rag.use_cases.chunking_methods import MergeChunker
from uwazi_rag.use_cases.retrieval_methods import EmbeddingRetrieval
from uwazi_rag.use_cases.run_sweep import StoreCell, define_sweep

experiments = define_sweep(
    [StoreCell(label="a", chunk_method=MergeChunker(), model="hashing")],
    [EmbeddingRetrieval()],
)
"""


def test_load_sweep_spec_loads_scripts_and_names_failures(tmp_path: Path) -> None:
    script = tmp_path / "unit_script.py"
    script.write_text(SCRIPT_IMPORTS, encoding="utf-8")
    stem, experiments = load_sweep_spec(script)

    assert stem == "unit_script"
    assert [experiment.name for experiment in experiments] == ["a-embedding"]

    bare = tmp_path / "bare.py"
    bare.write_text("from uwazi_rag.use_cases.chunking_methods import MergeChunker\n", encoding="utf-8")
    with pytest.raises(SweepSpecError, match="experiments"):
        load_sweep_spec(bare)

    broken = tmp_path / "broken.py"
    broken.write_text("this is not python(", encoding="utf-8")
    with pytest.raises(SweepSpecError, match="failed to run"):
        load_sweep_spec(broken)

    with pytest.raises(SweepSpecError, match="no sweep script"):
        load_sweep_spec(tmp_path / "missing.py")


def test_sweep_experiment_numbers_equal_the_shared_grading_path(
    grid: tuple[Path, Path, Path, Path, list[SweepExperiment]],
) -> None:
    """The acceptance criterion, offline: sweep numbers == eval-path numbers."""
    tmp_path, raw_dir, golden_path, results_path, experiments = grid
    assert _run(grid, results_path, only="a-default-embedding") == 0

    store_name = store_file_name(
        next(experiment.cell for experiment in experiments if experiment.cell.label == "a-default"),
        corpus_digest(raw_dir),
    )
    prepared = prepare_run(
        store_path=tmp_path / "benchmark_stores" / store_name,
        raw_dir=raw_dir,
        golden_path=golden_path,
    )
    embedder = HashingEmbedding(dimensions=DIMENSIONS)
    hits = rank_rows(prepared, retrieval="embedding", embedder=embedder)
    char_lengths = {chunk.chunk_id: len(chunk.text) for chunk in prepared.store.chunks()}
    card = score_rows(
        prepared.graded,
        hits,
        false_retrieval_threshold=configuration.FALSE_RETRIEVAL_THRESHOLD,
        chunk_char_lengths=char_lengths,
    )
    scope_all = card.scopes[0]

    text = results_path.read_text(encoding="utf-8")
    row = next(line for line in text.splitlines() if line.startswith("| a-default-embedding |"))
    cells = [cell.strip() for cell in row.strip("|").split("|")]
    expected = [
        "a-default-embedding",
        prepared.store.embedding_model,
        f"{prepared.config.target_max_chars}/{prepared.config.overlap_ratio:g}/"
        f"{'on' if prepared.config.prepend_header else 'off'}",
        "embedding",
        str(card.answerable_rows),
    ]
    expected += [f"{100 * scope_all.chunk.recall[k]:.1f}%" for k in (1, 5, 10)]
    expected += [f"{scope_all.chunk.mrr:.3f}"]
    expected += [f"{100 * scope_all.doc.recall[k]:.1f}%" for k in (1, 5, 10)]
    expected += [f"{scope_all.doc.mrr:.3f}"]
    assert cells[: len(expected)] == expected
    # the Step 3.6 lens columns sit between doc MRR and false-retr: cov@k, cov@3000, P@k, RP
    expected_lens = [f"{100 * scope_all.paragraph.coverage[k]:.1f}%" for k in (1, 5, 10)]
    budget = scope_all.paragraph.budget_coverage
    assert budget is not None  # char lengths were passed, so the budget lens was measured
    expected_lens.append(f"{100 * budget:.1f}%")
    expected_lens += [f"{100 * scope_all.chunk.precision[k]:.1f}%" for k in (1, 5, 10)]
    expected_lens.append(f"{100 * scope_all.chunk.r_precision:.1f}%")
    assert cells[len(expected) : len(expected) + len(expected_lens)] == expected_lens
    # the unanswerable row was measured on the same cosine scale the sweep used
    recorded_false = cells[len(expected) + len(expected_lens)]
    assert re.fullmatch(r"\d+/\d+", recorded_false)
    assert recorded_false == f"{len(card.unanswerable.false_retrievals)}/{card.unanswerable.rows}"
