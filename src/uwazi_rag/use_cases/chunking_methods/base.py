"""The chunking-method ABC — minimal, after :mod:`uwazi_rag.ports.embedding_port`.

A chunk method chunks ONE raw capture; capture identity (instance_key/shared_id/
language/file_id/title/template) comes from the capture, settings come from the
constructor. The ABC enforces the mandatory provenance contract (every chunk
must carry its ``paragraph_ids``) in exactly one place.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from uwazi_rag.domain.chunk import Chunk


class ChunkMethod(ABC):
    """One chunking strategy; parameterize it by constructing instances.

    ``chunk()`` is the public face and is final: it checks the provenance
    contract the golden set depends on, then lets the implementation run.
    Instances also self-describe (``name``/``params()``/``describe()``) and
    declare the store's recorded ``chunk_config`` — the facts sweeps print.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """The strategy's name; instance settings live in ``params()``."""

    @abstractmethod
    def _chunk(self, capture: dict) -> list[Chunk]:
        """Chunk one raw capture (raw Uwazi paragraphs + identity fields)."""

    def chunk(self, capture: dict) -> list[Chunk]:
        """Chunk one capture, enforcing the ``paragraph_ids`` provenance contract."""
        chunks = self._chunk(capture)
        for produced in chunks:
            if not produced.paragraph_ids:
                raise ValueError(
                    f"chunk method {self.name!r} produced {produced.chunk_id} without paragraph_ids — "
                    "provenance is the eval contract (PLAN.md Step 3.5)"
                )
        return chunks

    def params(self) -> dict[str, Any]:
        """This instance's settings — JSON-safe primitives, part of store fingerprints."""
        return {}

    @abstractmethod
    def chunk_config(self) -> dict[str, Any]:
        """The build-style ``chunk_config`` stores record under this instance.

        Same shape the grading path re-chunks from — sweeps build stores with
        exactly this config, and the byte-verify guard proves the store obeys it.
        """

    def describe(self) -> str:
        """Compact settings string for results.md cells (e.g. ``merge 1200/0.15/on``)."""
        return self.name
