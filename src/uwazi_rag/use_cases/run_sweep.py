"""Step 3.5 sweeps: method instances in, recorded benchmark out.

The ONLY orchestration helper a sweep needs. Sweep scripts (``benchmarks/*.py``,
data-as-code) declare plain Python lists — store cells (a chunk method instance
+ an embedding model, labeled) cross-producted with retrieval method instances —
and this helper does everything else:

- store caching, invisible: a store's file is named by a human-readable,
  content-derived slug — ``<method-slug(params)>__<model-slug>-<corpus-digest8>.json``
  (e.g. ``merge-1800-0.15-on__bge-m3-0ac7665e.json``) under ``data/benchmark_stores/``;
  a valid existing store is skipped, stale/missing ones are rebuilt. Pre-existing
  stores (the committed ``data/naive_store.json``) can never be addressed by a
  slug, so they are always read-only.
- results.md appends: resolved-plan lines at run start (every setting visible),
  one labeled block per experiment (facts from the graded objects), and a
  comparison table per run whose cells carry the settings
  (``merge 1200/0.15/on``, ``rrf k=60 w=1.0/1.0``).
- failure semantics: a failed experiment is recorded and the run continues;
  the sweep exits nonzero when anything failed.

Grading itself is NOT here: every experiment goes through the shared path in
:mod:`uwazi_rag.use_cases.eval_run` (prepare_run byte-verifies the store
against a re-chunk of the captures; score_rows grades) — an ``eval`` run and a
sweep experiment over the same store are the same computation by construction.
Impure but offline-deterministic; unit tests drive it on tmp dirs with the
tests' deterministic embedder — never Ollama, never inside pytest a real sweep.
"""

from __future__ import annotations

import hashlib
import importlib.util
import re
import sys
import time
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from uwazi_rag import configuration
from uwazi_rag.adapters.naive_vector_store import NaiveVectorStore
from uwazi_rag.configuration import ROOT_PATH
from uwazi_rag.ports.embedding_port import EmbeddingPort
from uwazi_rag.use_cases.build_golden import GOLDEN_FILE, read_jsonl
from uwazi_rag.use_cases.chunking_methods import ChunkMethod
from uwazi_rag.use_cases.eval_retrieval import COVERAGE_CHAR_BUDGET, RECALL_KS, RESULTS_FILE, _percent, render, score_rows
from uwazi_rag.use_cases.eval_run import append_results, build_run_facts, prepare_run
from uwazi_rag.use_cases.index_captures import index_captures
from uwazi_rag.use_cases.retrieval_methods import RetrievalMethod

# One throwaway embed per store build: its vector length is the store's dimensions.
STORE_BUILD_PROBE = "uwazi-rag benchmark store build probe"


class SweepSpecError(ValueError):
    """A sweep script (or --only) names something unusable — message is stderr-ready."""


@dataclass(frozen=True)
class StoreCell:
    """One build target: a chunk method instance + an embedding model, with a label.

    The label exists for readable experiment names/plan lines; the store itself
    is addressed by fingerprint only — two cells with the same (method, model)
    share one store file, whatever their labels.
    """

    label: str
    chunk_method: ChunkMethod
    model: str


@dataclass(frozen=True)
class SweepExperiment:
    """One graded run of the golden set: one store cell, one retrieval method instance."""

    name: str
    cell: StoreCell
    retrieval: RetrievalMethod


