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
  boundaries, over-long paragraphs stay whole; a split section's continuation
  chunks repeat its heading line at the top (text-assembly layer, added after
  packing — the heading never counts against the budget); a document with no
  heading falls back to the merge path byte-equal (the SectionChunker's
  graceful fallback).
- ``"section-split"`` — the same partition with monster handling: a single
  paragraph over the budget (always alone in its packing group) word-splits
  into consecutive pieces — ``overlap_ratio`` governs cuts INSIDE a paragraph
  (merge-style) while packing boundaries stay overlap-free; every piece chunk
  repeats its section heading, and the monster's paragraph anchors all its
  pieces, exactly like merge's split paragraphs.
- ``"type-merge"`` — merge's exact packing arithmetic plus ONE rule (Step 4c
  wave 3.4, user call 2026-10-13): a packing run breaks when a keepable
  paragraph's content type changes; ``section header``/``title`` paragraphs
  are glue — they take the effective type of the body run they preface (a
  trailing glue run keeps its own type), so "same types merge together; header
  and title may go together". Single-type corpora (every LBR/vic home) chunk
  byte-equal to ``"merge"`` by construction.

Two merge-only text layers (Step 4c wave 3.3, rung 2 on the winner — defaults
keep every legacy store byte-identical):

- ``sentence_cuts`` — merge's intra-paragraph (monster) cuts prefer the last
  sentence end (``.!?`` followed by whitespace) in the same cut window; no
  sentence end in the window → the exact legacy word cut; ``overlap_ratio``
  still governs the overlap band.
