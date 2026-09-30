"""The naive vector store: in-memory numpy + JSON persistence (PLAN.md Step 3).

Holds ``(chunk, vector)`` pairs in memory; search is a plain cosine scan
against every vector, returning the top-k. Persists to one JSON file so the
dev loop never re-embeds. Kept forever — it becomes the offline
``VectorStore`` double once the pgvector port lands (Step 5), so its method
surface already follows the port design (upsert/delete/search-shaped).
"""

from __future__ import annotations

import json
from collections.abc import Sequence
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from uwazi_rag.domain.chunk import Chunk

STORE_SCHEMA = "naive_store_v1"


class NaiveStoreMismatchError(RuntimeError):
    """A persisted store does not match the configured embedding model."""


class NaiveVectorStore:
    """In-memory vectors plus chunk payloads, persistable as one JSON file.

    ``embedding_model`` and ``dimensions`` are recorded with the index and
    re-checked on load/search: vectors from two different embedding spaces
    must never be compared silently — cosine across models is meaningless.
    """

    def __init__(self, *, dimensions: int, embedding_model: str) -> None:
        if dimensions < 1:
            raise ValueError(f"dimensions must be >= 1, got {dimensions}")
        self.dimensions = dimensions
        self.embedding_model = embedding_model
        self.created_at_utc = datetime.now(timezone.utc).isoformat(timespec="seconds")
        self._vectors = np.zeros((0, dimensions), dtype=np.float64)
        self._chunks: list[Chunk] = []
        self._row_of: dict[str, int] = {}
        self._unit: np.ndarray | None = None  # L2-normalized cache of ``_vectors``

    def __len__(self) -> int:
        return len(self._chunks)

    def chunks(self) -> list[Chunk]:
        """Snapshot of the stored chunks, in insertion order."""
        return list(self._chunks)

    def upsert(self, chunks: Sequence[Chunk], vectors: Sequence[Sequence[float]]) -> None:
        """Insert or replace by ``chunk_id`` — re-indexing overwrites, never duplicates."""
        if len(chunks) != len(vectors):
            raise ValueError(f"{len(chunks)} chunks but {len(vectors)} vectors — counts must match")
        new_chunks: list[Chunk] = []
        new_rows: list[np.ndarray] = []
        for chunk, vector in zip(chunks, vectors):
            row = np.asarray(vector, dtype=np.float64)
            if row.shape != (self.dimensions,):
                raise ValueError(f"vector for {chunk.chunk_id} has shape {row.shape}, store expects ({self.dimensions},)")
            if chunk.chunk_id in self._row_of:
                target = self._row_of[chunk.chunk_id]
                self._vectors[target] = row
                self._chunks[target] = chunk
            else:
                new_chunks.append(chunk)
                new_rows.append(row)
        if new_chunks:
            existing = len(self._chunks)
            block = np.vstack(new_rows)
            self._vectors = np.vstack([self._vectors, block]) if existing else block
            for offset, chunk in enumerate(new_chunks):
                self._row_of[chunk.chunk_id] = existing + offset
            self._chunks.extend(new_chunks)
        self._unit = None

    def search(self, vector: Sequence[float], *, k: int = 5, instance_key: str | None = None) -> list[tuple[Chunk, float]]:
        """Cosine similarity scan, best-first, at most ``k`` hits.

        ``instance_key`` optionally narrows the scan to one instance's
        chunks (the store can hold several once Step 4 reuses it).
        """
        if k < 1:
            raise ValueError(f"k must be >= 1, got {k}")
        query = np.asarray(vector, dtype=np.float64)
        if query.shape != (self.dimensions,):
            raise ValueError(f"query vector has shape {query.shape}, store expects ({self.dimensions},)")
        rows = list(range(len(self._chunks)))
        if instance_key is not None:
            rows = [index for index, chunk in enumerate(self._chunks) if chunk.instance_key == instance_key]
            if not rows:
                return []
        unit = self._unit_rows()[rows]
        query_norm = float(np.linalg.norm(query))
        if query_norm == 0.0:
            sims = np.zeros(len(rows), dtype=np.float64)
        else:
            sims = unit @ (query / query_norm)
        order = np.argsort(-sims)[:k]
        return [(self._chunks[rows[int(index)]], float(sims[index])) for index in order]

    def _unit_rows(self) -> np.ndarray:
        if self._unit is None:
            norms = np.linalg.norm(self._vectors, axis=1, keepdims=True)
            norms[norms == 0.0] = 1.0  # zero vectors get similarity 0, not NaN
            self._unit = self._vectors / norms
        return self._unit

    def save(self, path: Path) -> None:
        """Persist everything to one JSON file (atomic rename) so dev never re-embeds."""
        payload = {
            "schema": STORE_SCHEMA,
            "embedding_model": self.embedding_model,
            "dimensions": self.dimensions,
            "created_at_utc": self.created_at_utc,
            "entries": [
                {"chunk": chunk.model_dump(mode="json"), "vector": self._vectors[index].tolist()}
                for index, chunk in enumerate(self._chunks)
            ],
        }
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(path.suffix + ".tmp")
        tmp.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        tmp.replace(path)

    @classmethod
    def load(
        cls,
        path: Path,
        *,
        embedding_model: str | None = None,
        dimensions: int | None = None,
    ) -> NaiveVectorStore:
        """Load a persisted store, optionally guarding model + dimensions."""
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict) or data.get("schema") != STORE_SCHEMA:
            raise NaiveStoreMismatchError(f"{path} is not a '{STORE_SCHEMA}' naive store.")
        model = str(data.get("embedding_model", ""))
        dims = int(data.get("dimensions", 0))
        if embedding_model is not None and model != embedding_model:
            raise NaiveStoreMismatchError(
                f"{path} was indexed with '{model}', config expects '{embedding_model}' — "
                "rebuild with `uwazi-rag build-index`."
            )
        if dimensions is not None and dims != dimensions:
            raise NaiveStoreMismatchError(
                f"{path} was indexed with {dims} dims, config expects {dimensions} — rebuild with `uwazi-rag build-index`."
            )
        store = cls(dimensions=dims, embedding_model=model)
        created = data.get("created_at_utc")
        if created:
            store.created_at_utc = str(created)
        entries = data.get("entries", [])
        store.upsert(
            [Chunk.model_validate(entry["chunk"]) for entry in entries],
            [entry["vector"] for entry in entries],
        )
        return store
