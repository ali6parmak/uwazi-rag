"""Step 4c wave 3.0 — the pure heading detector behind the SectionChunker (offline, frozen).

PLAN.md Step 4c pre-stated the rules; they are code constants, never knobs:

- a TYPED paragraph (Uwazi segmentation types — the wave-0 scan verified they exist on the
  Uwazi capture homes) is a heading exactly when its type is one of
  ``UWAZI_HEADING_TYPES``. Types take precedence: where a type is present the regex never
  runs, so a typed body paragraph can never split on its content;
- a TYPELESS paragraph (the dataset homes are line-partitioned typeless) is a heading
  exactly when its first whitespace-stripped line matches one of three line-initial rules:
  an enumerated contract marker (``ARTICLE|SECTION|EXHIBIT|SCHEDULE|ANNEX|APPENDIX|PART|
  RECITALS``, uppercase, word-bounded — plus ``§``), an ordinal (``\\d+(\\.\\d+)*\\b`` at line
  start — word-bounded like the markers, a 2026-10-11 user-called refinement: digit-initial
  words such as ``23andMe`` never head), or a short all-caps line (≤``ALL_CAPS_MAX_CHARS``
  chars, at least one letter, no terminal ``.,;:``). Line-initial only — mid-line cross-references never split: only the
  paragraph's own first line is examined, so a heading verdict never cuts inside a
  paragraph's body.

Also here (shared with the wave-3.1 SectionChunker so the two can never drift): the
section partition of one capture, and the budget packer — over-cap sections split at
paragraph boundaries, overlap 0, with exactly ``build_chunks``' closure arithmetic.
"""

from __future__ import annotations

import re

from uwazi_rag.use_cases.chunking import keepable

# Uwazi segmentation types that mark a heading (lowercase — capture types are matched
# case-insensitively). "section header" is the segmentation's own heading signal; the rare
# "title" boxes are document-title furniture that heads their section the same way.
UWAZI_HEADING_TYPES = frozenset({"section header", "title"})

# The pre-stated all-caps budget: a heading line is short (≤ ~110 chars per PLAN.md 4c).
ALL_CAPS_MAX_CHARS = 110
# A line ending in sentence punctuation is prose, not a heading — except enumerated
# markers, which are checked first and may carry it ("RECITALS:").
TERMINAL_PUNCTUATION = frozenset(".,;:")

# Word-boundary guards keep suffixes/prose out: "PARTIES"/"ARTICLES"/"PARTLY" do not match,
# lowercase ("Article 5") does not match — markers are uppercase, per the pre-stated rule.
# Same guard on the ordinal (user call 2026-10-11, option b): "23andMe" is not an ordinal
# heading, while "2.3 DEFINITIONS", "1." and a bare year still are.
_HEADING_MARKER_RE = re.compile(r"^(?:ARTICLE|SECTION|EXHIBIT|SCHEDULE|ANNEX|APPENDIX|PART|RECITALS)\b|^§")
_ORDINAL_RE = re.compile(r"^\d+(?:\.\d+)*\b")


def is_heading(paragraph: dict) -> bool:
    """One raw capture paragraph → heading verdict (the SectionChunker's only split signal).

    The mirror of :func:`uwazi_rag.use_cases.chunking.keepable` — one rule, two consumers
    (the wave-3.0 scan and the wave-3.1 chunker call the very same function).
    """
    text = paragraph.get("text")
    if not isinstance(text, str) or not text.strip():
        return False
    paragraph_type = (paragraph.get("type") or "").strip().lower()
    if paragraph_type:
        return paragraph_type in UWAZI_HEADING_TYPES
    line = text.splitlines()[0].strip()
    if not line:
        return False
    if _HEADING_MARKER_RE.match(line):
        return True
    if _ORDINAL_RE.match(line):
        return True
    letters = [char for char in line if char.isalpha()]
    return (
        bool(letters)
        and len(line) <= ALL_CAPS_MAX_CHARS
        and not any(char.islower() for char in letters)
        and line[-1] not in TERMINAL_PUNCTUATION
    )


def partition_sections(paragraphs: list[dict]) -> list[list[int]]:
    """Split a capture's keepable paragraphs into sections at heading boundaries (pure).

    Each section runs from one heading to the next: the heading paragraph belongs to its
    own section (its text is body content a chunk must carry), dropped paragraphs (page
    headers/footers, empty boxes) never appear, and a document with no headings is one
    section. Ascending paragraph-id groups; capture gaps stay gaps (same convention as
    ``build_chunks`` paragraph_ids).
    """
    sections: list[list[int]] = []
    current: list[int] = []
    for index, paragraph in enumerate(paragraphs):
        if not keepable(paragraph):
            continue
        if current and is_heading(paragraph):
            sections.append(current)
            current = []
        current.append(index)
    if current:
        sections.append(current)
    return sections


def section_chars(paragraphs: list[dict], paragraph_ids: list[int]) -> int:
    """A group's body length the way the chunker joins it: pieces + one ``\\n`` per join."""
    return sum(len(str(paragraphs[paragraph_id]["text"]).strip()) for paragraph_id in paragraph_ids) + len(paragraph_ids) - 1


def pack_sections(sections: list[list[int]], paragraphs: list[dict], target_max_chars: int) -> list[list[int]]:
    """Split every over-budget section at paragraph boundaries, overlap 0 (pure).

    PLAN.md Step 4c wave 3.1: interior spans are packed at the SAME per-dataset budget as
    the section chunker's merge competitor; a section longer than the budget closes a chunk
    just before pushing past it — ``build_chunks``' closure arithmetic, at paragraph
    boundaries. One paragraph over the budget has no boundary inside and stays whole: that
    over-budget chunk is the section method's accepted cost, counted by the wave-3.0 scan.
    """
    if target_max_chars < 1:
        raise ValueError(f"target_max_chars must be >= 1, got {target_max_chars}")
    groups: list[list[int]] = []
    for section in sections:
        group: list[int] = []
        joined = 0
        for paragraph_id in section:
            piece = str(paragraphs[paragraph_id]["text"]).strip()
            if group and joined + 1 + len(piece) > target_max_chars:
                groups.append(group)
                group = []
                joined = 0
            joined = len(piece) if not group else joined + 1 + len(piece)
            group.append(paragraph_id)
        if group:
            groups.append(group)
    return groups
