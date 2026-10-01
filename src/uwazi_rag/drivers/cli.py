from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from uwazi_api.client import UwaziClient
from uwazi_api.domain.exceptions import SegmentationNotFoundError

from uwazi_rag import configuration
from uwazi_rag.adapters.naive_vector_store import NaiveStoreMismatchError, NaiveVectorStore
from uwazi_rag.adapters.ollama_embeddings import OllamaEmbeddings
from uwazi_rag.adapters.ollama_llm import OllamaLlm
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
from uwazi_rag.use_cases.build_golden import (
    GOLDEN_FILE,
    PASSAGES_FILE,
    build_golden_dataset,
    describe_run,
    merge_manual_rows,
    read_jsonl,
    write_passages_file,
)
from uwazi_rag.use_cases.chunking import OVERLAP_RATIO, TARGET_MAX_CHARS, build_chunks
from uwazi_rag.use_cases.embed_probe import format_probe_report, run_embed_probe
from uwazi_rag.use_cases.eval_retrieval import RESULTS_FILE, render, score_rows
from uwazi_rag.use_cases.eval_run import (
    EvalInputsError,
    append_results,
    build_run_facts,
    prepare_run,
    rank_rows,
)
from uwazi_rag.use_cases.fetch_document import (
    capture_entity,
    pages_covered,
    write_raw_capture,
)
from uwazi_rag.use_cases.index_captures import IndexStats, index_captures
from uwazi_rag.use_cases.passage_groups import GROUPS_PER_DOCUMENT, build_passage_groups, format_group_view
from uwazi_rag.use_cases.semantic_search import format_search_results, semantic_search


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="uwazi-rag",
        description="Semantic search + RAG for Uwazi collections (see PLAN.md).",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    hello = subparsers.add_parser("hello", help="embedding smoke test: embed one sentence via Ollama (Step 0)")
    hello.add_argument("--text", default="Witnesses reported that armed men took the prisoners away at night.")

    fetch = subparsers.add_parser("fetch", help="capture one entity's text from Uwazi as a fixture (Step 1)")
    fetch.add_argument("shared_id")
    fetch.add_argument("--language", default="en")

    chunk = subparsers.add_parser("chunk", help="dev: chunk a captured segmentation offline and print stats (Step 2)")
    chunk.add_argument("shared_id")
    chunk.add_argument("--language", default="en")

    index = subparsers.add_parser("index", help="index a template's pubhed entities (Step 4)")
    index.add_argument("--template")
    index.add_argument("--all", action="store_true")

    build_index = subparsers.add_parser(
        "build-index",
        help="chunk + embed every capture of the configured instance into the naive store (Step 3)",
    )
    build_index.add_argument("--source", default=None, help="captures dir (default: data/raw/<instance_key> from .env)")
    build_index.add_argument("--output", default=None, help="store path (default: data/naive_store.json)")
    build_index.add_argument("--batch-size", type=int, default=32)
    build_index.add_argument("--limit", type=int, default=None, help="index at most N captures (smoke test)")
    build_index.add_argument(
        "--max-chars",
        type=int,
        default=TARGET_MAX_CHARS,
        help=f"chunk character budget for the eval sweep (default: Step 2 constant {TARGET_MAX_CHARS})",
    )
    build_index.add_argument(
        "--overlap",
        type=float,
        default=OVERLAP_RATIO,
        help=f"overlap fraction of split long paragraphs (default: Step 2 constant {OVERLAP_RATIO})",
    )
    build_index.add_argument(
        "--no-header",
        action="store_true",
        help="omit the '{title} — {template} (page n)' context header from chunk text",
    )
    build_index.add_argument(
        "--embedding-model",
        default=None,
        help="embedding model for a benchmark store (default: EMBEDDING_MODEL from .env)",
    )
    build_index.add_argument(
        "--embedding-dimensions",
        type=int,
        default=None,
        help="vector size of --embedding-model (default: probed at runtime when the model is overridden)",
    )

    search = subparsers.add_parser(
        "search",
        help="embed the query, cosine-scan the naive store, print the top hits (Step 3; hybrid in Step 5)",
    )
    search.add_argument("query")
    search.add_argument("--top", type=int, default=5, help="how many hits to print (default 5)")
    search.add_argument("--store", default=None, help="naive store path (default: data/naive_store.json)")

    build_golden = subparsers.add_parser(
        "build-golden",
        help="LLM-drafts the golden retrieval-eval questions, anchored to passage groups (Step 3.5)",
    )
    build_golden.add_argument(
        "--samples-per-document", type=int, default=GROUPS_PER_DOCUMENT, help="passage groups per capture (default 2)"
    )
    build_golden.add_argument("--limit", type=int, default=None, help="process at most N captures (smoke run)")
    build_golden.add_argument("--output", default=None, help="evaluation dir (default: data/eval)")
    build_golden.add_argument(
        "--merge-manual",
        action="store_true",
        help="merge-only: validate + merge hand-written manual.jsonl rows into golden.jsonl (no LLM calls)",
    )
    build_golden.add_argument(
        "--passages-only",
        action="store_true",
        help="recreate passages.jsonl offline (no LLM) from the captures — for a lost/stale review file",
    )
    build_golden.add_argument(
        "--dry-run",
        action="store_true",
        help="print the sampling plan (groups, sizes, cross-language picks) without LLM calls",
    )

    show_group = subparsers.add_parser(
        "show-group",
        help="dev: pretty-print one passage group + neighbors, offline from the captures (Step 3.5)",
    )
    show_group.add_argument("group_id", help="e.g. bdd5a7c445847b35:00r9afbvijp6:en:g0000")
    show_group.add_argument("--source", default=None, help="captures dir (default: data/raw/<instance_key> from .env)")

    ask = subparsers.add_parser("ask", help="RAG answer with citations (Step 6)")
    ask.add_argument("question")

    eval = subparsers.add_parser(
        "eval",
        help="golden-set retrieval scorecard; appends a dated, labeled block to data/eval/results.md (Step 3.5)",
    )
    eval.add_argument(
        "--label", required=True, help="this run's name in results.md (see the existing blocks for house style)"
    )
    eval.add_argument(
        "--store",
        default=None,
        help="naive store path (default: data/naive_store.json) — its recorded chunk config and embedding model are graded",
    )
    eval.add_argument("--source", default=None, help="captures dir (default: data/raw/<instance_key> from .env)")

    benchmark = subparsers.add_parser(
        "benchmark",
        help="run a sweep spec: build each [stores] block once, grade its [[experiments]], append a comparison (Step 3.5)",
    )
    benchmark.add_argument(
        "--config",
        required=True,
        help="benchmark TOML (e.g. benchmarks/sweep1-chunking.toml) — [stores.<slug>] + [[experiments]]",
    )
    benchmark.add_argument(
        "--only",
        default=None,
        help="run a single named experiment (other experiments are skipped, stores untouched)",
    )
    benchmark.add_argument(
        "--dry-run",
        action="store_true",
        help="print the grid (stores + experiments) without building or grading anything",
    )
    benchmark.add_argument("--source", default=None, help="captures dir (default: data/raw/<instance_key> from .env)")

    for name in ("serve", "sync"):
        subparsers.add_parser(name, help="stub — implemented in a later PLAN step")

    return parser


