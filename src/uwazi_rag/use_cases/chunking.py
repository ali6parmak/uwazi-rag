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
``prepend_header``) exist so ``build-index`` can sweep them; the module
constants stay the Step 2 defaults everything else inherits.
"""

from __future__ import annotations

from uwazi_rag.domain.chunk import Chunk

TARGET_MIN_CHARS = 1200
TARGET_MAX_CHARS = 1800
OVERLAP_RATIO = 0.15
# Repeat-on-every-page boilerplate plus anything without text: never chunks.
DROP_TYPES = {"page header", "page footer"}


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
) -> list[Chunk]:
    """Merge raw segmentation paragraphs (Uwazi field names) into ``Chunk``s.

    Deterministic: the same input always produces the same chunk list, and
    ``chunk_id`` is derived from the chunk identity tuple + zero-padded index.
    ``target_max_chars``/``overlap_ratio``/``prepend_header`` are the eval
    sweep's knobs (Step 3.5); defaults are the Step 2 constants, so existing
    call sites keep today's chunking and chunk identity never moves.
    """
    if target_max_chars < 1:
        raise ValueError(f"target_max_chars must be >= 1, got {target_max_chars}")
    if not 0.0 <= overlap_ratio < 0.5:
        raise ValueError(f"overlap_ratio must be in [0, 0.5), got {overlap_ratio}")
    overlap_chars = int(target_max_chars * overlap_ratio)

    # (text piece, page, raw paragraph position) — the position anchors the
    # chunk back to paragraph_ids even where dropped paragraphs leave gaps.
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
        index = len(chunks)
        body = "\n".join(piece for piece, _, _ in buffer)
        pages = [page for _, page, _ in buffer if page is not None]
        seen: set[int] = set()
        paragraph_ids: list[int] = []
        for _, _, pid in buffer:
            if pid not in seen:
                seen.add(pid)
                paragraph_ids.append(pid)
        text = f"{_header(entity_title, template_name, pages[0] if pages else None)}\n{body}" if prepend_header else body
        chunks.append(
            Chunk(
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
        )
        buffer.clear()

    for piece, page, pid in parts:
        joined = len("\n".join(piece_text for piece_text, _, _ in buffer))
        if buffer and joined + 1 + len(piece) > target_max_chars:
            flush()
        buffer.append((piece, page, pid))
    flush()
    return chunks
