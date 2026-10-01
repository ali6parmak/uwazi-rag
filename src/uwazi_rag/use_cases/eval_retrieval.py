"""Step 3.5, scorecard half: grade ranked retrieval against the golden anchors.

Golden rows anchor ``paragraph_ids`` (0-based raw-capture positions), so the
dataset survives any chunk configuration. Grading works by *re-chunking* the
captures with the same pure chunker under the chunk config being graded and
reading each chunk's ``paragraph_ids`` provenance — no text matching, no
stored-forever chunk anchors. From ranked chunk ids it computes recall@k and
MRR at **chunk level** (granule precision) and **document level** (the
``(instance_key, shared_id, language)`` capture — keeps chunk-size sweeps
fair, because bigger chunks trivially inflate chunk-level recall).

Everything here is pure and offline-testable: metrics, mapping, scoping,
formatting. The CLI driver (:mod:`uwazi_rag.drivers.cli`) owns the impure
parts — loading captures, embedding questions through the ``EmbeddingPort``,
querying the store — and hands ranked ``Hit`` lists back in.

Metrics conventions:

- answerable rows only (``expected`` present) enter recall/MRR
- recall@k is the mean of per-row partial credit
  ``|gold ∩ ranked[:k]| / |gold|``
- MRR is measured within the ranked list the caller provides (CLI retrieves
  ``RETRIEVAL_DEPTH`` deep; a gold not found anywhere in it scores 0)
- unanswerable rows are excluded from every scope and reported as a
  *false-retrieval rate*: the fraction whose top-1 score reaches
  ``false_retrieval_threshold`` (cosine, config not code)
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any

from uwazi_rag.domain.chunk import Chunk
from uwazi_rag.use_cases.chunking import OVERLAP_RATIO, TARGET_MAX_CHARS
from uwazi_rag.use_cases.index_captures import capture_to_chunks

RECALL_KS = (1, 5, 10)
# MRR needs a real rank even when gold sits deep; the naive cosine scan is
# cheap (one numpy matmul per question over the whole store), so rank deep.
RETRIEVAL_DEPTH = 100
RESULTS_FILE = "results.md"
RESULTS_HEADER = (
    "# Retrieval eval results — `uwazi-rag eval` (Step 3.5)\n\n"
    "Append-only scorecard log: every run appends one dated, labeled block "
    "below. The golden set is the committed `data/eval/golden.jsonl`; scores "
    "are *relative* (config A vs config B, shared self-echo bias), never "
    "absolute (see `data/eval/about.md`).\n"
)

DocKey = tuple[str, str, str]  # (instance_key, shared_id, language)
NO_DOC_KEY: DocKey = ("", "", "")


@dataclass(frozen=True)
class ChunkConfig:
    """The chunk configuration being graded.

    Eval has no chunk flags of its own: the config comes from the store (new
    builds record it) and defaults to the Step 2 constants for legacy stores.
    """

    target_max_chars: int = TARGET_MAX_CHARS
    overlap_ratio: float = OVERLAP_RATIO
    prepend_header: bool = True

    @classmethod
    def from_store(cls, stored: Mapping[str, Any] | None) -> ChunkConfig:
        """Parse a store's recorded ``chunk_config`` (``None`` → Step 2 defaults)."""
        if stored is None:
            return cls()
        try:
            config = cls(
                target_max_chars=int(stored["target_max_chars"]),
                overlap_ratio=float(stored["overlap_ratio"]),
                prepend_header=bool(stored["prepend_header"]),
            )
            config.validate()
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError(f"store chunk_config is invalid ({stored!r}) — rebuild the store with build-index") from error
        return config

    def validate(self) -> None:
        """Reject nonsense configs before any chunking work (mirrors the chunker)."""
        if self.target_max_chars < 1:
            raise ValueError(f"target_max_chars must be >= 1, got {self.target_max_chars}")
        if not 0.0 <= self.overlap_ratio < 0.5:
            raise ValueError(f"overlap_ratio must be in [0, 0.5), got {self.overlap_ratio}")


@dataclass(frozen=True)
class Hit:
    """One ranked retrieval result, normalized out of a store's search shape."""

    chunk_id: str
    doc_key: DocKey
    score: float