def _run_hello(args: argparse.Namespace) -> int:
    probe = run_embed_probe(
        OllamaEmbeddings(),
        text=args.text,
        model=configuration.EMBEDDING_MODEL,
        base_url=configuration.OLLAMA_BASE_URL,
    )
    print(format_probe_report(probe, configuration.EMBEDDING_DIMENSIONS))
    if probe.dimensions != configuration.EMBEDDING_DIMENSIONS:
        hint = (
            "hint: EMBEDDING_DIMENSIONS (config) does not match the model's real output — "
            f"check the model card of '{probe.model}' and .env, or pull the model with `ollama pull {probe.model}`"
        )
        print(hint, file=sys.stderr)
        return 1
    return 0


def _run_fetch(args: argparse.Namespace) -> int:
    url, user, password = configuration.uwazi_credentials()
    client = UwaziClient(url=url, user=user, password=password)
    try:
        capture = capture_entity(client, shared_id=args.shared_id, language=args.language, url=url)
    except SegmentationNotFoundError as error:
        print(f"error: {error}", file=sys.stderr)
        print(
            "hint: segment the document first — segmentation status shows in Mongo collection 'segmentations'.",
            file=sys.stderr,
        )
        return 1
    except Exception as error:  # driver boundary: one bad fetch must not crash the shell
        print(f"error: fetch failed — is Uwazi reachable at {url}? | {error}", file=sys.stderr)
        return 1

    raw_path, fixture_path, fixture_updated = write_raw_capture(
        capture, instance_key=configuration.instance_key(url), raw_dir=configuration.RAW_DIR
    )

    pages = pages_covered(capture["paragraphs"])
    print(f"entity : {capture['shared_id']} ({capture['language']}) — {capture['title']}")
    print(f"file   : {capture['file']['name']} ({capture['file']['id']})")
    print(
        f"paras  : {len(capture['paragraphs'])} — status '{capture['segmentation_status']}'"
        + (f", pages {pages[0]}..{pages[1]}" if pages else "")
    )
    print(f"wrote  : {raw_path}")
    print(f"{'wrote' if fixture_updated else 'kept'}  : {fixture_path}")
    if not fixture_updated:
        print("(fixture content unchanged — fetch timestamp excluded)")
    if capture["segmentation_status"] != "ready":
        print(f"warning: segmentation status is '{capture['segmentation_status']}', not 'ready'", file=sys.stderr)
        return 1
    return 0


