"""Step 3: build a naive search index from the captured corpus in ``data/raw``.

Walks every capture of one instance, reuses the Step 2 chunk builder,
embeds through :class:`~uwazi_rag.ports.embedding_port.EmbeddingPort` in
batches and fills a store. Pure orchestration between two ports — unit
tests run offline on the committed fixtures with a deterministic embedder
(AGENTS.md testing policy).
"""

from __future__ import annotations

import json
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from loguru import logger

from uwazi_rag.domain.chunk import Chunk
from uwazi_rag.ports.embedding_port import EmbeddingPort
from uwazi_rag.use_cases.chunking import build_chunks


class ChunkVectorStore(Protocol):
    """The store surface Step 3 needs; Step 5 formalizes it as ``VectorStore``."""

    def upsert(self, chunks: Sequence[Chunk], vectors: Sequence[Sequence[float]]) -> None: ...

    def __len__(self) -> int: ...


@dataclass
class IndexStats:
    """What one ``index_captures`` run did (for the CLI's progress report)."""

    captures_seen: int
    captures_indexed: int
    skipped_not_ready: int
    skipped_no_chunks: int
    chunks_indexed: int


def load_captures(raw_dir: Path) -> list[dict]:
    """Parse every ``<sharedId>_<lang>.json`` capture under one instance's raw dir.

    Sorted by filename so runs are deterministic and progress logs are stable.
    Raises ``FileNotFoundError`` with a next action when nothing was captured yet.
    """
    if not raw_dir.is_dir():
        raise FileNotFoundError(
            f"no captures dir at {raw_dir} — run `uwazi-rag fetch <sharedId>` (or the seed script) first"
        )
    return [json.loads(path.read_text(encoding="utf-8")) for path in sorted(raw_dir.glob("*.json"))]


def capture_to_chunks(capture: dict) -> list[Chunk]:
    """One raw capture → ``Chunk``s (exactly the ``chunk`` command's logic)."""
    return build_chunks(
        capture["paragraphs"],
        instance_key=capture["instance_key"],
        shared_id=capture["shared_id"],
        language=capture["language"],
        file_id=capture["file"]["id"],
        entity_title=capture["title"],
        template_name=capture["template"]["name"],
    )


def index_captures(
    *,
    raw_dir: Path,
    store: ChunkVectorStore,
    embedder: EmbeddingPort,
    expected_dimensions: int,
    batch_size: int = 32,
    limit: int | None = None,
) -> IndexStats:
    """Chunk + embed every capture under ``raw_dir`` into ``store``.

    Idempotent: chunk identity is deterministic and ``upsert`` overwrites by
    ``chunk_id``. Captures whose segmentation is not ``ready`` (or that yield
    no keepable text) are skipped and counted, never fatal — Step 4's
    resilience rule, rehearsed early. Embeds in ``batch_size`` batches so one
    ``POST /api/embed`` stays reasonably sized and progress is visible.
    """
    if batch_size < 1:
        raise ValueError(f"batch_size must be >= 1, got {batch_size}")
    if limit is not None and limit < 1:
        raise ValueError(f"limit must be >= 1, got {limit}")
    captures = load_captures(raw_dir)
    if limit is not None:
        captures = captures[:limit]

    captures_indexed = 0
    skipped_not_ready = 0
    skipped_no_chunks = 0
    selected: list[Chunk] = []
    for capture in captures:
        if capture["segmentation_status"] != "ready":
            skipped_not_ready += 1
            logger.warning(
                f"skipping {capture['shared_id']} ({capture['language']}): "
                f"segmentation status '{capture['segmentation_status']}' is not 'ready'"
            )
            continue
        capture_chunks = capture_to_chunks(capture)
        if not capture_chunks:
            skipped_no_chunks += 1
            logger.warning(f"skipping {capture['shared_id']} ({capture['language']}): no keepable text")
            continue
        selected.extend(capture_chunks)
        captures_indexed += 1

    embedded = 0
    for start in range(0, len(selected), batch_size):
        batch = selected[start : start + batch_size]
        vectors = embedder.embed([chunk.text for chunk in batch])
        if len(vectors) != len(batch):
            raise RuntimeError(f"embedder returned {len(vectors)} vectors for a batch of {len(batch)} texts")
        if len(vectors[0]) != expected_dimensions:
            raise RuntimeError(
                f"embedder returned {len(vectors[0])} dims but {expected_dimensions} are configured — "
                "check EMBEDDING_MODEL / EMBEDDING_DIMENSIONS against the model card (`uwazi-rag hello`)"
            )
        store.upsert(batch, vectors)
        embedded += len(batch)
        logger.info(f"embedded {embedded}/{total_or(selected)} chunks")

    return IndexStats(
        captures_seen=len(captures),
        captures_indexed=captures_indexed,
        skipped_not_ready=skipped_not_ready,
        skipped_no_chunks=skipped_no_chunks,
        chunks_indexed=len(selected),
    )


def total_or(selected: list[Chunk]) -> int:
    """Total chunk count for progress messages (0 → 0 so ``/0`` never divides)."""
    return len(selected)
