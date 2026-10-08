"""Sweep-runner tests — the dataset wiring (Step 4a), offline end to end.

The dataset instruments run through the UNCHANGED benchmark runner: the spec
names its ``dataset``, the runner repoints captures + golden, and every
results.md block carries the instrument. These tests pin that wiring offline
(tmp captures + the deterministic embedder, per AGENTS.md policy), plus the
namespace derivation the default paths hang off.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from uwazi_rag import configuration
from uwazi_rag.ports.embedding_port import EmbeddingPort
from uwazi_rag.tests.hash_embedding import HashingEmbedding
from uwazi_rag.use_cases.chunking_methods import MergeChunker
from uwazi_rag.use_cases.retrieval_methods import EmbeddingRetrieval
from uwazi_rag.use_cases.run_sweep import StoreCell, SweepSpecError, define_sweep, load_sweep_spec, run_sweep

ROOT = configuration.ROOT_PATH
INSTANCE = "ds0000000000abcd"


def _capture(shared_id: str, title: str, paragraph: str) -> dict[str, Any]:
    return {
        "instance_key": INSTANCE,
        "shared_id": shared_id,
        "language": "en",
        "title": title,
        "template": {"id": "dataset", "name": "unit-dataset"},
        "file": {"id": f"corpus/{shared_id}.txt", "name": f"{shared_id}.txt"},
        "segmentation_status": "ready",
        "fetched_at_utc": None,
        "paragraphs": [{"text": paragraph}],
    }


def _factory(_model: str) -> EmbeddingPort:
    return HashingEmbedding(dimensions=16)


@pytest.fixture()
def instrument(tmp_path: Path) -> tuple[Path, Path, Path, list[Any]]:
    """A tiny two-capture instrument + golden (one unanswerable), ready to sweep."""
    raw_dir = tmp_path / "raw"
    raw_dir.mkdir(parents=True)
    gold_text = "The retention period for chat logs is 24 months."
    decoy_text = "Maritime arbitration clauses govern the shipping dispute."
    for name, capture in (
        ("gold_en.json", _capture("docgold1111", "Privacy Policy", gold_text)),
        ("decoy_en.json", _capture("docdecoy111", "Shipping Contract", decoy_text)),
    ):
        (raw_dir / name).write_text(json.dumps(capture, ensure_ascii=False), encoding="utf-8")

    rows = [
        {
            "id": "docgold1111:q001",
            "question": gold_text,
            "origin": "upstream",
            "query_language": "en",
            "source_group_id": "docgold1111",
            "expected": {
                "instance_key": INSTANCE,
                "shared_id": "docgold1111",
                "title": "Privacy Policy",
                "language": "en",
                "file_id": "corpus/docgold1111.txt",
                "paragraph_ids": [0],
                "text": gold_text,
            },
        },
        {
            "id": "m001",
            "question": "quantum flux monitoring grid",
            "origin": "manual",
            "query_language": "en",
            "source_group_id": None,
            "expected": None,
        },
    ]
    golden_path = tmp_path / "golden.jsonl"
    golden_path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")

    experiments = define_sweep(
        [StoreCell(label="baseline", chunk_method=MergeChunker(), model="hashing")],
        [EmbeddingRetrieval()],
    )
    return tmp_path, raw_dir, golden_path, experiments


def test_run_sweep_dataset_labels_every_appended_block(instrument: tuple[Path, Path, Path, list[Any]]) -> None:
    tmp_path, raw_dir, golden_path, experiments = instrument
    results_path = tmp_path / "results.md"

    exit_code = run_sweep(
        name="unit-dataset-sweep",
        experiments=experiments,
        embedder_factory=_factory,
        source=raw_dir,
        stores_dir=tmp_path / "stores",
        results_path=results_path,
        golden_path=golden_path,
        dataset="legalbenchrag-privacyqa",
    )
    assert exit_code == 0

    text = results_path.read_text(encoding="utf-8")
    assert "dataset : legalbenchrag-privacyqa" in text  # the plan line
    assert "dataset: legalbenchrag-privacyqa" in text  # the per-experiment block line
    assert "— benchmark unit-dataset-sweep — dataset legalbenchrag-privacyqa — comparison (1 experiment)" in text
    # instrument rows: one upstream answerable + one manual unanswerable
    assert "golden  : " in text and " — 2 row(s)" in text


def test_run_sweep_without_dataset_keeps_the_uwazi_defaults(instrument: tuple[Path, Path, Path, list[Any]]) -> None:
    tmp_path, raw_dir, golden_path, experiments = instrument
    results_path = tmp_path / "results.md"

    assert (
        run_sweep(
            name="unit-plain-sweep",
            experiments=experiments,
            embedder_factory=_factory,
            source=raw_dir,
            stores_dir=tmp_path / "stores",
            results_path=results_path,
            golden_path=golden_path,
        )
        == 0
    )
    text = results_path.read_text(encoding="utf-8")
    assert "dataset : " not in text and "\ndataset: " not in text and "— dataset " not in text
    # the Uwazi-golden sweeps never gain an instrument line (a bare 'dataset'
    # word can appear inside tmp paths, but never as a runner block)
    assert "— benchmark unit-plain-sweep — comparison (1 experiment)" in text


def test_dataset_instance_key_pins_the_namespace() -> None:
    """The dataset namespaces, computed the same way the builds print them (stable)."""
    assert configuration.dataset_instance_key("legalbenchrag-privacyqa") == "8a3f38ffd23a75e2"
    assert configuration.dataset_instance_key("legalbenchrag-contractnli") == "d7f14657e7264534"
    assert configuration.dataset_instance_key("legalbenchrag-cuad") == "c88547bc806ea086"
    assert configuration.dataset_instance_key("legalbenchrag-maud") == "4961ebee611362f6"
    assert configuration.dataset_instance_key("vic-chargebook") == "c49c2465f4afa801"


THE_DATASET_SPECS = [
    ("sweep_legalbenchrag_privacyqa.py", "legalbenchrag-privacyqa", 16),
    ("sweep_legalbenchrag_contractnli.py", "legalbenchrag-contractnli", 16),
    ("sweep_legalbenchrag_cuad.py", "legalbenchrag-cuad", 16),
    ("sweep_legalbenchrag_maud.py", "legalbenchrag-maud", 16),
    ("sweep_vic_chargebook.py", "vic-chargebook", 16),
]


@pytest.mark.parametrize(("file_name", "dataset_id", "cell_count"), THE_DATASET_SPECS)
def test_the_committed_dataset_specs_declare_their_instrument(file_name: str, dataset_id: str, cell_count: int) -> None:
    name, experiments, dataset = load_sweep_spec(ROOT / "benchmarks" / file_name)

    assert name == Path(file_name).stem
    assert dataset == dataset_id
    assert len({experiment.cell.label for experiment in experiments}) == cell_count


def test_a_bad_dataset_attribute_is_a_spec_error(tmp_path: Path) -> None:
    script = tmp_path / "bad_instrument.py"
    script.write_text(
        "from uwazi_rag.use_cases.chunking_methods import MergeChunker\n"
        "from uwazi_rag.use_cases.retrieval_methods import EmbeddingRetrieval\n"
        "from uwazi_rag.use_cases.run_sweep import StoreCell, define_sweep\n"
        "dataset = '  '\n"
        "experiments = define_sweep([StoreCell(label='a', chunk_method=MergeChunker(), model='hashing')], [EmbeddingRetrieval()])\n",  # noqa: E501
        encoding="utf-8",
    )
    with pytest.raises(SweepSpecError, match="dataset"):
        load_sweep_spec(script)