def define_sweep(cells: Sequence[StoreCell], retrievals: Sequence[RetrievalMethod]) -> list[SweepExperiment]:
    """The cross product cells × retrievals — no hand-expanded experiment rows.

    Experiment names are ``f"{cell.label}-{retrieval.name}"`` (stable, greppable
    in results.md); labels must be unique. Row-major order: cells outer,
    retrievals inner — deterministic, so recorded tables keep their shape.
    """
    if not cells:
        raise SweepSpecError("a sweep needs at least one store cell")
    if not retrievals:
        raise SweepSpecError("a sweep needs at least one retrieval method")
    labels = [cell.label for cell in cells]
    if any(not label.strip() for label in labels):
        raise SweepSpecError("every store cell needs a non-empty label")
    duplicated = sorted({label for label in labels if labels.count(label) > 1})
    if duplicated:
        raise SweepSpecError(f"duplicated store cell label(s) {', '.join(map(repr, duplicated))} — labels name experiments")
    return [
        SweepExperiment(name=f"{cell.label}-{retrieval.name}", cell=cell, retrieval=retrieval)
        for cell in cells
        for retrieval in retrievals
    ]


def select_sweep_experiments(experiments: Sequence[SweepExperiment], *, only: str | None) -> list[SweepExperiment]:
    """The declared order's selected experiments; ``only`` names exactly one of them."""
    if only is None:
        return list(experiments)
    matches = [experiment for experiment in experiments if experiment.name == only]
    if not matches:
        names = ", ".join(experiment.name for experiment in experiments)
        raise SweepSpecError(f"no experiment named {only!r} — defined: {names}")
    return matches