def _run_chunk(args: argparse.Namespace) -> int:
    url, _, _ = configuration.uwazi_credentials()
    capture_path = configuration.RAW_DIR / configuration.instance_key(url) / f"{args.shared_id}_{args.language}.json"
    if not capture_path.exists():
        print(
            f"error: no capture at {capture_path} — run `uwazi-rag fetch {args.shared_id} --language {args.language}` first",
            file=sys.stderr,
        )
        return 1
    capture = json.loads(capture_path.read_text(encoding="utf-8"))
    chunks = build_chunks(
        capture["paragraphs"],
        instance_key=capture["instance_key"],
        shared_id=capture["shared_id"],
        language=capture["language"],
        file_id=capture["file"]["id"],
        entity_title=capture["title"],
        template_name=capture["template"]["name"],
    )
    if not chunks:
        print("warning: capture produced no chunks (no keepable text)", file=sys.stderr)
        return 1
    sizes = [len(chunk.text) for chunk in chunks]
    pages_start = [chunk.page_start for chunk in chunks if chunk.page_start is not None]
    pages_end = [chunk.page_end for chunk in chunks if chunk.page_end is not None]
    print(f"entity : {capture['shared_id']} ({capture['language']}) — {capture['title']}")
    print(f"chunks : {len(chunks)} — avg {sum(sizes) // len(sizes)} chars, range {min(sizes)}..{max(sizes)}")
    if pages_start:
        print(f"pages  : {min(pages_start)}..{max(pages_end)}")
    return 0


def _build_naive_store(
    *,
    store_path: Path,
    raw_dir: Path,
    model: str,
    declared_dimensions: int | None,
    probe: bool,
    max_chars: int,
    overlap: float,
    header: bool,
    batch_size: int = 32,
    limit: int | None = None,
) -> tuple[IndexStats, int]:
    """Chunk + embed the captures into one saved store (build-index and benchmark share this).

    Dimensions: ``declared`` wins; else the model is probed once (``probe=True``,
    i.e. whenever the model was named explicitly — the benchmark always names
    its models); else the configured ``EMBEDDING_DIMENSIONS``. The store
    records chunk_config + model so grading later verifies exactly what this
    built. Raises ``ValueError``/``RuntimeError``/``OSError`` for the caller to
    present.
    """
    if declared_dimensions:
        dimensions = declared_dimensions
    elif probe:
        try:
            probe_result = run_embed_probe(
                OllamaEmbeddings(model=model, base_url=configuration.OLLAMA_BASE_URL),
                text="uwazi-rag dimension probe (store build)",
                model=model,
                base_url=configuration.OLLAMA_BASE_URL,
            )
            dimensions = probe_result.dimensions
        except (RuntimeError, ValueError) as error:
            raise ValueError(f"could not probe {model}'s vector size — {error}") from error
    else:
        dimensions = configuration.EMBEDDING_DIMENSIONS

    store = NaiveVectorStore(
        dimensions=dimensions,
        embedding_model=model,
        chunk_config={"target_max_chars": max_chars, "overlap_ratio": overlap, "prepend_header": header},
    )
    stats = index_captures(
        raw_dir=raw_dir,
        store=store,
        embedder=OllamaEmbeddings(model=model, base_url=configuration.OLLAMA_BASE_URL),
        expected_dimensions=dimensions,
        batch_size=batch_size,
        limit=limit,
        target_max_chars=max_chars,
        overlap_ratio=overlap,
        prepend_header=header,
    )
    store.save(store_path)
    return stats, dimensions


