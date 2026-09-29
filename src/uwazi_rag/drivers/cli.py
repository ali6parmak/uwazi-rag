from __future__ import annotations

import argparse
import sys

from uwazi_api.client import UwaziClient
from uwazi_api.domain.exceptions import SegmentationNotFoundError

from uwazi_rag import configuration
from uwazi_rag.adapters.ollama_embeddings import OllamaEmbeddings
from uwazi_rag.use_cases.embed_probe import format_probe_report, run_embed_probe
from uwazi_rag.use_cases.fetch_document import (
    pages_covered,
    raw_capture_json,
    segmentation_paragraphs,
    write_raw_capture,
)


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


def _run_fetch(args: argparse.Namespace) -> int:
    url, user, password = configuration.uwazi_credentials()
    client = UwaziClient(url=url, user=user, password=password)
    try:
        entity = client.entities.get_one(args.shared_id, args.language)
        segmentation = client.files.get_segmentation(args.shared_id, args.language)
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

    template = client.templates.get_by_id(entity.template) if entity.template else None
    document = next((d for d in entity.documents if d.id == segmentation.file_id), None)
    capture = raw_capture_json(
        shared_id=entity.shared_id or args.shared_id,
        language=args.language,
        instance_key=configuration.instance_key(url),
        title=entity.title or "",
        template_id=entity.template,
        template_name=template.name if template else "",
        file_id=segmentation.file_id,
        file_name=getattr(document, "originalname", None),
        segmentation_status=segmentation.status,
        paragraphs=segmentation_paragraphs(segmentation),
    )
    targets = write_raw_capture(capture, instance_key=configuration.instance_key(url), raw_dir=configuration.RAW_DIR)

    pages = pages_covered(capture["paragraphs"])
    print(f"entity : {capture['shared_id']} ({capture['language']}) — {capture['title']}")
    print(f"file   : {capture['file']['name']} ({capture['file']['id']})")
    print(
        f"paras  : {len(capture['paragraphs'])} — status '{segmentation.status}'"
        + (f", pages {pages[0]}..{pages[1]}" if pages else "")
    )
    for target in targets:
        print(f"wrote  : {target}")
    if segmentation.status != "ready":
        print(f"warning: segmentation status is '{segmentation.status}', not 'ready'", file=sys.stderr)
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
    if args.command == "fetch":
        return _run_fetch(args)
    # Everything else is a stub until its PLAN step is implemented.
    return _stub(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
