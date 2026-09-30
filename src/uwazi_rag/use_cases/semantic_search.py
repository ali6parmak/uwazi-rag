"""Step 3: naive semantic search — embed the query, cosine-scan the store.

The store owns the vectors and the scan; this use case embeds the query
through the port, shapes ``SearchHit``s and renders them for humans. Pure
with respect to the ports, so it is unit-testable offline (AGENTS.md policy).
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol

from uwazi_rag.domain.chunk import Chunk
from uwazi_rag.domain.search_hit import SearchHit
from uwazi_rag.ports.embedding_port import EmbeddingPort


class SearchableVectorStore(Protocol):
    """What search needs from a store; the ``VectorStore`` port refines it in Step 5."""

    def search(
        self, vector: Sequence[float], *, k: int = 5, instance_key: str | None = None
    ) -> list[tuple[Chunk, float]]: ...


def semantic_search(
    *,
    query: str,
    store: SearchableVectorStore,
    embedder: EmbeddingPort,
    k: int = 5,
) -> list[SearchHit]:
    """Embed ``query`` (one vector) and return the top-k hits, best first."""
    if not query.strip():
        raise ValueError("query is empty — give `search` something to look for")
    vectors = embedder.embed([query])
    return [SearchHit(chunk=chunk, similarity=similarity) for chunk, similarity in store.search(vectors[0], k=k)]


def format_search_results(hits: list[SearchHit], *, base_url: str | None = None) -> str:
    """Render hits: similarity, context header, pages, snippet and a Uwazi link.

    ``base_url`` (from config, when set) turns every hit into a link back into
    Uwazi — ``/{language}/entity/{sharedId}`` — previewing Step 6's citations.
    """
    if not hits:
        return "(no hits — the index is empty or nothing matched)"
    blocks: list[str] = []
    for rank, hit in enumerate(hits, start=1):
        lines = hit.chunk.text.split("\n", 1)
        header = lines[0]
        body = lines[1] if len(lines) > 1 else ""
        pages = f", pages {hit.chunk.page_start}..{hit.chunk.page_end}" if hit.chunk.page_start is not None else ""
        block = f"{rank}. [cos {hit.similarity:+.4f}] {header}{pages}"
        block += f"\n    {hit.chunk.chunk_id}"
        if body:
            block += f"\n    {body[:160].replace(chr(10), ' ')}..."
        if base_url:
            block += f"\n    {base_url}/{hit.chunk.language}/entity/{hit.chunk.shared_id}"
        blocks.append(block)
    return "\n".join(blocks)
