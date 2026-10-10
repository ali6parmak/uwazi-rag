"""Step 4a: build one dataset instrument from its verified upstream.

``uwazi-rag dataset <name>`` — the orchestration half of the dataset
adapters: resolve the adapter, verify the upstream against the home's
committed checksum pins, map the upstream into captures + upstream golden rows,
merge the LLM-drafted unanswerables (the home's ``manual.jsonl``), and write
both artifacts:

- captures (byte-identical on every rebuild — no clock inside) to the dataset's
  own ``data/raw/<instance_key>/``, exactly like an Uwazi capture corpus;
- ``golden.jsonl`` (upstream rows + manual rows merged, deterministic) to
  ``data/eval/datasets/<dataset_id>/``.

Idempotent by construction: same upstream + same manual file → same bytes
(the determinism tests run the whole build twice and compare). Missing
upstream is a self-explaining error quoting the re-fetch hint — the network
path is a real-fetch job for later (PLAN.md), never inside pytest.
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from loguru import logger

from uwazi_rag import configuration
from uwazi_rag.adapters.datasets import resolve_dataset
from uwazi_rag.adapters.datasets.base import DatasetBuildResult
from uwazi_rag.use_cases.build_golden import read_jsonl, write_jsonl

GOLDEN_FILE = "golden.jsonl"
MANUAL_FILE = "manual.jsonl"


@dataclass(frozen=True)
class DatasetBuildStats:
    """What one ``dataset`` build did — the CLI's progress report + the tests' handle."""

    dataset_id: str
    instance_key: str
    raw_dir: str
    golden_path: str
    captures_written: int
    upstream_rows: int
    manual_rows_merged: int


def build_dataset(
    dataset_id: str,
    *,
    home_dir: Path | None = None,
    upstream_dir: Path | None = None,
    raw_dir: Path | None = None,
    golden_dir: Path | None = None,
) -> DatasetBuildStats:
    """Build one dataset end-to-end (verify → map → merge manual → write).

    The ``*_dir`` parameters exist for the offline tests (they run the build
    on fixture slices in tmp dirs); the CLI passes none and gets the real
    house paths. Raises on anything dishonest — drift, missing upstream,
    invalid manual rows, duplicate identities — BEFORE writing anything.
    """
    adapter, re_fetch_hint = resolve_dataset(dataset_id, home_dir=home_dir)
    resolved_upstream = upstream_dir if upstream_dir is not None else adapter.upstream_dir()
    if not resolved_upstream.is_dir():
        raise FileNotFoundError(f"no upstream tree at {resolved_upstream} — restore it first: {re_fetch_hint}")
    resolved_home = adapter.home_dir()
    if not (resolved_home / "checksums.txt").is_file():
        raise FileNotFoundError(
            f"no committed pins at {resolved_home / 'checksums.txt'} — a dataset builds only over pinned upstream"
        )

    result: DatasetBuildResult = adapter.build(resolved_upstream)

    resolved_raw = raw_dir if raw_dir is not None else configuration.RAW_DIR / configuration.dataset_instance_key(dataset_id)
    resolved_golden_dir = golden_dir if golden_dir is not None else configuration.EVAL_DATASETS_DIR / dataset_id

    # Validate the manual rows BEFORE anything is written (abort-before-write holds
    # for every failure class: pins drift, self-check, manual validation).
    upstream_rows = list(result.golden_rows)
    manual_rows = _validated_manual(dataset_id, resolved_golden_dir, upstream_rows)
    merged = _merged_golden(upstream_rows, manual_rows)

    write_captures(result.captures, resolved_raw)
    resolved_golden_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(resolved_golden_dir / GOLDEN_FILE, merged)

    for line in result.summary():
        logger.info(line)
    logger.info(f"manual  : {len(manual_rows)} unanswerable row(s) merged from {MANUAL_FILE}")
    return DatasetBuildStats(
        dataset_id=dataset_id,
        instance_key=configuration.dataset_instance_key(dataset_id),
        raw_dir=str(resolved_raw),
        golden_path=str(resolved_golden_dir / GOLDEN_FILE),
        captures_written=len(result.captures),
        upstream_rows=len(upstream_rows),
        manual_rows_merged=len(manual_rows),
    )


def _validated_manual(dataset_id: str, golden_dir: Path, upstream_rows: list[dict]) -> list[dict]:
    """Read + validate the dataset's LLM-drafted unanswerables (absent file → none)."""
    manual_path = golden_dir / MANUAL_FILE
    if not manual_path.exists():
        return []
    from uwazi_rag.adapters.datasets.core import manual_row_problems

    manual_rows = read_jsonl(manual_path)
    problems = manual_row_problems(manual_rows, golden_rows=upstream_rows)
    if problems:
        raise ValueError(
            f"invalid manual rows for dataset {dataset_id} ({manual_path}) — fixing before anything is written:\n"
            + "\n".join(f"  - {problem}" for problem in problems)
        )
    return [dict(row) for row in manual_rows]


def _merged_golden(upstream_rows: list[dict], manual_rows: list[dict]) -> list[dict]:
    """Upstream rows first, manual rows appended (order fixed → bytes fixed)."""
    return [*upstream_rows, *manual_rows]


def write_captures(captures: Mapping[str, dict[str, Any]], raw_dir: Path) -> list[Path]:
    """Write dataset captures file-name-sorted, byte-stable (no clock fields)."""
    raw_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for name in sorted(captures):
        text = json.dumps(captures[name], ensure_ascii=False, indent=2) + "\n"
        path = raw_dir / name
        path.write_text(text, encoding="utf-8")
        written.append(path)
    return written


__all__ = [
    "GOLDEN_FILE",
    "MANUAL_FILE",
    "DatasetBuildStats",
    "build_dataset",
]
