from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from uwazi_api.client import UwaziClient
from uwazi_api.domain.exceptions import SegmentationNotFoundError

from uwazi_rag import configuration
from uwazi_rag.adapters.naive_vector_store import NaiveStoreMismatchError, NaiveVectorStore
from uwazi_rag.adapters.ollama_embeddings import OllamaEmbeddings
from uwazi_rag.use_cases.chunking import build_chunks
from uwazi_rag.use_cases.embed_probe import format_probe_report, run_embed_probe
from uwazi_rag.use_cases.fetch_document import (
    capture_entity,
    pages_covered,
    write_raw_capture,
)
from uwazi_rag.use_cases.index_captures import index_captures
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

    search = subparsers.add_parser(
        "search",
        help="embed the query, cosine-scan the naive store, print the top hits (Step 3; hybrid in Step 5)",
    )
    search.add_argument("query")
    search.add_argument("--top", type=int, default=5, help="how many hits to print (default 5)")
    search.add_argument("--store", default=None, help="naive store path (default: data/naive_store.json)")

    ask = subparsers.add_parser("ask", help="RAG answer with citations (Step 6)")
    ask.add_argument("question")

    for name in ("eval", "serve", "sync"):
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


def _run_build_index(args: argparse.Namespace) -> int:
    """Step 3: chunk + embed all captured docs of the configured instance, once."""
    try:
        url, _, _ = configuration.uwazi_credentials()
        store = NaiveVectorStore(
            dimensions=configuration.EMBEDDING_DIMENSIONS,
            embedding_model=configuration.EMBEDDING_MODEL,
        )
        raw_dir = Path(args.source) if args.source else configuration.RAW_DIR / configuration.instance_key(url)
        stats = index_captures(
            raw_dir=raw_dir,
            store=store,
            embedder=OllamaEmbeddings(),
            expected_dimensions=configuration.EMBEDDING_DIMENSIONS,
            batch_size=args.batch_size,
            limit=args.limit,
        )
        output = Path(args.output) if args.output else configuration.NAIVE_STORE_PATH
        store.save(output)
    except (ValueError, RuntimeError, OSError) as error:
        print(f"error: build-index failed — {error}", file=sys.stderr)
        print(
            f"hint: embedding needs Ollama serving '{configuration.EMBEDDING_MODEL}'"
            f" at {configuration.OLLAMA_BASE_URL}; captures come from `uwazi-rag fetch` / the seed script",
            file=sys.stderr,
        )
        return 1

    print(f"model   : {configuration.EMBEDDING_MODEL} ({configuration.EMBEDDING_DIMENSIONS} dims)")
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
    # Everything else is a stub until its PLAN step is implemented.
    return _stub(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
