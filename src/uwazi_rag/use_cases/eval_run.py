"""One golden-set grading run, shared by `eval` and `benchmark` (Step 3.5).

The drivers hand in paths + ports; this module owns the shared grading
sequence — load a store, verify its chunk config against a re-chunk of the
captures, grade the golden rows, rank them (by retrieval method), score. One
code path means `eval`'s numbers and `benchmark`'s are computed the same way
by construction; the commands differ only in labels, console output, and how
many experiments they wrap.

Ranking methods (``RETRIEVAL_METHODS``) grow with the PLAN steps: ``embedding``
(cosine over the store's own embedding model), ``bm25`` (lexical BM25 over the
store's chunk texts) and ``rrf`` (reciprocal rank fusion of both). Whatever
the method, hits keep the same ``Hit`` shape so ``score_rows`` grades all
methods identically — cosine-specific metrics (false-retrieval) simply stay
empty for the non-cosine ones.

Impure but offline-deterministic: the file loads here are the ones the CLI
already made (tested offline against committed fixtures); embedding goes
through the ``EmbeddingPort``. Tests use the committed fixtures +
``HashingEmbedding`` + a real saved ``NaiveVectorStore`` — never Ollama.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from uwazi_rag.adapters.naive_vector_store import NaiveVectorStore
from uwazi_rag.configuration import ROOT_PATH
from uwazi_rag.ports.embedding_port import EmbeddingPort
from uwazi_rag.use_cases.bm25 import Bm25Index
from uwazi_rag.use_cases.build_golden import read_jsonl
from uwazi_rag.use_cases.eval_retrieval import (
    RESULTS_HEADER,
    RETRIEVAL_DEPTH,
    ChunkConfig,
    ConfigCheck,
    DocKey,
    GradedSet,
    Hit,
    RunFacts,
    captures_by_doc_key,
    config_kwargs,
    hits_from_store,
    row_golds,
    verify_store_chunks,
)
from uwazi_rag.use_cases.index_captures import capture_to_chunks, load_captures
from uwazi_rag.use_cases.rank_fusion import fused_ranking, rrf_scores

# Ranking methods a benchmark experiment (or a later `eval` flag) may ask
# for; anything else is rejected loudly at spec-parse rank. ``bm25``/``rrf``
# are the Step 3.5 hybrid preview: lexical scoring and fused cosine+lexical.
RETRIEVAL_METHODS: tuple[str, ...] = ("embedding", "bm25", "rrf")
# One POST /api/embed per batch of golden questions (eval's proven batch size).
EMBED_BATCH_SIZE = 64


class EvalInputsError(RuntimeError):
    """A grading run's inputs disagree (store vs corpus vs golden) — fatal and self-explaining."""


@dataclass(frozen=True)
class PreparedRun:
    """Everything one grading experiment needs, loaded + verified once.

    Both ``eval`` and ``benchmark`` grade exactly this object — equality of
    the two commands' numbers is structural, not hoped-for.
    """

    store: NaiveVectorStore
    store_path: Path
    raw_dir: Path
    golden_path: Path
    rows: list[dict[str, Any]]
    config: ChunkConfig
    graded: GradedSet
    check: ConfigCheck


def prepare_run(*, store_path: Path, raw_dir: Path, golden_path: Path) -> PreparedRun:
    """Load store + captures + golden rows and verify they agree.

    Raises :class:`EvalInputsError` (self-explaining) when the store's chunks
    do not match its recorded chunk config, or when no golden row is gradable
    against ``raw_dir``; load errors (missing files, bad store schema)
    propagate to the caller.
    """
    store = NaiveVectorStore.load(store_path)
    rows = read_jsonl(golden_path)
    captures = load_captures(raw_dir)
    config = ChunkConfig.from_store(store.chunk_config)

    store_texts = {chunk.chunk_id: chunk.text for chunk in store.chunks()}
    rebuilt_texts = {
        chunk.chunk_id: chunk.text
        for capture in captures
        if capture["segmentation_status"] == "ready"
        for chunk in capture_to_chunks(capture, **config_kwargs(config))
    }
    check = verify_store_chunks(store_texts, rebuilt_texts)
    if check.fatal:
        raise EvalInputsError(
            f"store {store_path.name} does not match the chunk config being graded "
            f"({len(check.missing_in_store)} chunks missing, {len(check.text_conflicts)} text conflicts)\n"
            f"hint: the store's recorded chunk config is {store.chunk_config or 'none (legacy)'} and "
            f"{config.target_max_chars}/{config.overlap_ratio:g}/header={'on' if config.prepend_header else 'off'} "
            "was graded — re-run build-index with the same config as this store, or point --store at the matching store"
        )

    graded = row_golds(rows, captures=captures_by_doc_key(captures), config=config)
    if not graded.golds:
        raise EvalInputsError(
            f"no golden row could be graded against {raw_dir} ({len(graded.ungradable)} ungradable) — "
            "corpus and golden set disagree; check --source"
        )
    return PreparedRun(
        store=store,
        store_path=store_path,
        raw_dir=raw_dir,
        golden_path=golden_path,
        rows=rows,
        config=config,
        graded=graded,
        check=check,
    )


