"""Domain model: the eval-anchor granule of a document (PLAN.md Step 3.5)."""

from __future__ import annotations

from pydantic import BaseModel


class PassageGroup(BaseModel):
    """A contiguous run of keepable paragraphs packed to ~``GROUP_TARGET_CHARS``.

    The golden dataset's grouping unit: questions are generated from — and
    anchored to — these groups, so ``paragraph_ids`` (0-based positions in the
    raw capture where dropped paragraphs leave gaps) survive any chunking
    configuration and the dataset stays valid across a chunk-size sweep. ``text`` is the raw
    paragraph text only — never the entity title or page furniture — exactly
    what the question generator is shown. ``group_id`` is deterministic, like
    ``chunk_id``, so re-runs reuse the same identity.
    """

    group_id: str
    instance_key: str
    shared_id: str
    language: str
    file_id: str
    group_index: int
    title: str
    paragraph_ids: list[int]
    text: str
    page_start: int | None = None
    page_end: int | None = None
