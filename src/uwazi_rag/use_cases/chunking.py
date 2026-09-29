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

Pure function — no network, no store; runs offline against real captures.
"""

from __future__ import annotations

from uwazi_rag.domain.chunk import Chunk

TARGET_MIN_CHARS = 1200
TARGET_MAX_CHARS = 1800
OVERLAP_RATIO = 0.15
# Repeat-on-every-page boilerplate plus anything without text: never chunks.
DROP_TYPES = {"page header", "page footer"}


def _keepable(paragraph: dict) -> bool:
    text = paragraph.get("text")
    if not text or not text.strip():
        return False
    return (paragraph.get("type") or "").strip().lower() not in DROP_TYPES


def _split_long(text: str) -> list[str]:
    """Split one over-long paragraph into pieces <= TARGET_MAX_CHARS.

    Cuts at the last whitespace of the window when possible; consecutive
    pieces overlap by ~OVERLAP_RATIO so a sentence cut in half stays findable.
    """
    if len(text) <= TARGET_MAX_CHARS:
        return [text]
    overlap_chars = int(TARGET_MAX_CHARS * OVERLAP_RATIO)
    pieces: list[str] = []
    start = 0
    while True:
        window = text[start : start + TARGET_MAX_CHARS]
        if start + TARGET_MAX_CHARS >= len(text):
            pieces.append(text[start:])
            return pieces
        boundary = window.rfind(" ", int(TARGET_MAX_CHARS * 0.8))
        cut = boundary if boundary > 0 else TARGET_MAX_CHARS
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
) -> list[Chunk]:
    """Merge raw segmentation paragraphs (Uwazi field names) into ``Chunk``s.

    Deterministic: the same input always produces the same chunk list, and
    ``chunk_id`` is derived from the chunk identity tuple + zero-padded index.
    """
    parts: list[tuple[str, int | None]] = []
    for paragraph in paragraphs:
        if not _keepable(paragraph):
            continue
        page = paragraph.get("pageNumber")
        for piece in _split_long(paragraph["text"].strip()):
            parts.append((piece, page))

    chunks: list[Chunk] = []
    buffer: list[tuple[str, int | None]] = []

    def flush() -> None:
        if not buffer:
            return
        index = len(chunks)
        body = "\n".join(piece for piece, _ in buffer)
        pages = [page for _, page in buffer if page is not None]
        chunks.append(
            Chunk(
                chunk_id=f"{instance_key}:{shared_id}:{language}:{file_id}:{index:04d}",
                instance_key=instance_key,
                shared_id=shared_id,
                language=language,
                file_id=file_id,
                chunk_index=index,
                text=f"{_header(entity_title, template_name, pages[0] if pages else None)}\n{body}",
                page_start=min(pages) if pages else None,
                page_end=max(pages) if pages else None,
            )
        )
        buffer.clear()

    for piece, page in parts:
        joined = len("\n".join(piece_text for piece_text, _ in buffer))
        if buffer and joined + 1 + len(piece) > TARGET_MAX_CHARS:
            flush()
        buffer.append((piece, page))
    flush()
    return chunks