def hits_from_store(search_result: Sequence[tuple[Chunk, float]]) -> list[Hit]:
    """Adapt ``store.search`` output ([chunk, score] pairs) into ``Hit``s."""
    return [
        Hit(chunk_id=chunk.chunk_id, doc_key=(chunk.instance_key, chunk.shared_id, chunk.language), score=score)
        for chunk, score in search_result
    ]


@dataclass(frozen=True)
class ConfigCheck:
    """Result of checking a store against the chunk config being graded.

    ``missing_in_store``/``text_conflicts`` mean the eval-time re-chunking
    disagrees with what was actually built — grading against such a store
    would be silently wrong science, so the CLI aborts. ``extra_in_store`` is
    informational (chunks of captures outside this corpus — legitimate at
    Step 4 and later).
    """

    missing_in_store: tuple[str, ...] = ()
    text_conflicts: tuple[str, ...] = ()
    extra_in_store: tuple[str, ...] = ()

    @property
    def fatal(self) -> bool:
        return bool(self.missing_in_store or self.text_conflicts)


def verify_store_chunks(store_texts: Mapping[str, str], rebuilt_texts: Mapping[str, str]) -> ConfigCheck:
    """Assert the store's chunks are exactly what ``build_chunks`` yields now.

    ``store_texts`` maps chunk_id → text for the store being graded;
    ``rebuilt_texts`` maps chunk_id → text from re-chunking the captures with
    the graded config. Equality of ids and texts proves the store was built
    with that config (chunk identity never moves, so a changed chunk size
    makes ids and/or texts disagree here).
    """
    missing = tuple(sorted(chunk_id for chunk_id in rebuilt_texts if chunk_id not in store_texts))
    conflicts = tuple(
        sorted(
            chunk_id for chunk_id, text in rebuilt_texts.items() if chunk_id in store_texts and store_texts[chunk_id] != text
        )
    )
    extra = tuple(sorted(chunk_id for chunk_id in store_texts if chunk_id not in rebuilt_texts))
    return ConfigCheck(missing_in_store=missing, text_conflicts=conflicts, extra_in_store=extra)


# --------------------------------------------------------------------------
# Paragraph → chunk mapping (the golden anchors' bridge into any chunk config)
# --------------------------------------------------------------------------


def paragraph_chunk_map(chunks: Sequence[Chunk]) -> dict[int, list[str]]:
    """Raw paragraph position → the chunk ids whose text it contributed to.

    Chunks must carry ``paragraph_ids`` provenance from the chunker. One
    paragraph cut by the splitter maps to 2+ consecutive chunks; dropped
    paragraphs (headers/footers/pictures, gaps in the numbering) map to none.
    """
    mapping: dict[int, list[str]] = {}
    for chunk in chunks:
        for paragraph_id in chunk.paragraph_ids:
            ids = mapping.setdefault(paragraph_id, [])
            if not ids or ids[-1] != chunk.chunk_id:
                ids.append(chunk.chunk_id)
    return mapping


@dataclass(frozen=True)
class RowGold:
    """What one golden row demands from the ranking (chunk level + document level)."""

    row_id: str
    origin: str
    query_language: str
    expected_language: str = ""
    expected_title: str = ""
    doc_key: DocKey = NO_DOC_KEY
    gold_chunk_ids: frozenset[str] = frozenset()
    unmapped_paragraph_ids: tuple[int, ...] = ()
    unanswerable: bool = False


@dataclass
class GradedSet:
    """Golden rows split by gradability (output of :func:`row_golds`)."""

    golds: list[RowGold] = field(default_factory=list)
    unanswerable: list[RowGold] = field(default_factory=list)
    ungradable: list[str] = field(default_factory=list)
    anomalies: list[str] = field(default_factory=list)


def captures_by_doc_key(captures: Iterable[dict]) -> dict[DocKey, dict]:
    """Index raw captures by their identity tuple; duplicate identities abort."""
    index: dict[DocKey, dict] = {}
    for capture in captures:
        key = (str(capture["instance_key"]), str(capture["shared_id"]), str(capture["language"]))
        if key in index:
            raise ValueError(f"two captures share identity {key} — clean {key[1]}_{key[2]} first")
        index[key] = capture
    return index


