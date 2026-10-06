"""Step 4a — the dataset build registry.

Maps dataset ids (the golden-dir / instance-key namespace names) to adapters
built through factories, plus each home's re-fetch instructions. The factory
shape lets the offline tests construct adapters over fixture-slice homes; the
build use case resolves through :func:`registry`.
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import NamedTuple

from uwazi_rag.adapters.datasets.base import DatasetAdapter
from uwazi_rag.adapters.datasets.legalbenchrag import LegalBenchRagSource
from uwazi_rag.adapters.datasets.vic_chargebook import VicChargebook


class DatasetSpec(NamedTuple):
    """A registered dataset: its adapter factory + the re-fetch hint for missing upstream."""

    make: Callable[[Path | None], DatasetAdapter]
    re_fetch_hint: str


# MAUD is absent: license-gated (see data/datasets/legalbenchrag/about.md).
# Re-fetch hints quote each home's verified upstream origin + revision pin.
_REGISTRY: dict[str, DatasetSpec] = {
    "legalbenchrag-privacyqa": DatasetSpec(
        make=lambda home: LegalBenchRagSource("legalbenchrag-privacyqa", home_dir=home),
        re_fetch_hint=(
            "hf dataset awinml/legalbench-rag, revision 2b9c248bc8179ef0908fd6ba01d50b156facd48b — "
            "restore data/datasets/legalbenchrag/upstream/ (benchmarks/ + corpus/) and check SHA256SUMS"
        ),
    ),
    "legalbenchrag-contractnli": DatasetSpec(
        make=lambda home: LegalBenchRagSource("legalbenchrag-contractnli", home_dir=home),
        re_fetch_hint=(
            "hf dataset awinml/legalbench-rag, revision 2b9c248bc8179ef0908fd6ba01d50b156facd48b — "
            "restore data/datasets/legalbenchrag/upstream/ (benchmarks/ + corpus/) and check SHA256SUMS"
        ),
    ),
    "legalbenchrag-cuad": DatasetSpec(
        make=lambda home: LegalBenchRagSource("legalbenchrag-cuad", home_dir=home),
        re_fetch_hint=(
            "hf dataset awinml/legalbench-rag, revision 2b9c248bc8179ef0908fd6ba01d50b156facd48b — "
            "restore data/datasets/legalbenchrag/upstream/ (benchmarks/ + corpus/) and check SHA256SUMS"
        ),
    ),
    "vic-chargebook": DatasetSpec(
        make=lambda home: VicChargebook(home_dir=home),
        re_fetch_hint=(
            "hf dataset isaacus/legal-rag-bench, revision db0b31dc6d195ce9916897e1ac5e4e6209736c8a — "
            "restore data/datasets/vic-chargebook/upstream/ (corpus.jsonl + qa.jsonl)"
        ),
    ),
}


def registry() -> dict[str, DatasetSpec]:
    """The dataset-id → spec registry (a copy; callers cannot mutate registration)."""
    return dict(_REGISTRY)


def known_dataset_ids() -> list[str]:
    return sorted(_REGISTRY)


def resolve_dataset(name: str, *, home_dir: Path | None = None) -> tuple[DatasetAdapter, str]:
    """Build the adapter for one dataset id through its factory (home override honored).

    Returns ``(adapter, re_fetch_hint)``; unknown names list the registered ids.
    """
    spec = _REGISTRY.get(name)
    if spec is None:
        known = ", ".join(sorted(_REGISTRY))
        raise ValueError(f"unknown dataset {name!r} — registered datasets: {known}")
    return spec.make(home_dir), spec.re_fetch_hint
