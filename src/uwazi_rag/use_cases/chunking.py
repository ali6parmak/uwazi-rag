"""Step 2: merge segmentation paragraphs into retrieval-sized chunks.

Starting rules (PLAN.md Step 2 — later tuned ONLY through the eval harness):

- drop page furniture (``Page header``/``Page footer``) and empty layout boxes
  (pictures, empty text) — they repeat every page or carry no text
- merge adjacent paragraphs; close a chunk just before pushing past
  ~``TARGET_MAX_CHARS``
- split single paragraphs longer than ``TARGET_MAX_CHARS`` into pieces that
  share ~15% overlap, breaking at a word boundary when one is near
- prepend a context header ``"{title} — {template} (page {n})"`` so a chunk
  retrieved alone still says who/what it is about
- record the page range from the merged paragraphs' ``pageNumber``
- record each chunk's ``paragraph_ids`` — the raw capture positions it
  covers, so the eval scorecard can map paragraph anchors to chunk ids
  under any build configuration (PLAN.md Step 3.5)

Pure function — no network, no store; runs offline against real captures.
The build parameters (``target_max_chars``, ``overlap_ratio``,
``prepend_header``, ``split_mode``) exist so ``build-index`` and the eval
sweeps can drive them; the module constants stay the Step 2 defaults
everything else inherits, and ``split_mode="merge"`` is byte-identical to
every store built before Step 4c (back-compat contract of the Wave 3.1
method race).

Split modes (Step 4c wave 3.1 — the method axis, never a knob flip):

- ``"merge"`` — merge adjacent paragraphs; close a chunk just before the
  budget; over-long paragraphs word-split with shared overlap (Step 2).
- ``"segment"`` — one segmentation segment per chunk; over-long segments
  word-split with NO overlap (the SegmentChunker's merge-off mode).
- ``"section"`` — heading partition (typed Uwazi heading types first, regex
  on typeless lines), interior spans packed at the budget at paragraph
  boundaries, over-long paragraphs stay whole; a document with no heading
  falls back to the merge path byte-equal (the SectionChunker's graceful
  fallback).
"""

from __future__ import annotations

from uwazi_rag.domain.chunk import Chunk

TARGET_MIN_CHARS = 1200
TARGET_MAX_CHARS = 1800
OVERLAP_RATIO = 0.15
# Repeat-on-every-page boilerplate plus anything without text: never chunks.
DROP_TYPES = {"page header", "page footer"}
# The chunking-method axis (PLAN.md Step 4c wave 3.1): recorded in store
# ``chunk_config`` as ``split_mode`` and re-driven by grading. "merge" is the
# default so legacy stores re-chunk byte-identically without the key.
SPLIT_MODES = ("merge", "segment", "section")


def keepable(paragraph: dict) -> bool:
    """True when a raw Uwazi paragraph can carry content (Step 2 drop rule).

    Public because the golden dataset must anchor passages to the exact
    paragraphs the chunker uses — one rule, two consumers, no drift.
    """
    text = paragraph.get("text")
    if not text or not text.strip():
        return False
    return (paragraph.get("type") or "").strip().lower() not in DROP_TYPES


def _split_long(text: str, target_max_chars: int = TARGET_MAX_CHARS, overlap_chars: int | None = None) -> list[str]:
    """Split one over-long paragraph into pieces <= target_max_chars.

    Cuts at the last whitespace of the window when possible; consecutive
    pieces overlap by ~overlap_chars so a sentence cut in half stays findable.
    """
    if overlap_chars is None:
        overlap_chars = int(target_max_chars * OVERLAP_RATIO)
    if len(text) <= target_max_chars:
        return [text]
    pieces: list[str] = []
    start = 0
    while True:
        window = text[start : start + target_max_chars]
        if start + target_max_chars >= len(text):
            pieces.append(text[start:])
            return pieces
        boundary = window.rfind(" ", int(target_max_chars * 0.8))
        cut = boundary if boundary > 0 else target_max_chars
        pieces.append(text[start : start + cut])
        start += cut - overlap_chars


def _header(entity_title: str, template_name: str, page_start: int | None) -> str:
    subject = entity_title or "Untitled"
    source = f"{subject} — {template_name}" if template_name else subject
    return f"{source} (page {page_start})" if page_start is not None else source


def _emit_chunk(
    *,
    body_parts: list[tuple[str, int | None, int]],
    instance_key: str,
    shared_id: str,
    language: str,
    file_id: str,
    entity_title: str,
    template_name: str,
    prepend_header: bool,
    index: int,
) -> Chunk:
    """Assemble one ``Chunk`` from ``(piece, page, paragraph position)`` parts — the merge flush's exact construction."""
    body = "\n".join(piece for piece, _, _ in body_parts)
    pages = [page for _, page, _ in body_parts if page is not None]
    seen: set[int] = set()
    paragraph_ids: list[int] = []
    for _, _, pid in body_parts:
        if pid not in seen:
            seen.add(pid)
            paragraph_ids.append(pid)
    text = f"{_header(entity_title, template_name, pages[0] if pages else None)}\n{body}" if prepend_header else body
    return Chunk(
        chunk_id=f"{instance_key}:{shared_id}:{language}:{file_id}:{index:04d}",
        instance_key=instance_key,
        shared_id=shared_id,
        language=language,
        file_id=file_id,
        chunk_index=index,
        text=text,
        page_start=min(pages) if pages else None,
        page_end=max(pages) if pages else None,
        paragraph_ids=paragraph_ids,
    )


