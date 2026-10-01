"""Step 3.5 benchmark driver support: TOML sweep specs, plan, comparison tables.

A benchmark TOML separates building from measuring: each ``[stores.<slug>]``
block is one index build spec (chunker strategy + geometry + embedding
model), each ``[[experiments]]`` one graded run of the golden set against a
store with one ranking method. Parsing is deterministic and loud — unknown
keys, unimplemented strategies and dangling references fail before anything
is built or embedded; the impure orchestration lives in the CLI
(:mod:`uwazi_rag.drivers.cli`), which reuses the shared grading path.

Strategies are module-level tuples so unimplemented options fail loudly:
``CHUNKER_STRATEGIES`` grows when the chunker grows (e.g. drop-footnotes or
section chunking, if approved); ``RETRIEVAL_METHODS`` is imported from the
shared grading path so the spec can never accept a method the runner lacks.
"""

from __future__ import annotations

import math
import tomllib
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

from uwazi_rag.configuration import ROOT_PATH
from uwazi_rag.use_cases.chunking import OVERLAP_RATIO, TARGET_MAX_CHARS
from uwazi_rag.use_cases.eval_retrieval import RECALL_KS, ChunkConfig, _percent
from uwazi_rag.use_cases.eval_run import RETRIEVAL_METHODS

STORE_KEYS = ("chunker", "max_chars", "overlap", "header", "model", "source")
EXPERIMENT_KEYS = ("name", "store", "retrieval")
CHUNKER_STRATEGIES: tuple[str, ...] = ("merge",)


class BenchmarkSpecError(ValueError):
    """A benchmark TOML (or a --only selection) names something unusable — message is stderr-ready."""


@dataclass(frozen=True)
class StoreSpec:
    """One ``[stores.<slug>]`` build spec; ``source`` turns it into read-only reuse."""

    slug: str
    chunker: str = "merge"
    max_chars: int = TARGET_MAX_CHARS
    overlap: float = OVERLAP_RATIO
    header: bool = True
    model: str = ""
    source: str | None = None

    @property
    def chunk_config(self) -> dict[str, Any]:
        """The build-style ``chunk_config`` this spec maps to (recorded on stores)."""
        return {"target_max_chars": self.max_chars, "overlap_ratio": self.overlap, "prepend_header": self.header}

    @property
    def is_source(self) -> bool:
        """``True`` when the spec points at a pre-existing store (never written)."""
        return self.source is not None

    def source_path(self) -> Path:
        """The resolved source path: absolute as-is, else repo-root relative."""
        if self.source is None:
            raise BenchmarkSpecError(f"[stores.{self.slug}] has no source — it is a build spec, not a reuse spec")
        candidate = Path(self.source)
        return candidate if candidate.is_absolute() else ROOT_PATH / candidate

    def describe(self) -> str:
        """``1200/0.15/on`` — the geometry shorthand the comparison table reuses."""
        return format_chunk_cfg(max_chars=self.max_chars, overlap=self.overlap, header=self.header)


@dataclass(frozen=True)
class ExperimentSpec:
    """One ``[[experiments]]`` row: a store, one ranking method, a stable name."""

    name: str
    store: str
    retrieval: str = "embedding"


@dataclass(frozen=True)
class BenchmarkSpec:
    """A parsed benchmark TOML — validation complete, nothing built yet."""

    path: Path
    stores: dict[str, StoreSpec]
    experiments: list[ExperimentSpec]

    @property
    def name(self) -> str:
        """The run's short name (the TOML's file stem, e.g. ``sweep1-chunking``)."""
        return self.path.stem


