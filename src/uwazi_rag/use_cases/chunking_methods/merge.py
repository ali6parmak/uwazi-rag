"""The merge chunker as a method instance — the one chunker PLAN.md settled on.

``MergeChunker`` is a thin settings-carrying wrapper over
:func:`uwazi_rag.use_cases.index_captures.capture_to_chunks`, which is the
shared entry into :func:`uwazi_rag.use_cases.chunking.build_chunks` — there is
still exactly one chunker; instances only hold its parameters. The science
guard leans on this equality: grading re-chunks via the store's recorded
config and byte-verifies the store, so a ``MergeChunker`` and the shared
chunker can never quietly diverge.
"""

from __future__ import annotations

from typing import Any

from uwazi_rag.domain.chunk import Chunk
from uwazi_rag.use_cases.chunking import OVERLAP_RATIO, TARGET_MAX_CHARS
from uwazi_rag.use_cases.chunking_methods.base import ChunkMethod
from uwazi_rag.use_cases.index_captures import capture_to_chunks


class MergeChunker(ChunkMethod):
    """Merge adjacent segmentation paragraphs into retrieval-sized chunks.

    Settings are constructor params (the Step 2 constants are the defaults):
    ``max_chars`` closes a chunk just before the budget, ``overlap`` is the
    fraction long split paragraphs share, ``header`` prepends the
    ``"{title} — {template} (page n)"`` context line.
    """

    def __init__(self, *, max_chars: int = TARGET_MAX_CHARS, overlap: float = OVERLAP_RATIO, header: bool = True) -> None:
        """Validate eagerly (mirrors the chunker) so a bad instance fails at definition."""
        if max_chars < 1:
            raise ValueError(f"max_chars must be >= 1, got {max_chars}")
        if not 0.0 <= overlap < 0.5:
            raise ValueError(f"overlap must be in [0, 0.5), got {overlap}")
        self.max_chars = max_chars
        self.overlap = overlap
        self.header = header

    @property
    def name(self) -> str:
        return "merge"

    def params(self) -> dict[str, Any]:
        return {"max_chars": self.max_chars, "overlap": self.overlap, "header": self.header}

    def chunk_config(self) -> dict[str, Any]:
        return {"target_max_chars": self.max_chars, "overlap_ratio": self.overlap, "prepend_header": self.header}

    def describe(self) -> str:
        return f"merge {self.max_chars}/{self.overlap:g}/{'on' if self.header else 'off'}"

    def _chunk(self, capture: dict) -> list[Chunk]:
        return capture_to_chunks(capture, **self.chunk_config())