def rank_rows(prepared: PreparedRun, *, retrieval: str, embedder: EmbeddingPort | None = None) -> dict[str, list[Hit]]:
    """Rank every golden row against ``prepared.store``; the method picks the ranker.

    ``embedding`` embeds the questions through ``embedder`` — which must
    match the store's model — and cosine-scans to ``RETRIEVAL_DEPTH`` depth.
    Unknown methods are rejected loudly (``RETRIEVAL_METHODS`` is the law).
    """
    if retrieval not in RETRIEVAL_METHODS:
        raise ValueError(f"retrieval method {retrieval!r} is not implemented (available: {', '.join(RETRIEVAL_METHODS)})")
    if retrieval == "embedding":
        if embedder is None:
            raise ValueError("retrieval 'embedding' needs an embedder — build one for the store's model")
        return _rank_by_embedding(prepared, embedder)
    if retrieval == "rrf":
        if embedder is None:
            raise ValueError("retrieval 'rrf' needs an embedder — build one for the store's model")
        return _rank_by_rrf(prepared, embedder)
    if retrieval == "bm25":
        return _rank_by_bm25(prepared)
    raise ValueError(f"retrieval method {retrieval!r} is in RETRIEVAL_METHODS but has no ranker wired")


def _rank_by_embedding(prepared: PreparedRun, embedder: EmbeddingPort) -> dict[str, list[Hit]]:
    """Embed questions in batches with the store's own model and cosine-ranked hits."""
    store = prepared.store
    model = getattr(embedder, "model", None)
    if model is not None and model != store.embedding_model:
        raise ValueError(
            f"query embedder model {model!r} differs from the store's model {store.embedding_model!r} — "
            "cosine across embedding spaces is meaningless; one store, one model"
        )
    hits_by_row: dict[str, list[Hit]] = {}
    batch: list[dict[str, Any]] = []
    for row in prepared.rows:
        batch.append(row)
        if len(batch) >= EMBED_BATCH_SIZE:
            _embed_batch(embedder, batch, store, hits_by_row)
            batch = []
    _embed_batch(embedder, batch, store, hits_by_row)
    return hits_by_row


def _embed_batch(
    embedder: EmbeddingPort,
    rows: list[dict[str, Any]],
    store: NaiveVectorStore,
    hits_by_row: dict[str, list[Hit]],
) -> None:
    """Embed one batch of golden questions and record their ranked hits."""
    if not rows:
        return
    vectors = embedder.embed([str(row["question"]) for row in rows])
    for row, vector in zip(rows, vectors, strict=True):
        hits_by_row[str(row["id"])] = hits_from_store(store.search(vector, k=RETRIEVAL_DEPTH))


def _rank_by_bm25(prepared: PreparedRun) -> dict[str, list[Hit]]:
    """Rank chunks lexicographically — the store contributes texts only, no embeddings."""
    chunks = prepared.store.chunks()
    doc_keys: dict[str, DocKey] = {chunk.chunk_id: (chunk.instance_key, chunk.shared_id, chunk.language) for chunk in chunks}
    index = Bm25Index({chunk.chunk_id: chunk.text for chunk in chunks})
    hits_by_row: dict[str, list[Hit]] = {}
    for row in prepared.rows:
        hits_by_row[str(row["id"])] = [
            Hit(chunk_id=chunk_id, doc_key=doc_keys[chunk_id], score=score)
            for chunk_id, score in index.score(str(row["question"]))[:RETRIEVAL_DEPTH]
        ]
    return hits_by_row


def _rank_by_rrf(prepared: PreparedRun, embedder: EmbeddingPort) -> dict[str, list[Hit]]:
    """Fuse the store's cosine ranking with BM25 (reciprocal rank, k = 60)."""
    embed_hits = _rank_by_embedding(prepared, embedder)
    bm25_hits = _rank_by_bm25(prepared)
    doc_keys: dict[str, DocKey] = {
        chunk.chunk_id: (chunk.instance_key, chunk.shared_id, chunk.language) for chunk in prepared.store.chunks()
    }
    fused: dict[str, list[Hit]] = {}
    for row in prepared.rows:
        row_id = str(row["id"])
        rankings = [
            [hit.chunk_id for hit in embed_hits.get(row_id, ())],
            [hit.chunk_id for hit in bm25_hits.get(row_id, ())],
        ]
        scores = rrf_scores(rankings)
        fused[row_id] = [
            Hit(chunk_id=chunk_id, doc_key=doc_keys[chunk_id], score=scores[chunk_id])
            for chunk_id in fused_ranking(rankings)[:RETRIEVAL_DEPTH]
        ]
    return fused


def build_run_facts(
    prepared: PreparedRun,
    *,
    label: str,
    started_at_utc: str,
    elapsed_seconds: float,
    false_retrieval_threshold: float,
) -> RunFacts:
    """The RunFacts block both commands log — identical fields for identical runs."""
    rows = prepared.rows
    return RunFacts(
        label=label,
        started_at_utc=started_at_utc,
        elapsed_seconds=elapsed_seconds,
        golden_path=_display_path(prepared.golden_path),
        rows=len(rows),
        synthetic_rows=sum(1 for row in rows if row.get("origin") == "synthetic"),
        manual_rows=sum(1 for row in rows if row.get("origin") == "manual"),
        store_path=_display_path(prepared.store_path),
        store_chunks=len(prepared.store),
        store_model=prepared.store.embedding_model,
        store_dimensions=prepared.store.dimensions,
        store_created_at_utc=prepared.store.created_at_utc,
        config=prepared.config,
        false_retrieval_threshold=false_retrieval_threshold,
    )


def append_results(results_path: Path, block_text: str) -> None:
    """Append one rendered block to the results log (creating the headered file first)."""
    if not results_path.exists():
        results_path.write_text(RESULTS_HEADER, encoding="utf-8")
    with results_path.open("a", encoding="utf-8") as stream:
        stream.write("\n")
        stream.write(block_text)
        stream.write("\n")


def _display_path(path: Path) -> str:
    """Repo-relative when the path lives inside the repo (results.md stays portable)."""
    try:
        return str(path.relative_to(ROOT_PATH))
    except ValueError:
        return str(path)