def _run_build_index(args: argparse.Namespace) -> int:
    """Step 3: chunk + embed all captured docs of the configured instance, once.

    Step 3.5 grew the benchmark surface: chunking knobs (``--max-chars``,
    ``--overlap``, ``--no-header``) and an embedding-model override (``--embedding-model``
    + probed/declared ``--embedding-dimensions``). Both are recorded in the
    store so `eval` grades exactly what was built.
    """
    model = args.embedding_model or configuration.EMBEDDING_MODEL
    output = Path(args.output) if args.output else configuration.NAIVE_STORE_PATH
    try:
        url, _, _ = configuration.uwazi_credentials()
        raw_dir = Path(args.source) if args.source else configuration.RAW_DIR / configuration.instance_key(url)
        stats, dimensions = _build_naive_store(
            store_path=output,
            raw_dir=raw_dir,
            model=model,
            declared_dimensions=args.embedding_dimensions,
            probe=bool(args.embedding_model),
            max_chars=args.max_chars,
            overlap=args.overlap,
            header=not args.no_header,
            batch_size=args.batch_size,
            limit=args.limit,
        )
    except (ValueError, RuntimeError, OSError) as error:
        print(f"error: build-index failed — {error}", file=sys.stderr)
        print(
            f"hint: embedding needs Ollama serving '{model}'"
            f" at {configuration.OLLAMA_BASE_URL}; captures come from `uwazi-rag fetch` / the seed script",
            file=sys.stderr,
        )
        return 1

    print(f"model   : {model} ({dimensions} dims)")
    print(f"chunking: max-chars {args.max_chars}, overlap {args.overlap:g}, header {'on' if not args.no_header else 'OFF'}")
    print(
        f"captures: {stats.captures_indexed}/{stats.captures_seen} indexed"
        f" — {stats.skipped_not_ready} not ready, {stats.skipped_no_chunks} without keepable text"
    )
    print(f"chunks  : {stats.chunks_indexed}")
    print(f"wrote   : {output}")
    return 0


def _run_search(args: argparse.Namespace) -> int:
    store_path = Path(args.store) if args.store else configuration.NAIVE_STORE_PATH
    if not store_path.exists():
        print(f"error: no naive index at {store_path} — run `uwazi-rag build-index` first", file=sys.stderr)
        return 1
    try:
        store = NaiveVectorStore.load(
            store_path,
            embedding_model=configuration.EMBEDDING_MODEL,
            dimensions=configuration.EMBEDDING_DIMENSIONS,
        )
        hits = semantic_search(query=args.query, store=store, embedder=OllamaEmbeddings(), k=args.top)
    except (NaiveStoreMismatchError, RuntimeError, ValueError) as error:
        print(f"error: search failed — {error}", file=sys.stderr)
        print(
            f"hint: the query embedding needs Ollama at {configuration.OLLAMA_BASE_URL}"
            " (`ollama serve`); a store/model mismatch → rebuild with `uwazi-rag build-index`",
            file=sys.stderr,
        )
        return 1

    print(f"query  : {args.query}")
    print(f"index  : {store_path} — {len(store)} chunks, model '{store.embedding_model}'")
    print(format_search_results(hits, base_url=configuration.UWAZI_URL or None))
    return 0


