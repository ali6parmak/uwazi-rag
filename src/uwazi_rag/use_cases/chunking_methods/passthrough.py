"""The pass-through chunk method — fixed corpora that arrive pre-chunked.

vic-chargebook (PLAN.md Step 4a) ships its passages already chunked (≤512
tokens upstream); re-chunking would grade upstream's choices, not ours. A
pass-through method makes the corpus's OWN granule the chunk: one keepable
capture paragraph → one chunk, no merging, no splitting, header optional.

The provenance contract is unchanged (the ABC enforces ``paragraph_ids``; each
chunk carries exactly its one paragraph) and the ``chunk_config`` stays a
``build_chunks``-shaped config, so grading's byte-verify guard works as-is:
on single-paragraph captures this method is byte-equal to
``capture_to_chunks`` under its own config (asserted in tests) — the science
guard that keeps a sweep's numbers and an ``eval`` run's numbers the same. A
fixed corpus with multi-paragraph captures would diverge from the merge
chunker, and the byte-verify would then abort loudly — exactly the honest
failure wanted if such a corpus is ever graded.
"""

from __future__ import annotations

from typing import Any

from uwazi_rag.domain.chunk import Chunk
from uwazi_rag.use_cases.chunking import _header, keepable
from uwazi_rag.use_cases.chunking_methods.base import ChunkMethod

# Ceiling above the fixed corpora's longest unit (vic-chargebook's longest
# passage is 2,715 chars): no pass-through chunk is split, and the graders'
# byte-verify aborts loudly if an upstream unit ever exceeds it.
PASS_THROUGH_MAX_CHARS = 4096


class PassThroughChunker(ChunkMethod):
    """One capture paragraph = one chunk, verbatim — no merge, no split."""

    def __init__(self, *, max_chars: int = PASS_THROUGH_MAX_CHARS, header: bool = True) -> None:
        """Validate eagerly (mirrors the merge chunker) so a bad instance fails at definition."""
        if max_chars < 1:
            raise ValueError(f"max_chars must be >= 1, got {max_chars}")
        self.max_chars = max_chars
        self.header = header

    @property
    def name(self) -> str:
        return "passthrough"

    def params(self) -> dict[str, Any]:
        return {"max_chars": self.max_chars, "header": self.header}

    def chunk_config(self) -> dict[str, Any]:
        # Overlap is meaningless without splitting; recorded 0.0 so the graded
        # config re-chunks (single-paragraph captures) byte-identically.
        return {"target_max_chars": self.max_chars, "overlap_ratio": 0.0, "prepend_header": self.header}

    def describe(self) -> str:
        return f"passthrough {self.max_chars}/{'on' if self.header else 'off'}"

    def _chunk(self, capture: dict) -> list[Chunk]:
        if not capture.get("paragraphs"):
            return []
        instance_key = str(capture["instance_key"])
        shared_id = str(capture["shared_id"])
        language = str(capture["language"])
        file_id = str(capture["file"]["id"])
        title = str(capture["title"])
        template_name = str(capture["template"]["name"])
        chunks: list[Chunk] = []
        for index, paragraph in enumerate(capture.get("paragraphs", [])):
            if not keepable(paragraph):
                continue
            body = str(paragraph["text"]).strip()
            page: int | None = paragraph.get("pageNumber")
            text = f"{_header(title, template_name, page)}\n{body}" if self.header else body
            chunks.append(
                Chunk(
                    chunk_id=f"{instance_key}:{shared_id}:{language}:{file_id}:{index:04d}",
                    instance_key=instance_key,
                    shared_id=shared_id,
                    language=language,
                    file_id=file_id,
                    chunk_index=len(chunks),
                    text=text,
                    page_start=page,
                    page_end=page,
                    paragraph_ids=[index],
                )
            )
        return chunks
