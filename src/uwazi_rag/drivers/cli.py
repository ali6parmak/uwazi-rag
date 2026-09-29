from __future__ import annotations

import argparse
import sys

from uwazi_rag import configuration
from uwazi_rag.adapters.ollama_embeddings import OllamaEmbeddings
from uwazi_rag.use_cases.embed_probe import format_probe_report, run_embed_probe


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

    index = subparsers.add_parser("index", help="index a template's published entities (Step 4)")
    index.add_argument("--template")
    index.add_argument("--all", action="store_true")

    search = subparsers.add_parser("search", help="search the index (semantic way in Step 3, hybrid in Step 5)")
    search.add_argument("query")

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


def _stub(name: str) -> int:
    print(f"error: '{name}' is a stub — implemented in a later step of PLAN.md", file=sys.stderr)
    return 2


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()
    if args.command == "hello":
        return _run_hello(args)
    # Everything else is a stub until its PLAN step is implemented.
    return _stub(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