def corpus_digest(raw_dir: Path) -> str:
    """sha256 over the captures' names + contents (sorted) — the corpus side of store file names."""
    files = sorted(raw_dir.glob("*.json"))
    if not files:
        raise FileNotFoundError(f"no captures under {raw_dir} — run `uwazi-rag fetch` (or the seed script) first")
    digest = hashlib.sha256()
    for path in files:
        digest.update(path.name.encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
    return digest.hexdigest()


def store_file_name(cell: StoreCell, corpus: str) -> str:
    """The readable store filename: ``<method-slug(params)>__<model-slug>-<corpus-digest8>.json``.

    Slugs are deterministic labels, not identities — the same inputs always
    render the same file (two sweeps configuring the same cell share one store,
    whatever their labels), and the corpus digest's first 8 hex chars are the
    one content input a slug cannot say in words. Validity stays content-based:
    ``_ensure_store`` checks the store's recorded model + chunk_config and the
    grading path byte-verifies the texts, so a stale or lying file is never
    trusted no matter what it is called.
    """
    return f"{method_slug(cell.chunk_method)}__{_slug_text(cell.model)}-{corpus[:8]}.json"


def _slug_text(value: str) -> str:
    """Filesystem-safe slug text: one dash per run of anything outside letters/digits/._-."""
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip("-")
    return cleaned or "x"


def _slug_setting(value: Any) -> str:
    """One ``params()`` value as slug text: bool → on/off, floats compact, strings sanitized."""
    if isinstance(value, bool):
        return "on" if value else "off"
    if isinstance(value, float):
        return f"{value:g}"
    if isinstance(value, int):
        return str(value)
    return _slug_text(str(value))


def method_slug(method: ChunkMethod) -> str:
    """``<name>-<setting>-<setting>-…`` from ``params()`` insertion order (e.g. ``merge-1800-0.15-on``).

    Deterministic across processes and sweeps: same instance, same slug, so the
    store cache is shared, not duplicated. Slugs are labels — two different
    cells that colliding slugs would name identically are still kept honest by
    the content-based validity checks (never by the name).
    """
    settings = "-".join(_slug_setting(value) for value in method.params().values())
    return _slug_text(f"{method.name}-{settings}") if settings else _slug_text(method.name)


@dataclass(frozen=True)
class ExperimentResult:
    """What one experiment produced — numbers when it ran, an error when not."""

    name: str
    ok: bool
    retrieval: str = "—"
    model: str = "—"
    cfg: str = "—"
    n: int = 0
    chunk_recall: Mapping[int, float] | None = None
    chunk_mrr: float = 0.0
    doc_recall: Mapping[int, float] | None = None
    doc_mrr: float = 0.0
    coverage: Mapping[int, float] | None = None
    budget_coverage: float | None = None
    chunk_precision: Mapping[int, float] | None = None
    r_precision: float = 0.0
    false_retrieval: str = "—"
    build_seconds: float | None = None
    run_seconds: float | None = None
    error: str = ""


def format_chunk_cfg(*, max_chars: int, overlap: float, header: bool) -> str:
    """``1800/0.15/on`` — geometry shorthand shared by comparison output."""
    return f"{max_chars}/{overlap:g}/{'on' if header else 'off'}"


def render_comparison(results: Sequence[ExperimentResult]) -> list[str]:
    """The run's comparison table: one row per experiment, shared metric columns.

    Columns follow the currency ladder: chunk level (granule lens: R@k, MRR,
    P@k, RP), document level (the granularity-neutral decider: R@k, MRR), then
    the paragraph lens (cov@k, cov@budget — packaging-immune, never the
    cross-chunker decider). Cells carry the settings: ``model``/``chunk cfg``
    come from the graded objects (the store was verified, so these are facts),
    ``retrieval`` from the method instance's own ``describe()``. The caveat
    lines under the table carry the self-anchored-gold honesty note.
    """
    ks = list(RECALL_KS)
    lens_columns = 2 * (len(ks) + 1)  # cov@k + cov@budget + P@k + RP
    lines = [
        "| experiment | model | chunk cfg | retrieval | n | "
        + " | ".join(f"chunk R@{k}" for k in ks)
        + " | chunk MRR | "
        + " | ".join(f"doc R@{k}" for k in ks)
        + " | doc MRR | "
        + " | ".join(f"cov@{k}" for k in ks)
        + f" | cov@{COVERAGE_CHAR_BUDGET} | "
        + " | ".join(f"P@{k}" for k in ks)
        + " | RP | false-retr | build/score time |",
        "|" + "---|" * (7 + 2 * len(ks) + 2 + lens_columns),
    ]
    for result in results:
        if not result.ok:
            dashes = ["—"] * (2 * len(ks) + 2 + lens_columns)
            lines.append(f"| {result.name} | — | — | — | — | " + " | ".join(dashes) + " | — | — |")
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
        cov_cells = [_percent(result.coverage[k]) if result.coverage else "—" for k in ks]
        budget_cell = _percent(result.budget_coverage) if result.budget_coverage is not None else "—"
        precision_cells = [_percent(result.chunk_precision[k]) if result.chunk_precision else "—" for k in ks]
        lines.append(
            f"| {result.name} | {result.model} | {result.cfg} | {result.retrieval} | {result.n} | "
            + " | ".join(chunk_cells)
            + f" | {result.chunk_mrr:.3f} | "
            + " | ".join(doc_cells)
            + f" | {result.doc_mrr:.3f} | "
            + " | ".join(cov_cells)
            + f" | {budget_cell} | "
            + " | ".join(precision_cells)
            + f" | {_percent(result.r_precision)} | {false_cell} | {time_cell} |"
        )
    lines.append("")
    lines.append(
        f"cov@k = anchor paragraphs covered in top-k (any chunk holding the paragraph counts); "
        f"cov@{COVERAGE_CHAR_BUDGET} = same within the first {COVERAGE_CHAR_BUDGET:,} retrieved chars (whole packed chunks)"
    )
    lines.append(
        "P@k / RP are systematically pessimistic — gold is self-anchored (questions were drafted from the passage "
        "they quote); compare configs, never absolutes"
    )
    return lines


def _display_path(path: Path) -> str:
    """Repo-relative when the path lives inside the repo (results.md stays portable)."""
    try:
        return str(path.relative_to(ROOT_PATH))
    except ValueError:
        return str(path)


def render_resolved_plan(
    *,
    name: str,
    raw_dir: Path,
    golden_path: Path,
    experiments: Sequence[SweepExperiment],
    store_paths: Mapping[str, Path],
    capture_count: int,
    golden_rows: int,
) -> list[str]:
    """The resolved plan: settings visible, readable store paths, experiment order."""
    labels = list(dict.fromkeys(experiment.cell.label for experiment in experiments))
    lines = [
        f"plan    : {name} — {len(experiments)} experiment(s) over {len(labels)} store cell(s)",
        f"captures: {_display_path(raw_dir)} — {capture_count} capture(s)",
        f"golden  : {_display_path(golden_path)} — {golden_rows} row(s)",
        "stores  :",
    ]
    for label in labels:
        cell = next(experiment.cell for experiment in experiments if experiment.cell.label == label)
        lines.append(
            f"  {label:<22} {cell.chunk_method.describe():<22} × {cell.model:<28} → {_display_path(store_paths[label])}"
        )
    lines.append("experiments:")
    for position, experiment in enumerate(experiments, start=1):
        lines.append(
            f"  {position}. {experiment.name:<28} → {experiment.cell.label:<22} retrieval {experiment.retrieval.describe()}"
        )
    return lines


def _ensure_store(
    *,
    cell: StoreCell,
    path: Path,
    raw_dir: Path,
    embedder_factory: Callable[[str], EmbeddingPort],
) -> float | None:
    """Make the slug-named store ready; return build seconds (``None`` = up to date).

    Valid store files are skipped; missing, corrupt, or config-stale ones are
    rebuilt in place — the path belongs to the content slug, so a rebuild can
    never touch a pre-existing store (``data/naive_store.json`` et al.).
    Failures raise; the caller records them and the run continues.
    """
    expected_config = cell.chunk_method.chunk_config()
    if path.exists():
        try:
            loaded = NaiveVectorStore.load(path)
            valid = loaded.embedding_model == cell.model and loaded.chunk_config == expected_config
        except (RuntimeError, ValueError, KeyError, TypeError, OSError):
            valid = False
        if valid:
            print(f"store   : {cell.label} — up to date ({_display_path(path)} matches the plan; build skipped)")
            return None

    embedder = embedder_factory(cell.model)
    embedded_model = getattr(embedder, "model", None)
    if embedded_model is not None and embedded_model != cell.model:
        raise ValueError(
            f"the embedder factory produced model {embedded_model!r} for cell model {cell.model!r} — "
            "a store's recorded model must be the embedder's own"
        )
    probe = embedder.embed([STORE_BUILD_PROBE])
    if len(probe) != 1:
        raise RuntimeError(f"the embedder returned {len(probe)} vectors for one probe text")
    dimensions = len(probe[0])
    if dimensions < 1:
        raise ValueError(f"the embedder returned a {dimensions}-dimension vector — check the model")

    store = NaiveVectorStore(dimensions=dimensions, embedding_model=cell.model, chunk_config=expected_config)
    clock = time.monotonic()
    stats = index_captures(
        raw_dir=raw_dir, store=store, embedder=embedder, expected_dimensions=dimensions, **expected_config
    )
    seconds = time.monotonic() - clock
    store.save(path)
    print(f"store   : {cell.label} — built {stats.chunks_indexed:,} chunks in {seconds:.0f}s")
    return seconds


def run_sweep(
    *,
    name: str,
    experiments: Sequence[SweepExperiment],
    embedder_factory: Callable[[str], EmbeddingPort],
    source: Path | None = None,
    only: str | None = None,
    dry_run: bool = False,
    stores_dir: Path | None = None,
    results_path: Path | None = None,
    golden_path: Path | None = None,
) -> int:
    """Run one recorded sweep: build-or-reuse each cell's store, grade, append, return the exit code.

    The CLI is a thin wrapper over this; the seams (``stores_dir``/``results_path``/
    ``golden_path``/``source``/``embedder_factory``) exist so offline unit tests
    can drive the whole thing on real files with the deterministic embedder.
    """
    selected = select_sweep_experiments(experiments, only=only)
    raw_dir = Path(source) if source else configuration.RAW_DIR / configuration.instance_key(configuration.uwazi_url())
    digest = corpus_digest(raw_dir)
    capture_count = len(sorted(raw_dir.glob("*.json")))
    stores_dir = stores_dir if stores_dir is not None else configuration.BENCHMARK_STORES_DIR
    results_path = results_path if results_path is not None else configuration.EVAL_DIR / RESULTS_FILE
    golden_path = golden_path if golden_path is not None else configuration.EVAL_DIR / GOLDEN_FILE
    golden_rows = len(read_jsonl(golden_path))

    store_paths = {
        label: stores_dir / store_file_name(cell, digest)
        for label, cell in ((experiment.cell.label, experiment.cell) for experiment in selected)
    }
    plan_lines = render_resolved_plan(
        name=name,
        raw_dir=raw_dir,
        golden_path=golden_path,
        experiments=selected,
        store_paths=store_paths,
        capture_count=capture_count,
        golden_rows=golden_rows,
    )
    if dry_run:
        for line in plan_lines:
            print(line)
        return 0

    append_results(
        results_path,
        f"## {datetime.now(timezone.utc).isoformat(timespec='seconds')} — benchmark {name} — resolved plan\n\n"
        + "\n".join(plan_lines)
        + "\n",
    )
    for line in plan_lines:
        print(line)

    store_state: dict[str, tuple[float | None, str]] = {}
    results: list[ExperimentResult] = []
    for experiment in selected:
        label = experiment.cell.label
        path = store_paths[label]
        started_at = datetime.now(timezone.utc)
        full_label = f"benchmark {name}: {experiment.name}"

        if label not in store_state:  # store phase: lazy, once per cell
            try:
                store_state[label] = (
                    _ensure_store(cell=experiment.cell, path=path, raw_dir=raw_dir, embedder_factory=embedder_factory),
                    "",
                )
            except (RuntimeError, ValueError, OSError) as error:
                store_state[label] = (None, str(error).replace("\n", " ")[:240])

        build_seconds, store_error = store_state[label]
        if store_error:
            results.append(ExperimentResult(name=experiment.name, ok=False, error=store_error))
            print(f"failure : {experiment.name} — {store_error}", file=sys.stderr)
            append_results(
                results_path, f"## {started_at.isoformat(timespec='seconds')} — {full_label}\n\nFAILED: {store_error}\n"
            )
            continue

        clock = time.monotonic()
        try:
            prepared = prepare_run(store_path=path, raw_dir=raw_dir, golden_path=golden_path)
            for note in prepared.graded.ungradable:
                print(f"warning: {note}", file=sys.stderr)
            if prepared.check.extra_in_store:
                print(
                    f"note: {len(prepared.check.extra_in_store)} store chunks belong to captures outside {raw_dir} "
                    "(indexed earlier from a wider corpus) — they stay in the ranking",
                    file=sys.stderr,
                )
            embedder = embedder_factory(prepared.store.embedding_model)
            hits_by_row = experiment.retrieval.rank(prepared, embedder=embedder)
            # the budget lens reads the store's chunk texts (byte-verified = the graded truth)
            char_lengths = {chunk.chunk_id: len(chunk.text) for chunk in prepared.store.chunks()}
            card = score_rows(
                prepared.graded,
                hits_by_row,
                false_retrieval_threshold=(
                    configuration.FALSE_RETRIEVAL_THRESHOLD if experiment.retrieval.cosine_calibrated else None
                ),
                chunk_char_lengths=char_lengths,
            )
        except (RuntimeError, ValueError, OSError) as error:
            message = str(error).replace("\n", " ")[:240]
            elapsed = time.monotonic() - clock
            results.append(ExperimentResult(name=experiment.name, ok=False, run_seconds=elapsed, error=message))
            print(f"failure : {experiment.name} — {message}", file=sys.stderr)
            append_results(
                results_path,
                f"## {started_at.isoformat(timespec='seconds')} — {full_label}\n\nFAILED after {elapsed:.0f}s: {message}\n",
            )
            continue

        elapsed = time.monotonic() - clock
        run = build_run_facts(
            prepared,
            label=full_label,
            started_at_utc=started_at.isoformat(timespec="seconds"),
            elapsed_seconds=elapsed,
            false_retrieval_threshold=configuration.FALSE_RETRIEVAL_THRESHOLD,
        )
        block = render(run, card, heading=True)
        block += f"retrieval: {experiment.retrieval.describe()}\n"
        if not experiment.retrieval.cosine_calibrated:
            block += (
                "note: false-retrieval is cosine-specific — this method scores on a different scale, "
                "so comparison cells read —\n"
            )
        append_results(results_path, block)
        print(render(run, card, heading=False), end="")
        print(f"retrieval: {experiment.retrieval.describe()}")
        scope_all = card.scopes[0]
        results.append(
            ExperimentResult(
                name=experiment.name,
                ok=True,
                retrieval=experiment.retrieval.describe(),
                model=run.store_model,
                cfg=format_chunk_cfg(
                    max_chars=run.config.target_max_chars,
                    overlap=run.config.overlap_ratio,
                    header=run.config.prepend_header,
                ),
                n=card.answerable_rows,
                chunk_recall=scope_all.chunk.recall,
                chunk_mrr=scope_all.chunk.mrr,
                doc_recall=scope_all.doc.recall,
                doc_mrr=scope_all.doc.mrr,
                coverage=scope_all.paragraph.coverage,
                budget_coverage=scope_all.paragraph.budget_coverage,
                chunk_precision=scope_all.chunk.precision,
                r_precision=scope_all.chunk.r_precision,
                false_retrieval=(
                    f"{len(card.unanswerable.false_retrievals)}/{card.unanswerable.rows}"
                    if experiment.retrieval.cosine_calibrated
                    else "—"
                ),
                build_seconds=build_seconds,
                run_seconds=elapsed,
            )
        )

    heading = (
        f"## {datetime.now(timezone.utc).isoformat(timespec='seconds')} — benchmark {name} — comparison "
        f"({len(results)} experiment{'s' if len(results) != 1 else ''})"
    )
    block = heading + "\n\n" + "\n".join(render_comparison(results)) + "\n"
    append_results(results_path, block)
    for line in block.splitlines():
        print(line)
    graded = sum(1 for result in results if result.ok)
    print(f"done    : {graded}/{len(results)} experiments graded — results appended to {_display_path(results_path)}")
    return 0 if graded == len(results) else 1


def load_sweep_spec(path: Path) -> tuple[str, list[SweepExperiment]]:
    """Load one sweep script; its module-level ``experiments`` list is the run's grid.

    Scripts are data-as-code (one script = one recorded sweep); the run's name
    is the file stem. Failures name the script and are stderr-ready.
    """
    if not path.is_file():
        raise SweepSpecError(f"no sweep script at {path} — the specs live in benchmarks/ as plain Python")
    spec = importlib.util.spec_from_file_location(f"uwazi_rag_sweep_{re.sub(r'\\W', '_', path.stem)}", path)
    if spec is None or spec.loader is None:
        raise SweepSpecError(f"{path}: cannot be loaded as a Python module")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    try:
        spec.loader.exec_module(module)
    except Exception as error:
        raise SweepSpecError(f"{path}: the script failed to run — {type(error).__name__}: {error}") from error
    experiments = getattr(module, "experiments", None)
    if not isinstance(experiments, list) or not experiments:
        raise SweepSpecError(
            f"{path}: must define a non-empty module-level experiments list — call define_sweep(cells, retrievals)"
        )
    if any(not isinstance(experiment, SweepExperiment) for experiment in experiments):
        raise SweepSpecError(f"{path}: experiments entries must come from define_sweep (SweepExperiment objects)")
    return path.stem, experiments