def _run_build_golden(args: argparse.Namespace) -> int:
    """Step 3.5 (dataset half): draft golden questions, or run an offline mode."""
    output_dir = Path(args.output) if args.output else configuration.EVAL_DIR
    modes = [
        flag
        for requested, flag in (
            (args.merge_manual, "--merge-manual"),
            (args.passages_only, "--passages-only"),
            (args.dry_run, "--dry-run"),
        )
        if requested
    ]
    if len(modes) > 1:
        print(f"error: pick exactly one of {' or '.join(modes)}", file=sys.stderr)
        return 2

    if args.passages_only:
        try:
            url = configuration.uwazi_url()
            stats = write_passages_file(
                raw_dir=configuration.RAW_DIR / configuration.instance_key(url),
                output_dir=output_dir,
                samples_per_document=args.samples_per_document,
                limit=args.limit,
            )
        except (ValueError, RuntimeError, OSError) as error:
            print(f"error: passages-only failed — {error}", file=sys.stderr)
            return 1
        print(
            f"captures : {stats.captures_used}/{stats.captures_seen} used — "
            f"{stats.skipped_not_ready} not ready, {stats.skipped_no_groups} skipped"
        )
        print(f"passages : {stats.groups_sampled} sampled groups of {stats.groups_total} built")
        print("wrote    : " + "; ".join(stats.outputs))
        return 0

    if args.merge_manual:
        try:
            merge_stats = merge_manual_rows(eval_dir=output_dir)
        except (OSError, ValueError, RuntimeError) as error:
            print(f"error: merge-manual failed — {error}", file=sys.stderr)
            print(
                "hint: manual rows need origin 'manual', a real source_group_id, and the "
                f"expected block copied from the passages.jsonl of {output_dir}",
                file=sys.stderr,
            )
            return 1
        print(f"golden  : {merge_stats.golden_rows_before} → {merge_stats.golden_rows_after} rows")
        print(
            f"manual  : {merge_stats.manual_rows_merged} merged — {merge_stats.example_rows_skipped} template rows "
            f"skipped, {merge_stats.manual_rows_skipped_duplicated} already present, "
            f"{merge_stats.ids_autoassigned} ids auto-assigned"
        )
        print(f"wrote   : {output_dir / GOLDEN_FILE}")
        return 0

    try:
        url = configuration.uwazi_url()
        raw_dir = configuration.RAW_DIR / configuration.instance_key(url)
        llm = OllamaLlm()
        stats = build_golden_dataset(
            raw_dir=raw_dir,
            llm=llm,
            output_dir=output_dir,
            samples_per_document=args.samples_per_document,
            limit=args.limit,
            dry_run=args.dry_run,
            llm_description=f"Ollama chat '{llm.model}' at {llm.base_url} (Ollama defaults, non-streaming)",
        )
    except (ValueError, RuntimeError, OSError) as error:
        print(f"error: build-golden failed — {error}", file=sys.stderr)
        print(
            f"hint: question drafts need Ollama serving '{configuration.LLM_MODEL}' at {configuration.OLLAMA_BASE_URL} "
            f"(`ollama serve`, `ollama pull {configuration.LLM_MODEL}`); captures come from `uwazi-rag fetch`",
            file=sys.stderr,
        )
        return 1

    if args.dry_run:
        for line in stats.plan_lines:
            print(line)
        print(
            f"plan     : {stats.groups_sampled} groups over {stats.captures_used}/{stats.captures_seen} captures "
            "(seeded sampling — see data/eval/about.md after a real run); nothing written"
        )
        return 0
    print(describe_run(stats))
    if stats.rows_written == 0 and stats.captures_used:
        print("error: no questions were generated — see the failures above", file=sys.stderr)
        return 1
    return 0


