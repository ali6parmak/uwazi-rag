"""Domain model: a retrieval-ready piece of a document (PLAN.md Step 2)."""

from __future__ import annotations

from pydantic import BaseModel


class Chunk(BaseModel):
    """The embedded + retrieved unit.

    Identity is ``(instance_key, shared_id, language, file_id, chunk_index)``
    (PLAN.md golden rule 8): deterministic, so re-running the pipeline yields
    the same ids — re-runs overwrite, never duplicate. ``text`` carries a
    context header (title — template, page) so a chunk retrieved alone still
    says who/what it is about.

    ``paragraph_ids`` records the raw capture positions (0-based, gaps kept)
    whose text contributed to this chunk — the eval scorecard maps golden
    rows' ``expected.paragraph_ids`` to chunk ids through it (Step 3.5).
    A paragraph cut by the splitter appears in the (2+) chunks that own its
    pieces. Empty for chunks persisted before the field existed.
    """

    chunk_id: str
    instance_key: str
    shared_id: str
    language: str
    file_id: str
    chunk_index: int
    text: str
    page_start: int | None = None
    page_end: int | None = None
    paragraph_ids: list[int] = []
