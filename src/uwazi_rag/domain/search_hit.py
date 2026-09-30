"""Domain model: one semantic-search result (PLAN.md Step 3)."""

from __future__ import annotations

from pydantic import BaseModel

from uwazi_rag.domain.chunk import Chunk


class SearchHit(BaseModel):
    """A chunk plus how close its embedding sits to the query.

    ``similarity`` is the raw cosine in ``[-1.0, 1.0]`` — ranking uses it
    as-is, the CLI only rounds it for display.
    """

    chunk: Chunk
    similarity: float
