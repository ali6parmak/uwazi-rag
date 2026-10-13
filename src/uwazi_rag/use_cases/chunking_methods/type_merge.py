"""The TypeMergeChunker — wave 3.4: merge, but runs break at content-type changes.

PLAN.md Step 4c wave 3.4 (user call 2026-10-13): MergeChunker's exact packing
arithmetic (budget, closure, 0.15-overlap monster cuts, header) plus ONE rule —
a packing run breaks when a keepable paragraph's content type changes;
``section header``/``title`` are glue, carrying the effective type of the body
run they preface (so header and title may go together, per the user's rule).
Uwazi-only by nature: the dataset homes are single-type ("text" everywhere)
corpora → byte-equal to merge there by construction (asserted in tests) — the
arm's home is the live Uwazi instance (footnotes, list items). The wave-3.3
``breadcrumb`` layer composes here (user call 2026-10-13): the race runs the
2×2 {merge, type-merge} × {plain, +breadcrumb}.
"""

from __future__ import annotations

from typing import Any

from uwazi_rag.domain.chunk import Chunk
from uwazi_rag.use_cases.chunking import OVERLAP_RATIO, TARGET_MAX_CHARS
from uwazi_rag.use_cases.chunking_methods.base import ChunkMethod
from uwazi_rag.use_cases.index_captures import capture_to_chunks


class TypeMergeChunker(ChunkMethod):
    """Type-run packing with merge's budget/overlap/closure arithmetic.

    ``breadcrumb`` (default OFF) swaps the header's template slot for the
    chunk's section heading line — recorded only when ON, like the merge
    chunker's rung-2 layers, so plain instances keep the legacy identity.
    """

    def __init__(
        self,
        *,
        max_chars: int = TARGET_MAX_CHARS,
        overlap: float = OVERLAP_RATIO,
        header: bool = True,
        breadcrumb: bool = False,
    ) -> None:
        """Validate eagerly (mirrors the merge chunker) so a bad instance fails at definition."""
        if max_chars < 1:
            raise ValueError(f"max_chars must be >= 1, got {max_chars}")
        if not 0.0 <= overlap < 0.5:
            raise ValueError(f"overlap must be in [0, 0.5), got {overlap}")
        if breadcrumb and not header:
            raise ValueError("breadcrumb needs header — the crumb IS the header's context slot")
        self.max_chars = max_chars
        self.overlap = overlap
        self.header = header
        self.breadcrumb = breadcrumb

    @property
    def name(self) -> str:
        return "type-merge"

    def params(self) -> dict[str, Any]:
        params: dict[str, Any] = {"max_chars": self.max_chars, "overlap": self.overlap, "header": self.header}
        if self.breadcrumb:
            params["layers"] = "crumb"  # slug-facing; the store record carries the granular key
        return params

    def chunk_config(self) -> dict[str, Any]:
        # overlap_ratio is FUNCTIONAL here (merge-style monster cuts) — recorded like merge's.
        config: dict[str, Any] = {
            "target_max_chars": self.max_chars,
            "overlap_ratio": self.overlap,
            "prepend_header": self.header,
            "split_mode": "type-merge",
        }
        if self.breadcrumb:
            config["breadcrumb"] = True
        return config

    def describe(self) -> str:
        return f"type-merge {self.max_chars}/{self.overlap:g}/{'on' if self.header else 'off'}" + (
            " +breadcrumb" if self.breadcrumb else ""
        )

    def _chunk(self, capture: dict) -> list[Chunk]:
        return capture_to_chunks(capture, **self.chunk_config())
