"""The SectionSplitChunker — the SectionChunker plus monster handling.

PLAN.md Step 4c wave 3.1's fourth arm (user call 2026-10-11, raced together
with the others). From the SectionChunker it differs in exactly ONE rule: a
single paragraph over the budget — always alone in its packing group, a
packing property, not a search — is word-split at word boundaries into
consecutive pieces that share ``overlap_ratio`` overlap (0.15, merge-style:
``overlap_ratio`` governs cuts INSIDE a paragraph, while packing boundaries
stay overlap-free). Every piece chunk repeats its section heading line on top,
the heading paragraph anchors its whole section (as in the SectionChunker), and
the monster's own paragraph anchors all its pieces — exactly like merge's
split paragraphs. Where the SectionChunker carries a monster whole (up to
~10.9k chars on maud), this method prices what splitting them buys.

On monster-free captures the two are byte-equal (asserted in tests), which is
why the arm is skipped on privacyqa: its largest paragraph is 1,064 chars, so
the variant has nothing to measure there. The monster question is decided on
maud (52.1% of its text mass exceeds 2400 chars) in wave 3.2.
"""

from __future__ import annotations

from typing import Any

from uwazi_rag.domain.chunk import Chunk
from uwazi_rag.use_cases.chunking import OVERLAP_RATIO, TARGET_MAX_CHARS
from uwazi_rag.use_cases.chunking_methods.base import ChunkMethod
from uwazi_rag.use_cases.index_captures import capture_to_chunks


class SectionSplitChunker(ChunkMethod):
    """Heading section + budget packing; over-long single paragraphs word-split (merge-style overlap)."""

    def __init__(self, *, max_chars: int = TARGET_MAX_CHARS, header: bool = True) -> None:
        """Validate eagerly (mirrors the merge chunker) so a bad instance fails at definition."""
        if max_chars < 1:
            raise ValueError(f"max_chars must be >= 1, got {max_chars}")
        self.max_chars = max_chars
        self.header = header

    @property
    def name(self) -> str:
        return "section-split"

    def params(self) -> dict[str, Any]:
        return {"max_chars": self.max_chars, "header": self.header}

    def chunk_config(self) -> dict[str, Any]:
        # overlap_ratio is FUNCTIONAL here: it sets the within-paragraph cut overlap
        # (merge-style) and the headingless fallback's merge overlap — same number, one rule.
        return {
            "target_max_chars": self.max_chars,
            "overlap_ratio": OVERLAP_RATIO,
            "prepend_header": self.header,
            "split_mode": "section-split",
        }

    def describe(self) -> str:
        return f"section-split {self.max_chars}/{'on' if self.header else 'off'}"

    def _chunk(self, capture: dict) -> list[Chunk]:
        return capture_to_chunks(capture, **self.chunk_config())