def row_golds(
    rows: Sequence[Mapping[str, Any]],
    *,
    captures: Mapping[DocKey, dict],
    config: ChunkConfig,
) -> GradedSet:
    """Map every golden row's anchors to gold chunk sets under ``config``.

    Rows with ``expected: null`` become ``unanswerable`` entries; rows whose
    capture/file identity cannot be found are counted ungradable (with a
    description) instead of crashing the run — a stale row against a fresh
    corpus must downgrade loudly, not silently.
    """
    graded = GradedSet()
    doc_maps: dict[DocKey, dict[int, list[str]]] = {}
    for row in rows:
        row_id = str(row.get("id", ""))
        origin = str(row.get("origin", ""))
        query_language = str(row.get("query_language", ""))
        expected = row.get("expected")
        if not isinstance(expected, dict):
            graded.unanswerable.append(
                RowGold(row_id=row_id, origin=origin, query_language=query_language, doc_key=NO_DOC_KEY)
            )
            continue
        doc_key = (
            str(expected.get("instance_key", "")),
            str(expected.get("shared_id", "")),
            str(expected.get("language", "")),
        )
        capture = captures.get(doc_key)
        if capture is None:
            graded.ungradable.append(f"{row_id}: no capture for {doc_key[1]} ({doc_key[2]})")
            continue
        if capture["file"]["id"] != expected.get("file_id"):
            graded.ungradable.append(f"{row_id}: file_id {expected.get('file_id')!r} no longer matches the capture")
            continue
        doc_map = doc_maps.get(doc_key)
        if doc_map is None:
            doc_map = paragraph_chunk_map(capture_to_chunks(capture, **config_kwargs(config)))
            doc_maps[doc_key] = doc_map
        paragraph_ids = [int(pid) for pid in expected.get("paragraph_ids", [])]
        gold = {chunk_id for pid in paragraph_ids for chunk_id in doc_map.get(pid, [])}
        unmapped = tuple(pid for pid in paragraph_ids if not doc_map.get(pid))
        if unmapped:
            graded.anomalies.append(f"{row_id}: paragraph(s) {list(unmapped)} not keepable under the current drop rule")
        if not gold:
            graded.ungradable.append(f"{row_id}: no expected paragraph maps to a chunk")
            continue
        graded.golds.append(
            RowGold(
                row_id=row_id,
                origin=origin,
                query_language=query_language,
                expected_language=str(expected.get("language", "")),
                expected_title=str(expected.get("title", "")),
                doc_key=doc_key,
                gold_chunk_ids=frozenset(gold),
                unmapped_paragraph_ids=unmapped,
            )
        )
    return graded


def config_kwargs(config: ChunkConfig) -> dict[str, Any]:
    """``build_chunks``/``capture_to_chunks`` keyword arguments for ``config``."""

    return {
        "target_max_chars": config.target_max_chars,
        "overlap_ratio": config.overlap_ratio,
        "prepend_header": config.prepend_header,
    }


# --------------------------------------------------------------------------
# Metrics (chunk level + document level)
# --------------------------------------------------------------------------


def first_gold_rank(hits: Sequence[Hit], gold: frozenset[str]) -> int:
    """1-based rank of the first gold chunk, 0 when none is in the ranking."""
    for position, hit in enumerate(hits, start=1):
        if hit.chunk_id in gold:
            return position
    return 0


def recall_at_k(hits: Sequence[Hit], gold: frozenset[str], k: int) -> float:
    """``|gold ∩ ranked[:k]| / |gold|`` — 0.0 when gold is empty (never graded)."""
    if not gold:
        return 0.0
    top = {hit.chunk_id for hit in hits[:k]}
    return len(top & gold) / len(gold)


def ranked_doc_keys(hits: Sequence[Hit]) -> list[DocKey]:
    """The distinct documents in ranking order (first occurrence dedupes)."""
    seen: set[DocKey] = set()
    order: list[DocKey] = []
    for hit in hits:
        if hit.doc_key not in seen:
            seen.add(hit.doc_key)
            order.append(hit.doc_key)
    return order


def doc_gold_rank(hits: Sequence[Hit], doc_key: DocKey) -> int:
    """1-based rank of the gold document among distinct retrieved docs, 0 if absent."""
    for position, key in enumerate(ranked_doc_keys(hits), start=1):
        if key == doc_key:
            return position
    return 0


# --------------------------------------------------------------------------
# Scoring + aggregation
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class RowScore:
    """One answerable row's metrics."""

    gold: RowGold
    chunk_recall: dict[int, float]
    chunk_mrr: float
    doc_recall: dict[int, float]
    doc_mrr: float