def build_chunks(
    paragraphs: list[dict],
    *,
    instance_key: str,
    shared_id: str,
    language: str,
    file_id: str,
    entity_title: str,
    template_name: str,
    target_max_chars: int = TARGET_MAX_CHARS,
    overlap_ratio: float = OVERLAP_RATIO,
    prepend_header: bool = True,
    split_mode: str = "merge",
) -> list[Chunk]:
    """Merge raw segmentation paragraphs (Uwazi field names) into ``Chunk``s.

    Deterministic: the same input always produces the same chunk list, and
    ``chunk_id`` is derived from the chunk identity tuple + zero-padded index.
    ``target_max_chars``/``overlap_ratio``/``prepend_header``/``split_mode``
    are the eval sweep's knobs (Step 3.5, Step 4c wave 3.1); defaults are the
    Step 2 constants and the merge mode, so existing call sites keep today's
    chunking, chunk identity never moves, and every store built before 4c
    byte-verifies unchanged.
    """
    if target_max_chars < 1:
        raise ValueError(f"target_max_chars must be >= 1, got {target_max_chars}")
    if not 0.0 <= overlap_ratio < 0.5:
        raise ValueError(f"overlap_ratio must be in [0, 0.5), got {overlap_ratio}")
    if split_mode not in SPLIT_MODES:
        raise ValueError(f"split_mode must be one of {', '.join(SPLIT_MODES)}, got {split_mode!r}")
    overlap_chars = int(target_max_chars * overlap_ratio)

    if split_mode == "segment":
        # Merge-off: one segmentation segment per chunk; an over-long segment splits at word
        # boundaries with NO overlap (each piece is its own chunk).
        segment_chunks: list[Chunk] = []
        for index, paragraph in enumerate(paragraphs):
            if not keepable(paragraph):
                continue
            page = paragraph.get("pageNumber")
            text = str(paragraph["text"]).strip()
            for piece in _split_long(text, target_max_chars, 0):
                segment_chunks.append(
                    _emit_chunk(
                        body_parts=[(piece, page, index)],
                        instance_key=instance_key,
                        shared_id=shared_id,
                        language=language,
                        file_id=file_id,
                        entity_title=entity_title,
                        template_name=template_name,
                        prepend_header=prepend_header,
                        index=len(segment_chunks),
                    )
                )
        return segment_chunks

    if split_mode == "section":
        # Lazy import: headings.py holds keepable's second consumer (the detector), so the
        # detector cannot be a top-level import here without a cycle.
        from uwazi_rag.use_cases.headings import is_heading, pack_sections, partition_sections

        if not any(keepable(paragraph) and is_heading(paragraph) for paragraph in paragraphs):
            # Graceful fallback: a headingless document chunks exactly like merge —
            # byte-equal by construction (verified in tests).
            return build_chunks(
                paragraphs,
                instance_key=instance_key,
                shared_id=shared_id,
                language=language,
                file_id=file_id,
                entity_title=entity_title,
                template_name=template_name,
                target_max_chars=target_max_chars,
                overlap_ratio=overlap_ratio,
                prepend_header=prepend_header,
                split_mode="merge",
            )
        groups = pack_sections(partition_sections(paragraphs), paragraphs, target_max_chars)
        section_chunks: list[Chunk] = []
        for group in groups:
            body_parts = [(str(paragraphs[pid]["text"]).strip(), paragraphs[pid].get("pageNumber"), pid) for pid in group]
            section_chunks.append(
                _emit_chunk(
                    body_parts=body_parts,
                    instance_key=instance_key,
                    shared_id=shared_id,
                    language=language,
                    file_id=file_id,
                    entity_title=entity_title,
                    template_name=template_name,
                    prepend_header=prepend_header,
                    index=len(section_chunks),
                )
            )
        return section_chunks

    # (text piece, page, raw paragraph position) — the position anchors the
    # chunk back to paragraph_ids even where dropped paragraphs leave gaps.
    # Merge mode only (below): the segment/section modes returned earlier.
    parts: list[tuple[str, int | None, int]] = []
    for index, paragraph in enumerate(paragraphs):
        if not keepable(paragraph):
            continue
        page = paragraph.get("pageNumber")
        for piece in _split_long(str(paragraph["text"]).strip(), target_max_chars, overlap_chars):
            parts.append((piece, page, index))

    chunks: list[Chunk] = []
    buffer: list[tuple[str, int | None, int]] = []

    def flush() -> None:
        if not buffer:
            return
        chunks.append(
            _emit_chunk(
                body_parts=list(buffer),
                instance_key=instance_key,
                shared_id=shared_id,
                language=language,
                file_id=file_id,
                entity_title=entity_title,
                template_name=template_name,
                prepend_header=prepend_header,
                index=len(chunks),
            )
        )
        buffer.clear()

    for piece, page, pid in parts:
        joined = len("\n".join(piece_text for piece_text, _, _ in buffer))
        if buffer and joined + 1 + len(piece) > target_max_chars:
            flush()
        buffer.append((piece, page, pid))
    flush()
    return chunks