- ``breadcrumb`` — "title — section": the context header's template slot is
  replaced by the chunk's section heading line ("{title} — {heading line}
  (page n)") when the chunk's first paragraph sits in a heading section;
  preamble chunks keep today's header. Text-assembly layer added after
  packing — never counted against the budget. Requires ``prepend_header``
  and merge mode (the crumb IS the header's context slot).
"""

from __future__ import annotations

from uwazi_rag.domain.chunk import Chunk

TARGET_MIN_CHARS = 1200
TARGET_MAX_CHARS = 1800
OVERLAP_RATIO = 0.15
# Repeat-on-every-page boilerplate plus anything without text: never chunks.
DROP_TYPES = {"page header", "page footer"}
# The chunking-method axis (PLAN.md Step 4c wave 3.1 + 2026-10-13 user calls): recorded
# in store ``chunk_config`` as ``split_mode`` and re-driven by grading. "merge" is the
# default so legacy stores re-chunk byte-identically without the key.
SPLIT_MODES = ("merge", "segment", "section", "section-split", "type-merge")


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


# The wave-3.3 sentence_cuts layer's frozen constants (like the heading detector — never
# knobs): a sentence end is one of these characters followed by whitespace.
SENTENCE_DELIMITERS = frozenset(".!?")
_WHITESPACE = frozenset(" \t\n\r\f\v")


def sentence_split(text: str, target_max_chars: int = TARGET_MAX_CHARS, overlap_chars: int | None = None) -> list[str]:
    """Split one over-long paragraph at sentence ends where the window offers one.

    The wave-3.3 ``sentence_cuts`` layer: the same loop as :func:`_split_long`
    (same window, same ~0.8-budget floor, same overlap band), but the cut lands
    after the last ``.``/``!``/``?`` followed by whitespace inside the window;
    when the window holds no sentence end the cut falls back to the exact
    word-boundary logic — so this function can only make cuts read cleaner,
    never exceed the budget.
    """
    if overlap_chars is None:
        overlap_chars = int(target_max_chars * OVERLAP_RATIO)
    if len(text) <= target_max_chars:
        return [text]
    pieces: list[str] = []
    start = 0
    floor = int(target_max_chars * 0.8)
    while True:
        if start + target_max_chars >= len(text):
            pieces.append(text[start:])
            return pieces
        boundary = 0
        for position in range(start + target_max_chars - 1, start + floor - 1, -1):
            if text[position] in SENTENCE_DELIMITERS and (position + 1 >= len(text) or text[position + 1] in _WHITESPACE):
                boundary = position + 1
                break
        if boundary == 0:
            window = text[start : start + target_max_chars]
            word = window.rfind(" ", floor)
            boundary = start + word if word > 0 else start + target_max_chars
        pieces.append(text[start:boundary])
        start += boundary - start - overlap_chars


def _header(entity_title: str, context_name: str, page_start: int | None) -> str:
    """The header line: ``"{title} — {context} (page n)"``.

    ``context_name`` is the template name normally; the wave-3.3 ``breadcrumb``
    layer passes the section heading line instead ("title — section").
    """
    subject = entity_title or "Untitled"
    source = f"{subject} — {context_name}" if context_name else subject
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
    context: str | None = None,
) -> Chunk:
    """Assemble one ``Chunk`` from ``(piece, page, paragraph position)`` parts — the merge flush's exact construction.

    ``context`` (the wave-3.3 ``breadcrumb`` layer) replaces the header's
    template slot with the section heading line; ``None`` keeps the template,
    so the header text — never the body, ids, or counts — is the only thing
    the crumb can change.
    """
    body = "\n".join(piece for piece, _, _ in body_parts)
    pages = [page for _, page, _ in body_parts if page is not None]
    seen: set[int] = set()
    paragraph_ids: list[int] = []
    for _, _, pid in body_parts:
        if pid not in seen:
            seen.add(pid)
            paragraph_ids.append(pid)
    text = (
        f"{_header(entity_title, context or template_name, pages[0] if pages else None)}\n{body}" if prepend_header else body
    )
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
    sentence_cuts: bool = False,
    breadcrumb: bool = False,
) -> list[Chunk]:
    """Merge raw segmentation paragraphs (Uwazi field names) into ``Chunk``s.

    Deterministic: the same input always produces the same chunk list, and
    ``chunk_id`` is derived from the chunk identity tuple + zero-padded index.
    ``target_max_chars``/``overlap_ratio``/``prepend_header``/``split_mode`` are
    the eval sweep's knobs (Step 3.5, Step 4c wave 3.1), and
    ``sentence_cuts``/``breadcrumb`` are the wave-3.3 rung-2 layers on merge;
    defaults are the Step 2 constants and the merge mode, so existing call
    sites keep today's chunking, chunk identity never moves, and every store
    built before 4c byte-verifies unchanged.
    """
    if target_max_chars < 1:
        raise ValueError(f"target_max_chars must be >= 1, got {target_max_chars}")
    if not 0.0 <= overlap_ratio < 0.5:
        raise ValueError(f"overlap_ratio must be in [0, 0.5), got {overlap_ratio}")
    if split_mode not in SPLIT_MODES:
        raise ValueError(f"split_mode must be one of {', '.join(SPLIT_MODES)}, got {split_mode!r}")
    if sentence_cuts and split_mode != "merge":
        raise ValueError(f"sentence_cuts only applies to split_mode 'merge', got {split_mode!r}")
    if breadcrumb and split_mode != "merge":
        raise ValueError(f"breadcrumb only applies to split_mode 'merge', got {split_mode!r}")
    if breadcrumb and not prepend_header:
        raise ValueError("breadcrumb needs prepend_header — the crumb IS the header's context slot")
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

    if split_mode == "type-merge":
        # Wave 3.4 (user call 2026-10-13): merge's exact packing arithmetic — the same
        # parts stream, monster splits, and closure — plus one break rule: a packing run
        # ends when the next keepable paragraph's content type changes; heading types
        # glue forward (they carry the body run they preface). Lazy import, same cycle
        # reason as the section branch.
        from uwazi_rag.use_cases.headings import effective_types

        eff_by_pid = effective_types(paragraphs)
        type_parts: list[tuple[str, int | None, int, str]] = []
        for index, paragraph in enumerate(paragraphs):
            if not keepable(paragraph):
                continue
            page = paragraph.get("pageNumber")
            for piece in _split_long(str(paragraph["text"]).strip(), target_max_chars, overlap_chars):
                type_parts.append((piece, page, index, eff_by_pid[index]))
        type_chunks: list[Chunk] = []
        type_buffer: list[tuple[str, int | None, int, str]] = []

        def type_flush() -> None:
            if not type_buffer:
                return
            type_chunks.append(
                _emit_chunk(
                    body_parts=[(piece, page, pid) for piece, page, pid, _ in type_buffer],
                    instance_key=instance_key,
                    shared_id=shared_id,
                    language=language,
                    file_id=file_id,
                    entity_title=entity_title,
                    template_name=template_name,
                    prepend_header=prepend_header,
                    index=len(type_chunks),
                )
            )
            type_buffer.clear()

        run_type: str | None = None
        for piece, page, pid, eff in type_parts:
            joined = len("\n".join(piece_text for piece_text, _, _, _ in type_buffer))
            if type_buffer and (eff != run_type or joined + 1 + len(piece) > target_max_chars):
                type_flush()
            type_buffer.append((piece, page, pid, eff))
            run_type = eff
        type_flush()
        return type_chunks

    if split_mode in ("section", "section-split"):
        # Lazy import: headings.py holds keepable's second consumer (the detector), so the
        # detector cannot be a top-level import here without a cycle.
        from uwazi_rag.use_cases.headings import is_heading, pack_sections, partition_sections

        word_split = split_mode == "section-split"
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
        section_chunks: list[Chunk] = []
        for section in partition_sections(paragraphs):
            # Every section opens at its heading — except a leading preamble (no heading at
            # all). A split section's CONTINUATION chunks repeat the heading line at the top
            # so a chunk retrieved alone still names its section: the heading paragraph also
            # anchors the continuation through paragraph_ids. The repeated line is added at
            # text assembly, AFTER packing — not counted against the budget (user call
            # 2026-10-11) — exactly like prepend_header, which is why the wave-3.0 scan's
            # section/partition counts stay exact. The chunk header shows the heading's page.
            heading_pid = section[0] if is_heading(paragraphs[section[0]]) else None
            for group in pack_sections([section], paragraphs, target_max_chars):
                # A monster (a single paragraph over the budget) is always alone in its packing
                # group: plain section keeps it whole; section-split word-splits it into
                # consecutive pieces — overlap_ratio governs cuts INSIDE a paragraph
                # (merge-style), packing boundaries stay overlap-free. Every chunk emitted
                # from a continuation group repeats the section heading on top.
                monster_pid = None
                if word_split and len(group) == 1:
                    only_text = str(paragraphs[group[0]]["text"]).strip()
                    if len(only_text) > target_max_chars:
                        monster_pid = group[0]
                if monster_pid is not None:
                    monster = paragraphs[monster_pid]
                    page = monster.get("pageNumber")
                    bodies: list[list[tuple[str, int | None, int]]] = [
                        [(piece, page, monster_pid)]
                        for piece in _split_long(str(monster["text"]).strip(), target_max_chars, overlap_chars)
                    ]
                else:
                    bodies = [
                        [(str(paragraphs[pid]["text"]).strip(), paragraphs[pid].get("pageNumber"), pid) for pid in group]
                    ]
                for body_parts in bodies:
                    if heading_pid is not None and group[0] != heading_pid:
                        heading = paragraphs[heading_pid]
                        body_parts = [(str(heading["text"]).strip(), heading.get("pageNumber"), heading_pid), *body_parts]
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

    # Merge mode: the wave-3.3 crumb map (first pid → its section's heading line) is
    # built before the parts stream; preamble chunks stay headerless-of-crumb (None →
    # today's template header), and nothing here can move ids, pages, or packing.
    crumbs: dict[int, str] = {}
    if breadcrumb:
        # Lazy import (same cycle reason as the section branch).
        from uwazi_rag.use_cases.headings import is_heading, partition_sections

        for section in partition_sections(paragraphs):
            heading_pid = section[0] if is_heading(paragraphs[section[0]]) else None
            if heading_pid is None:
                continue
            heading_line = str(paragraphs[heading_pid]["text"]).splitlines()[0].strip()
            if heading_line:
                crumbs.update((pid, heading_line) for pid in section)

    # (text piece, page, raw paragraph position) — the position anchors the
    # chunk back to paragraph_ids even where dropped paragraphs leave gaps.
    # Merge mode only (below): the segment/section/type-merge modes returned earlier.
    parts: list[tuple[str, int | None, int]] = []
    for index, paragraph in enumerate(paragraphs):
        if not keepable(paragraph):
            continue
        page = paragraph.get("pageNumber")
        splitter = sentence_split if sentence_cuts else _split_long
        for piece in splitter(str(paragraph["text"]).strip(), target_max_chars, overlap_chars):
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
                context=crumbs.get(buffer[0][2]),
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