def parse_benchmark_toml(path: Path) -> BenchmarkSpec:
    """Parse + validate a benchmark TOML; every mistake names its file and section."""
    try:
        raw = tomllib.loads(path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as error:
        raise BenchmarkSpecError(f"{path}: not valid TOML — {error}") from error
    except OSError as error:
        raise BenchmarkSpecError(f"{path}: could not be read — {error}") from error
    stores = _parse_stores(raw.get("stores"), path)
    experiments = _parse_experiments(raw.get("experiments"), stores, path)
    return BenchmarkSpec(path=path, stores=stores, experiments=experiments)


def _parse_stores(raw: Any, path: Path) -> dict[str, StoreSpec]:
    if not isinstance(raw, dict) or not raw:
        raise BenchmarkSpecError(f"{path}: no [stores.<slug>] blocks — a benchmark builds or reuses at least one store")
    stores: dict[str, StoreSpec] = {}
    for slug, body in raw.items():
        context = f"{path}: [stores.{slug}]"
        if not isinstance(body, dict):
            raise BenchmarkSpecError(f"{context} must be a table")
        unknown = sorted(key for key in body if key not in STORE_KEYS)
        if unknown:
            raise BenchmarkSpecError(
                f"{context} unknown key(s) {', '.join(map(str, unknown))} — allowed: {', '.join(STORE_KEYS)}"
            )
        chunker = body.get("chunker", "merge")
        if not isinstance(chunker, str) or chunker not in CHUNKER_STRATEGIES:
            raise BenchmarkSpecError(
                f"{context} chunker {chunker!r} is not implemented (available: {', '.join(CHUNKER_STRATEGIES)})"
            )
        model = body.get("model")
        if not isinstance(model, str) or not model.strip():
            raise BenchmarkSpecError(f'{context} needs a model (e.g. model = "bge-m3")')
        max_chars = _typed(context, "max_chars", body.get("max_chars", TARGET_MAX_CHARS), int, "whole number")
        if max_chars < 1:
            raise BenchmarkSpecError(f"{context} max_chars must be >= 1, got {max_chars}")
        overlap = _typed(context, "overlap", body.get("overlap", OVERLAP_RATIO), (int, float), "number")
        if not 0.0 <= float(overlap) < 0.5:
            raise BenchmarkSpecError(f"{context} overlap must be in [0, 0.5), got {overlap}")
        header = _typed(context, "header", body.get("header", True), bool, "true/false")
        source = body.get("source")
        if source is not None and (not isinstance(source, str) or not source.strip()):
            raise BenchmarkSpecError(f"{context} source must be a path (repo-root relative or absolute)")
        stores[str(slug)] = StoreSpec(
            slug=str(slug),
            chunker=chunker,
            max_chars=max_chars,
            overlap=float(overlap),
            header=header,
            model=model,
            source=source,
        )
    return stores


def _parse_experiments(raw: Any, stores: Mapping[str, StoreSpec], path: Path) -> list[ExperimentSpec]:
    if not isinstance(raw, list) or not raw:
        raise BenchmarkSpecError(f"{path}: no [[experiments]] — a benchmark measures at least one experiment")
    experiments: list[ExperimentSpec] = []
    seen: set[str] = set()
    for position, item in enumerate(raw, start=1):
        context = f"{path}: [[experiments]] #{position}"
        if not isinstance(item, dict):
            raise BenchmarkSpecError(f"{context} must be a table")
        unknown = sorted(key for key in item if key not in EXPERIMENT_KEYS)
        if unknown:
            raise BenchmarkSpecError(
                f"{context} unknown key(s) {', '.join(map(str, unknown))} — allowed: {', '.join(EXPERIMENT_KEYS)}"
            )
        name = item.get("name")
        if not isinstance(name, str) or not name.strip():
            raise BenchmarkSpecError(f'{context} needs a name (e.g. name = "merge-1200")')
        if name in seen:
            raise BenchmarkSpecError(f"{context} experiment name {name!r} is duplicated")
        seen.add(name)
        store_slug = item.get("store")
        if not isinstance(store_slug, str) or store_slug not in stores:
            raise BenchmarkSpecError(f"{context} references store {store_slug!r} — defined: {', '.join(stores)}")
        retrieval = item.get("retrieval", "embedding")
        if not isinstance(retrieval, str) or retrieval not in RETRIEVAL_METHODS:
            raise BenchmarkSpecError(
                f"{context} retrieval {retrieval!r} is not implemented (available: {', '.join(RETRIEVAL_METHODS)})"
            )
        experiments.append(ExperimentSpec(name=name, store=store_slug, retrieval=retrieval))
    return experiments


def _typed(context: str, key: str, value: Any, expected: type | tuple[type, ...], what: str) -> Any:
    """TOML value type-guard with the file/section in the error (bools never pass as ints)."""
    allowed = (expected,) if isinstance(expected, type) else expected
    if isinstance(value, bool) and bool not in allowed:
        raise BenchmarkSpecError(f"{context} {key} must be a {what} — got {value!r}")
    if not isinstance(value, allowed):
        raise BenchmarkSpecError(f"{context} {key} must be a {what} — got {value!r}")
    return value


def select_experiments(experiments: Sequence[ExperimentSpec], *, only: str | None) -> list[ExperimentSpec]:
    """The spec order's selected experiments; ``only`` names exactly one of them."""
    if only is None:
        return list(experiments)
    matches = [experiment for experiment in experiments if experiment.name == only]
    if not matches:
        names = ", ".join(experiment.name for experiment in experiments)
        raise BenchmarkSpecError(f"no experiment named {only!r} — defined: {names}")
    return matches


class _StoreFingerprint(Protocol):
    """The read-only surface benchmark needs from a loaded store (naive store today)."""

    embedding_model: str
    chunk_config: dict[str, Any] | None


def store_matches_spec(store: _StoreFingerprint, spec: StoreSpec) -> bool:
    """True when a loaded store was built exactly as the spec says.

    Legacy stores (no recorded ``chunk_config``) match when the spec is the
    Step 2 defaults — that is precisely the committed baseline's case; the
    deeper byte-level proof happens later in :func:`prepare_run`'s
    re-chunking verification.
    """
    try:
        recorded = ChunkConfig.from_store(store.chunk_config)
    except ValueError:
        return False
    return (
        recorded.target_max_chars == spec.max_chars
        and math.isclose(recorded.overlap_ratio, spec.overlap, rel_tol=0.0, abs_tol=1e-12)
        and recorded.prepend_header == spec.header
        and store.embedding_model == spec.model
    )


def format_chunk_cfg(*, max_chars: int, overlap: float, header: bool) -> str:
    """``1200/0.15/on`` — geometry shorthand shared by plan + comparison output."""
    return f"{max_chars}/{overlap:g}/{'on' if header else 'off'}"


def describe_plan(
    spec: BenchmarkSpec,
    experiments: Sequence[ExperimentSpec],
    store_paths: Mapping[str, str],
) -> list[str]:
    """The ``--dry-run`` grid: what would be built or reused, what would be graded."""
    slugs = list(dict.fromkeys(experiment.store for experiment in experiments))
    lines = [
        f"plan    : {spec.path} — {len(experiments)} experiment(s) over {len(slugs)} store(s)",
        "stores  :",
    ]
    for slug in slugs:
        store = spec.stores[slug]
        kind = "reuse" if store.is_source else "build-or-skip"
        lines.append(f"  {slug:<22} {kind:<13} {store_paths[slug]}  {store.describe()}  {store.model} ({store.chunker})")
    lines.append("experiments:")
    for position, experiment in enumerate(experiments, start=1):
        lines.append(f"  {position}. {experiment.name:<22} → {experiment.store:<22} retrieval {experiment.retrieval}")
    return lines


@dataclass(frozen=True)
class ExperimentResult:
    """What one experiment produced — numbers when it ran, an error when not."""

    name: str
    ok: bool
    model: str = "—"
    cfg: str = "—"
    n: int = 0
    chunk_recall: Mapping[int, float] | None = None
    chunk_mrr: float = 0.0
    doc_recall: Mapping[int, float] | None = None
    doc_mrr: float = 0.0
    false_retrieval: str = "—"
    build_seconds: float | None = None
    run_seconds: float | None = None
    error: str = ""


def render_comparison(results: Sequence[ExperimentResult]) -> list[str]:
    """The run's comparison table: one row per experiment, shared metric columns."""
    ks = list(RECALL_KS)
    lines = [
        "| experiment | model | chunk cfg | n | "
        + " | ".join(f"chunk R@{k}" for k in ks)
        + " | chunk MRR | "
        + " | ".join(f"doc R@{k}" for k in ks)
        + " | doc MRR | false-retr | build/score time |",
        "|" + "---|" * (6 + 2 * len(ks) + 2),
    ]
    dashes = len(ks) * ["—"] + ["—", *["—"] * len(ks), "—"]
    for result in results:
        if not result.ok:
            lines.append(f"| {result.name} | — | — | — | " + " | ".join(dashes) + " | — | — |")
            lines.append(f"> failed: {result.name} — {result.error}" if result.error else f"> failed: {result.name}")
            continue
        time_cell = (
            (f"{result.build_seconds:.0f}s" if result.build_seconds is not None else "reuse")
            + " / "
            + (f"{result.run_seconds:.1f}s" if result.run_seconds is not None else "—")
        )
        false_cell = result.false_retrieval if result.false_retrieval else "—"
        chunk_cells = [_percent(result.chunk_recall[k]) if result.chunk_recall else "—" for k in ks]
        doc_cells = [_percent(result.doc_recall[k]) if result.doc_recall else "—" for k in ks]
        lines.append(
            f"| {result.name} | {result.model} | {result.cfg} | {result.n} | "
            + " | ".join(chunk_cells)
            + f" | {result.chunk_mrr:.3f} | "
            + " | ".join(doc_cells)
            + f" | {result.doc_mrr:.3f} | {false_cell} | {time_cell} |"
        )
    return lines
