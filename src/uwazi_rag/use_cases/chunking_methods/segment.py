"""The SegmentChunker — one DLA segmentation segment per chunk (merge-off).

PLAN.md Step 4c wave 3.1's first method arm: the merge chunker packs adjacent
segments together because a segment alone can be too small to retrieve; this
method measures what the segmentation's OWN granule is worth. Race scope:
uwazi-only — the Uwazi home is the one corpus where segmentation segments are
paragraph-shaped; on the line-partitioned dataset captures this method
degenerates to line-per-chunk, so it never runs there.

Uwazi sections often arrive as ONE segment (the segmentation folds a whole
section into a single box), so an over-long segment still splits at word
boundaries ~2400 chars with overlap 0 (the pre-stated method budget, fixed —
unlike the merge chunker the budget never packs multiple segments together).

Implementation is deliberately thin: ``merge_off`` rides in
``build_chunks``/``capture_to_chunks`` as ``split_mode="segment"``, so the
science guard holds by construction — grading re-chunks through the recorded
config and byte-verifies the store against the very same call.
"""

from __future__ import annotations

from typing import Any

from uwazi_rag.domain.chunk import Chunk
from uwazi_rag.use_cases.chunking_methods.base import ChunkMethod
from uwazi_rag.use_cases.index_captures import capture_to_chunks

# The pre-stated over-long-segment word-split budget ("~2400", PLAN.md 4c).
SEGMENT_SPLIT_BUDGET = 2400


class SegmentChunker(ChunkMethod):
    """One segmentation segment = one chunk; over-long segments split, overlap 0."""

    def __init__(self, *, max_chars: int = SEGMENT_SPLIT_BUDGET, header: bool = True) -> None:
        """Validate eagerly (mirrors the chunker) so a bad instance fails at definition."""
        if max_chars < 1:
            raise ValueError(f"max_chars must be >= 1, got {max_chars}")
        self.max_chars = max_chars
        self.header = header

    @property
    def name(self) -> str:
        return "segment"

    def params(self) -> dict[str, Any]:
        return {"max_chars": self.max_chars, "header": self.header}

    def chunk_config(self) -> dict[str, Any]:
        # Overlap is method-fixed to 0 (no packing, no shared pieces) — recorded so the
        # graded config re-chunks byte-identically; ``split_mode`` drives the merge-off path.
        return {
            "target_max_chars": self.max_chars,
            "overlap_ratio": 0.0,
            "prepend_header": self.header,
            "split_mode": "segment",
        }

    def describe(self) -> str:
        return f"segment {self.max_chars}/{'on' if self.header else 'off'}"

    def _chunk(self, capture: dict) -> list[Chunk]:
        return capture_to_chunks(capture, **self.chunk_config())