@dataclass(frozen=True)
class LevelScore:
    """Mean metrics of one scope at one level (chunk or document)."""

    rows: int = 0
    recall: dict[int, float] = field(default_factory=dict)
    mrr: float = 0.0


def _mean(values: Sequence[float]) -> float:
    return sum(values) / len(values) if values else 0.0


@dataclass(frozen=True)
class ScopeScore:
    """One scope's chunk- and document-level means (``n`` = rows graded)."""

    label: str
    chunk: LevelScore
    doc: LevelScore

    @property
    def n(self) -> int:
        return self.chunk.rows


@dataclass(frozen=True)
class UnanswerableScore:
    """The expected-nothing rows: excluded from recall/MRR, judged by top-1 only."""

    rows: int
    threshold: float
    top1_scores: dict[str, float]
    false_retrievals: tuple[str, ...]

    @property
    def false_retrieval_rate(self) -> float:
        return len(self.false_retrievals) / self.rows if self.rows else 0.0


@dataclass(frozen=True)
class Scorecard:
    """The full eval result: scoped tables + the unanswerable side-report."""

    scopes: list[ScopeScore]
    answerable_rows: int
    unanswerable: UnanswerableScore
    ungradable: tuple[str, ...] = ()
    anomalies: tuple[str, ...] = ()


def score_rows(
    graded: GradedSet,
    hits_by_row: Mapping[str, Sequence[Hit]],
    *,
    recall_ks: Sequence[int] = RECALL_KS,
    false_retrieval_threshold: float,
) -> Scorecard:
    """Compute the scorecard from per-row ranked hits (pure; caller did retrieval).

    ``graded`` comes from :func:`row_golds`, ``hits_by_row`` maps row id →
    ranked ``Hit``s (``RETRIEVAL_DEPTH`` deep). Rows without hits score 0.
    """
    if not 0.0 <= false_retrieval_threshold <= 1.0:
        raise ValueError(f"false_retrieval_threshold must be in [0, 1], got {false_retrieval_threshold}")
    ks = tuple(sorted(dict.fromkeys(recall_ks)))

    row_scores = [_score_one(gold, hits_by_row.get(gold.row_id, ()), ks) for gold in graded.golds]

    scopes = [
        ScopeScore(
            label=label,
            chunk=_level(subset, "chunk_recall", "chunk_mrr", ks),
            doc=_level(subset, "doc_recall", "doc_mrr", ks),
        )
        for label, subset in _scope_subsets(row_scores)
    ]

    top1_scores: dict[str, float] = {}
    false_rows: list[str] = []
    for gold in graded.unanswerable:
        hits = hits_by_row.get(gold.row_id, ())
        top1 = hits[0].score if hits else 0.0
        top1_scores[gold.row_id] = top1
        if top1 >= false_retrieval_threshold:
            false_rows.append(gold.row_id)

    return Scorecard(
        scopes=scopes,
        answerable_rows=len(row_scores),
        unanswerable=UnanswerableScore(
            rows=len(graded.unanswerable),
            threshold=false_retrieval_threshold,
            top1_scores=top1_scores,
            false_retrievals=tuple(false_rows),
        ),
        ungradable=tuple(graded.ungradable),
        anomalies=tuple(dict.fromkeys(graded.anomalies)),
    )


def _score_one(gold: RowGold, hits: Sequence[Hit], ks: Sequence[int]) -> RowScore:
    chunk_rank = first_gold_rank(hits, gold.gold_chunk_ids)
    doc_rank = doc_gold_rank(hits, gold.doc_key)
    return RowScore(
        gold=gold,
        chunk_recall={k: recall_at_k(hits, gold.gold_chunk_ids, k) for k in ks},
        chunk_mrr=1.0 / chunk_rank if chunk_rank else 0.0,
        doc_recall={k: (1.0 if 0 < doc_rank <= k else 0.0) for k in ks},
        doc_mrr=1.0 / doc_rank if doc_rank else 0.0,
    )


def _scope_subsets(scores: list[RowScore]) -> list[tuple[str, list[RowScore]]]:
    """Fixed eval cuts: overall, per expected language, per origin, cross-language."""
    subsets: list[tuple[str, list[RowScore]]] = [("all", list(scores))]
    languages = sorted({score.gold.expected_language for score in scores if score.gold.expected_language})
    for language in languages:
        subsets.append((language, [s for s in scores if s.gold.expected_language == language]))
    for origin in ("synthetic", "manual"):
        subsets.append((origin, [s for s in scores if s.gold.origin == origin]))
    subsets.append(("cross-language", [s for s in scores if s.gold.query_language != s.gold.expected_language]))
    subsets.append(("same-language", [s for s in scores if s.gold.query_language == s.gold.expected_language]))
    return subsets


