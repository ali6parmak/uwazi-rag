"""The SectionChunker — one section per chunk, at heading boundaries.

PLAN.md Step 4c wave 3.1's second method arm (go/no-go measured by the wave-3.0
scan: 98.0% of contract docs carry headings — the arm is KEPT). The partition
is one rule, two consumers: the wave-3.0 scan and this class both call
:mod:`uwazi_rag.use_cases.headings`' detector/partition/packer verbatim —
packed interior spans at the SAME per-dataset budget as the merge competitor
(``max_chars``), over-cap sections split at paragraph boundaries with overlap
0, an over-long single paragraph staying whole, header on by default.

A split section's CONTINUATION chunks repeat the section's heading line at the
top of their text (user call 2026-10-11): a chunk retrieved alone still names
its section, the heading paragraph anchors its whole section through
``paragraph_ids``, and the repeated line is a text-assembly layer — added
after packing, NOT counted against the budget, so the wave-3.0 scan's
section/partition counts stay exact.

A document with no heading falls back to the merge path BYTE-EQUAL (verified
in tests) — the graceful fallback PLAN.md pre-states, so headingless corpora
(or a doc with none) measure merge, not a degenerate one-chunk-monolith. The
fallback is why ``chunk_config`` records the merge overlap: a headingless doc
re-chunks exactly like ``MergeChunker(max_chars=...)`` under the same config.
"""

from __future__ import annotations

from typing import Any

from uwazi_rag.domain.chunk import Chunk
from uwazi_rag.use_cases.chunking import OVERLAP_RATIO, TARGET_MAX_CHARS
from uwazi_rag.use_cases.chunking_methods.base import ChunkMethod
from uwazi_rag.use_cases.index_captures import capture_to_chunks


class SectionChunker(ChunkMethod):
    """Heading partition → budget-packed sections; headingless docs merge byte-equal."""

    def __init__(self, *, max_chars: int = TARGET_MAX_CHARS, header: bool = True) -> None:
        """Validate eagerly (mirrors the merge chunker) so a bad instance fails at definition."""
        if max_chars < 1:
            raise ValueError(f"max_chars must be >= 1, got {max_chars}")
        self.max_chars = max_chars
        self.header = header

    @property
    def name(self) -> str:
        return "section"

    def params(self) -> dict[str, Any]:
        return {"max_chars": self.max_chars, "header": self.header}

    def chunk_config(self) -> dict[str, Any]:
        # Overlap rides along ONLY for the headingless fallback (a section chunk never
        # word-splits; packing is paragraph-boundary, overlap 0 by method definition).
        return {
            "target_max_chars": self.max_chars,
            "overlap_ratio": OVERLAP_RATIO,
            "prepend_header": self.header,
            "split_mode": "section",
        }

    def describe(self) -> str:
        return f"section {self.max_chars}/{'on' if self.header else 'off'}"

    def _chunk(self, capture: dict) -> list[Chunk]:
        return capture_to_chunks(capture, **self.chunk_config())