def _run_show_group(args: argparse.Namespace) -> int:
    """Step 3.5 dev tool: one passage group + neighbors, fully offline from the captures."""
    parts = str(args.group_id).split(":")
    if len(parts) != 4 or not parts[3].startswith("g") or not parts[3][1:].isdigit():
        print(
            f'error: group ids look like "<instance_key>:<shared_id>:<lang>:g0004" — got {args.group_id!r}',
            file=sys.stderr,
        )
        return 1
    _, shared_id, language, suffix = parts
    try:
        url = configuration.uwazi_url()
        raw_dir = Path(args.source) if args.source else configuration.RAW_DIR / configuration.instance_key(url)
        capture_path = raw_dir / f"{shared_id}_{language}.json"
        if not capture_path.exists():
            print(
                f"error: no capture at {capture_path} — run `uwazi-rag fetch {shared_id} --language {language}` "
                "or point --source at the right captures dir",
                file=sys.stderr,
            )
            return 1
        capture = json.loads(capture_path.read_text(encoding="utf-8"))
        if str(capture["instance_key"]) != parts[0]:
            print(
                f"error: {args.group_id} names instance {parts[0]!r} but that capture belongs to "
                f"{capture['instance_key']!r} — point --source at the right captures dir",
                file=sys.stderr,
            )
            return 1
        groups = build_passage_groups(
            capture["paragraphs"],
            instance_key=capture["instance_key"],
            shared_id=capture["shared_id"],
            language=capture["language"],
            file_id=capture["file"]["id"],
            title=capture["title"],
        )
        index = int(suffix[1:])
        if not 0 <= index < len(groups):
            print(
                f"error: {args.group_id} is out of range — {shared_id}_{language} has {len(groups)} groups "
                f"(g0000..g{len(groups) - 1:04d})",
                file=sys.stderr,
            )
            return 1
    except (ValueError, RuntimeError, OSError) as error:
        print(f"error: show-group failed — {error}", file=sys.stderr)
        return 1
    sampled: set[str] = set()
    if (configuration.EVAL_DIR / PASSAGES_FILE).exists():
        sampled = {str(row["group_id"]) for row in read_jsonl(configuration.EVAL_DIR / PASSAGES_FILE)}
    print(format_group_view(groups[index], all_groups=groups, sampled_ids=sampled))
    return 0


def _run_eval(args: argparse.Namespace) -> int:
    """Step 3.5 (scorecard half): embed golden questions, grade the store, log results.

    The whole grading sequence is the shared path in
    :mod:`uwazi_rag.use_cases.eval_run` — the same one `benchmark` uses, so a
    sweep point against the same store cannot disagree with an `eval` run.
    """
    store_path = Path(args.store) if args.store else configuration.NAIVE_STORE_PATH
    try:
        url = configuration.uwazi_url()
        raw_dir = Path(args.source) if args.source else configuration.RAW_DIR / configuration.instance_key(url)
        prepared = prepare_run(
            store_path=store_path,
            raw_dir=raw_dir,
            golden_path=configuration.EVAL_DIR / GOLDEN_FILE,
        )
    except (NaiveStoreMismatchError, EvalInputsError, OSError) as error:
        print(f"error: eval could not load its inputs — {error}", file=sys.stderr)
        print(
            "hint: a store comes from `uwazi-rag build-index`, the golden set from "
            f"uwazi-rag build-golden; captures live in {configuration.RAW_DIR}/<instance_key>",
            file=sys.stderr,
        )
        return 1
    if prepared.check.extra_in_store:
        print(
            f"note: {len(prepared.check.extra_in_store)} store chunks belong to captures outside {raw_dir} "
            "(indexed earlier from a wider corpus) — they stay in the ranking",
            file=sys.stderr,
        )
    for note in prepared.graded.ungradable:
        print(f"warning: {note}", file=sys.stderr)

    started_at = datetime.now(timezone.utc)
    clock_start = time.monotonic()
    try:
        embedder = OllamaEmbeddings(model=prepared.store.embedding_model, base_url=configuration.OLLAMA_BASE_URL)
        hits_by_row = rank_rows(prepared, retrieval="embedding", embedder=embedder)
    except (RuntimeError, ValueError) as error:
        print(f"error: eval failed — {error}", file=sys.stderr)
        print(
            f"hint: question embeddings need Ollama serving '{prepared.store.embedding_model}' "
            f"at {configuration.OLLAMA_BASE_URL}' (`ollama serve`)",
            file=sys.stderr,
        )
        return 1

    threshold = configuration.FALSE_RETRIEVAL_THRESHOLD
    card = score_rows(prepared.graded, hits_by_row, false_retrieval_threshold=threshold)
    run = build_run_facts(
        prepared,
        label=args.label,
        started_at_utc=started_at.isoformat(timespec="seconds"),
        elapsed_seconds=time.monotonic() - clock_start,
        false_retrieval_threshold=threshold,
    )
    results_path = configuration.EVAL_DIR / RESULTS_FILE
    append_results(results_path, render(run, card, heading=True))

    print(render(run, card, heading=False), end="")
    print(f"results : appended to {results_path}")
    return 0