def _level(scores: list[RowScore], recall_attr: str, mrr_attr: str, ks: Sequence[int]) -> LevelScore:
    return LevelScore(
        rows=len(scores),
        recall={k: _mean([getattr(score, recall_attr)[k] for score in scores]) for k in ks},
        mrr=_mean([getattr(score, mrr_attr) for score in scores]),
    )


# --------------------------------------------------------------------------
# Rendering (console scorecard + results.md block — same facts, one table)
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class RunFacts:
    """The run's identity and conditions, printed with every scorecard."""

    label: str
    started_at_utc: str
    elapsed_seconds: float
    golden_path: str
    rows: int
    synthetic_rows: int
    manual_rows: int
    store_path: str
    store_chunks: int
    store_model: str
    store_dimensions: int
    store_created_at_utc: str
    config: ChunkConfig
    false_retrieval_threshold: float
    retrieval_depth: int = RETRIEVAL_DEPTH


def _percent(value: float) -> str:
    return f"{100 * value:.1f}%"


def _table_lines(scopes: Sequence[ScopeScore], ks: Sequence[int]) -> list[str]:
    """The scoped markdown table: chunk-level columns then doc-level columns."""
    lines = [
        "| scope | n | "
        + " | ".join(f"chunk R@{k}" for k in ks)
        + " | chunk MRR | "
        + " | ".join(f"doc R@{k}" for k in ks)
        + " | doc MRR |",
        "|" + "---|" * (4 + 2 * len(ks)),
    ]
    for scope in scopes:
        prefix = "" if scope.n else "—"  # empty scope: every cell reads —
        chunk_cells = [_percent(scope.chunk.recall[k]) if scope.n else prefix for k in ks] + [
            f"{scope.chunk.mrr:.3f}" if scope.n else prefix
        ]
        doc_cells = [f"{_percent(scope.doc.recall[k])}" if scope.n else prefix for k in ks] + [
            f"{scope.doc.mrr:.3f}" if scope.n else prefix
        ]
        lines.append(f"| {scope.label} | {scope.n} | " + " | ".join(chunk_cells + doc_cells) + " |")
    return lines


def render(run: RunFacts, card: Scorecard, *, heading: bool) -> str:
    """Render the scorecard for the console (``heading=False``) or results.md (``True``)."""
    lines: list[str] = []
    if heading:
        lines.append(f"## {run.started_at_utc} — {run.label}")
        lines.append("")
    lines.append(f"label: {run.label}")
    lines.append(
        f"store: `{run.store_path}` — {run.store_chunks:,} chunks, {run.store_model} "
        f"({run.store_dimensions}d), built {run.store_created_at_utc}"
    )
    lines.append(
        f"golden: `{run.golden_path}` — {run.rows} rows ({run.synthetic_rows} synthetic / "
        f"{run.manual_rows} manual); ranked depth {run.retrieval_depth}"
    )
    lines.append(
        f"chunk config: max-chars {run.config.target_max_chars}, overlap {run.config.overlap_ratio:g}, "
        f"header {'on' if run.config.prepend_header else 'OFF'}"
    )
    ks = sorted(card.scopes[0].chunk.recall) if card.scopes else list(RECALL_KS)
    lines.append("")
    lines.extend(_table_lines(card.scopes, ks))
    lines.append("")
    unans = card.unanswerable
    per_row = (
        " (top-1: " + ", ".join(f"{rid} {score:.4f}" for rid, score in unans.top1_scores.items()) + ")"
        if unans.top1_scores
        else ""
    )
    lines.append(
        f"Unanswerable: {unans.rows} rows, threshold ≥ {unans.threshold:.3f} → false-retrieval "
        f"{len(unans.false_retrievals)}/{unans.rows} ({_percent(unans.false_retrieval_rate)})" + per_row
    )
    for note in card.ungradable:
        lines.append(f"ungradable: {note}")
    for note in card.anomalies:
        lines.append(f"anomaly: {note}")
    return "\n".join(lines) + "\n"
