"""Step 4a — the dataset-adapter interface and the build-result types.

One adapter per upstream dataset (PLAN.md Step 4a). An adapter knows how to
verify its upstream checksums and turn that upstream into dataset captures +
golden rows; orchestration (paths, writing, manual merge, summary printing)
lives in :mod:`uwazi_rag.use_cases.build_dataset` so adapters stay thin and
their mapping code stays testable offline.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

from uwazi_rag.adapters.datasets.pins import PinCheck


@dataclass(frozen=True)
class DatasetBuildResult:
    """What one adapter build produced — captures, golden rows, summary facts.

    Every field is derived deterministically from the upstream tree, so two
    builds of the same upstream produce equal results (bit-stability is
    asserted in the adapter tests, then verified again across real builds).
    """

    captures: Mapping[str, dict[str, Any]]  # capture file name → capture dict
    golden_rows: Sequence[dict[str, Any]]  # upstream rows only (manual merges in the use case)
    pin_checks: Sequence[PinCheck]
    checks: int  # the per-dataset acceptance checks verified during build (span self-check or label resolution)
    note: str = ""  # the dataset-specific decision worth recording in the summary

    def summary(self) -> list[str]:
        """Deterministic summary lines for the ``dataset`` command's report."""
        lines = [f"pins    : {', '.join(f'{check.label} ({check.digest[:12]}…)' for check in self.pin_checks)}"]
        lines.append(f"captures: {len(self.captures)}")
        lines.append(f"golden  : {len(self.golden_rows)} upstream row(s); {self.checks} acceptance check(s) passed")
        if self.note:
            lines.append(f"note    : {self.note}")
        return lines


class DatasetAdapter(Protocol):
    """The adapter surface the build use case drives; adapters register in the package ``__init__``."""

    @property
    def dataset_id(self) -> str:
        """The instrument's id (e.g. ``legalbenchrag-cuad``) — its namespace + golden dir."""

    def home_dir(self) -> Path:
        """The dataset's committed home (holds ``about.md`` + ``checksums.txt``)."""

    def upstream_dir(self) -> Path:
        """The (gitignored) upstream tree this adapter consumes when present."""

    def verify(self, upstream_dir: Path) -> list[PinCheck]:
        """Verify the upstream tree against the home's committed pins (raises on drift)."""

    def build(self, upstream_dir: Path) -> DatasetBuildResult:
        """Map the verified upstream into captures + upstream golden rows."""


def capture_file_name(capture: Mapping[str, Any]) -> str:
    """The captures-dir file name for one dataset capture (``load_captures``-compatible)."""
    return f"{capture['shared_id']}_{capture['language']}.json"