def _benchmark_store_path(slug: str) -> Path:
    """Where a benchmark spec's build-store lives (sweeps never touch the baseline store)."""
    return configuration.BENCHMARK_STORES_DIR / f"{slug}.json"


def _run_benchmark(args: argparse.Namespace) -> int:
    """Step 3.5 (benchmark half): build the spec's stores once, grade each experiment.

    Store phase honors the grid: a source-backed store is used read-only (and
    validated against its spec); a build store is built when missing or stale
    and skipped when a matching store file exists. Experiments run in spec
    order through the shared grading path; a failed experiment is recorded and
    the run continues. Everything lands in results.md: one labeled block per
    experiment plus a comparison table for the whole run.
    """
    try:
        spec = parse_benchmark_toml(Path(args.config))
        selected = select_experiments(spec.experiments, only=args.only)
    except (BenchmarkSpecError, OSError) as error:
        print(f"error: benchmark spec failed — {error}", file=sys.stderr)
        return 1

    store_paths = {
        slug: (spec_store.source_path() if spec_store.is_source else _benchmark_store_path(slug))
        for slug, spec_store in spec.stores.items()
    }
    if args.dry_run:
        for line in describe_plan(spec, selected, {slug: str(path) for slug, path in store_paths.items()}):
            print(line)
        return 0

    if args.source:
        raw_dir = Path(args.source)
    else:
        try:
            raw_dir = configuration.RAW_DIR / configuration.instance_key(configuration.uwazi_url())
        except RuntimeError as error:
            print(f"error: benchmark needs the captures dir — {error}", file=sys.stderr)
            return 1

    results_path = configuration.EVAL_DIR / RESULTS_FILE
    golden_path = configuration.EVAL_DIR / GOLDEN_FILE
    store_costs: dict[str, float | None] = {}  # slug → build seconds (None = reused/up to date)
    store_errors: dict[str, str] = {}

    results: list[ExperimentResult] = []
    for experiment in selected:
        spec_store = spec.stores[experiment.store]
        path = store_paths[experiment.store]
        label = f"benchmark {spec.name}: {experiment.name}"
        started_at = datetime.now(timezone.utc)

        # Store phase (lazy, once per slug): validate reuse specs, build-or-skip build specs.
        if experiment.store not in store_costs and experiment.store not in store_errors:
            try:
                store_costs[experiment.store] = _make_benchmark_store_ready(
                    spec_store=spec_store, path=path, raw_dir=raw_dir
                )
            except (NaiveStoreMismatchError, EvalInputsError, RuntimeError, ValueError, OSError) as error:
                store_errors[experiment.store] = str(error).replace("\n", " ")[:240]

        if experiment.store in store_errors:
            message = store_errors[experiment.store]
            results.append(ExperimentResult(name=experiment.name, ok=False, error=message))
            print(f"failure : {experiment.name} — {message}", file=sys.stderr)
            append_results(results_path, f"## {started_at.isoformat(timespec='seconds')} — {label}\n\nFAILED: {message}\n")
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
            embedder = (
                OllamaEmbeddings(model=prepared.store.embedding_model, base_url=configuration.OLLAMA_BASE_URL)
                if experiment.retrieval in ("embedding", "rrf")
                else None
            )
            hits_by_row = rank_rows(prepared, retrieval=experiment.retrieval, embedder=embedder)
            card = score_rows(
                prepared.graded,
                hits_by_row,
                false_retrieval_threshold=(
                    configuration.FALSE_RETRIEVAL_THRESHOLD if experiment.retrieval == "embedding" else None
                ),
            )
        except (NaiveStoreMismatchError, EvalInputsError, RuntimeError, ValueError, OSError) as error:
            message = str(error).replace("\n", " ")[:240]
            elapsed = time.monotonic() - clock
            results.append(ExperimentResult(name=experiment.name, ok=False, run_seconds=elapsed, error=message))
            print(f"failure : {experiment.name} — {message}", file=sys.stderr)
            append_results(
                results_path,
                f"## {started_at.isoformat(timespec='seconds')} — {label}\n\nFAILED after {elapsed:.0f}s: {message}\n",
            )
            continue

        elapsed = time.monotonic() - clock
        run = build_run_facts(
            prepared,
            label=label,
            started_at_utc=started_at.isoformat(timespec="seconds"),
            elapsed_seconds=elapsed,
            false_retrieval_threshold=configuration.FALSE_RETRIEVAL_THRESHOLD,
        )
        block = render(run, card, heading=True)
        if experiment.retrieval != "embedding":
            block += (
                f"note: false-retrieval is cosine-specific — retrieval '{experiment.retrieval}' "
                "scores on a different scale, so comparison cells read —\n"
            )
        append_results(results_path, block)
        print(render(run, card, heading=False), end="")
        scope_all = card.scopes[0]
        results.append(
            ExperimentResult(
                name=experiment.name,
                ok=True,
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
                false_retrieval=(
                    f"{len(card.unanswerable.false_retrievals)}/{card.unanswerable.rows}"
                    if experiment.retrieval == "embedding"
                    else "—"
                ),
                build_seconds=store_costs.get(experiment.store),
                run_seconds=elapsed,
            )
        )

    heading = (
        f"## {datetime.now(timezone.utc).isoformat(timespec='seconds')} — benchmark {spec.name} — comparison "
        f"({len(results)} experiment{'s' if len(results) != 1 else ''})"
    )
    block = heading + "\n\n" + "\n".join(render_comparison(results)) + "\n"
    append_results(results_path, block)
    for line in block.splitlines():
        print(line)
    graded = sum(1 for result in results if result.ok)
    print(f"done    : {graded}/{len(results)} experiments graded — results appended to {results_path}")
    return 0 if graded == len(results) else 1


