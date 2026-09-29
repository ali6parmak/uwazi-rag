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