def _make_benchmark_store_ready(*, spec_store: StoreSpec, path: Path, raw_dir: Path) -> float | None:
    """Make ``path`` ready for grading per its spec; return build seconds (``None`` = reused).

    Source-backed stores are loaded and validated read-only (their file is
    never written — the committed baseline lives here). Build stores are
    skipped when a valid matching file exists and rebuilt otherwise (missing,
    corrupt, or stale-vs-spec). Failures raise; the caller records them and
    the run continues with the other experiments.
    """
    if spec_store.is_source:
        loaded = NaiveVectorStore.load(path)
        if not store_matches_spec(loaded, spec_store):
            raise EvalInputsError(
                f"source store {path} does not match its spec "
                f"(model {spec_store.model!r}, {spec_store.describe()}) — refusing to grade under it"
            )
        print(f"store   : {spec_store.slug} — reuse (read-only) {path}")
        return None
    try:
        loaded = NaiveVectorStore.load(path)
        valid = store_matches_spec(loaded, spec_store)
    except (NaiveStoreMismatchError, ValueError, OSError):
        valid = False
    if valid:
        print(f"store   : {spec_store.slug} — up to date ({path} matches the spec; build skipped)")
        return None
    print(
        f"store   : {spec_store.slug} — {path} is missing or stale → building "
        f"({spec_store.describe()}, model {spec_store.model})"
    )
    clock = time.monotonic()
    try:
        stats, _ = _build_naive_store(
            store_path=path,
            raw_dir=raw_dir,
            model=spec_store.model,
            declared_dimensions=None,
            probe=True,
            max_chars=spec_store.max_chars,
            overlap=spec_store.overlap,
            header=spec_store.header,
        )
    except (RuntimeError, ValueError, OSError) as error:
        raise EvalInputsError(f"building {path} failed — {error}") from error
    seconds = time.monotonic() - clock
    print(f"store   : {spec_store.slug} — built {stats.chunks_indexed:,} chunks in {seconds:.0f}s")
    return seconds


def _stub(name: str) -> int:
    print(f"error: '{name}' is a stub — implemented in a later step of PLAN.md", file=sys.stderr)
    return 2


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()
    if args.command == "hello":
        return _run_hello(args)
    if args.command == "fetch":
        return _run_fetch(args)
    if args.command == "chunk":
        return _run_chunk(args)
    if args.command == "build-index":
        return _run_build_index(args)
    if args.command == "search":
        return _run_search(args)
    if args.command == "build-golden":
        return _run_build_golden(args)
    if args.command == "show-group":
        return _run_show_group(args)
    if args.command == "eval":
        return _run_eval(args)
    if args.command == "benchmark":
        return _run_benchmark(args)
    # Everything else is a stub until its PLAN step is implemented.
    return _stub(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
