"""The merge chunker as a method instance — the one chunker PLAN.md settled on.

``MergeChunker`` is a thin settings-carrying wrapper over
:func:`uwazi_rag.use_cases.index_captures.capture_to_chunks`, which is the
shared entry into :func:`uwazi_rag.use_cases.chunking.build_chunks` — there is
still exactly one chunker; instances only hold its parameters. The science
guard leans on this equality: grading re-chunks via the store's recorded
config and byte-verifies the store, so a ``MergeChunker`` and the shared
chunker can never quietly diverge.
"""

from __future__ import annotations

from typing import Any

from uwazi_rag.domain.chunk import Chunk
from uwazi_rag.use_cases.chunking import OVERLAP_RATIO, TARGET_MAX_CHARS
from uwazi_rag.use_cases.chunking_methods.base import ChunkMethod
from uwazi_rag.use_cases.index_captures import capture_to_chunks


class MergeChunker(ChunkMethod):
    """Merge adjacent segmentation paragraphs into retrieval-sized chunks.

    Settings are constructor params (the Step 2 constants are the defaults):
    ``max_chars`` closes a chunk just before the budget, ``overlap`` is the
    fraction long split paragraphs share, ``header`` prepends the
    ``"{title} — {template} (page n)"`` context line. The wave-3.3 rung-2
    layers ride as separate flags: ``sentence_cuts`` prefers sentence ends in
    the monster-cut window, ``breadcrumb`` replaces the header's template slot
    with the chunk's section heading line ("title — section"). Both default
    OFF — and join ``params()``/``chunk_config()`` only when ON — so the plain
    instance keeps the exact legacy store identity the committed merge stores
    were built with (and the lock's merge bytes never move).
    """

    def __init__(
        self,
        *,
        max_chars: int = TARGET_MAX_CHARS,
        overlap: float = OVERLAP_RATIO,
        header: bool = True,
        sentence_cuts: bool = False,
        breadcrumb: bool = False,
    ) -> None:
        """Validate eagerly (mirrors the chunker) so a bad instance fails at definition."""
        if max_chars < 1:
            raise ValueError(f"max_chars must be >= 1, got {max_chars}")
        if not 0.0 <= overlap < 0.5:
            raise ValueError(f"overlap must be in [0, 0.5), got {overlap}")
        if breadcrumb and not header:
            raise ValueError("breadcrumb needs header — the crumb IS the header's context slot")
        self.max_chars = max_chars
        self.overlap = overlap
        self.header = header
        self.sentence_cuts = sentence_cuts
        self.breadcrumb = breadcrumb

    @property
    def name(self) -> str:
        return "merge"

    def params(self) -> dict[str, Any]:
        params: dict[str, Any] = {"max_chars": self.max_chars, "overlap": self.overlap, "header": self.header}
        # ``layers`` is the slug-facing summary (store file names are slug-built from
        # params() values — two boolean True values would collide identically); the
        # store's recorded chunk_config carries the granular ``sentence_cuts``/``breadcrumb``
        # keys instead. The plain instance stays exactly the legacy three-param identity.
        layers: list[str] = []
        if self.sentence_cuts:
            layers.append("sentences")
        if self.breadcrumb:
            layers.append("crumb")
        if layers:
            params["layers"] = "-".join(layers)
        return params

    def chunk_config(self) -> dict[str, Any]:
        config: dict[str, Any] = {
            "target_max_chars": self.max_chars,
            "overlap_ratio": self.overlap,
            "prepend_header": self.header,
        }
        if self.sentence_cuts:
            config["sentence_cuts"] = True
        if self.breadcrumb:
            config["breadcrumb"] = True
        return config

    def describe(self) -> str:
        return (
            f"merge {self.max_chars}/{self.overlap:g}/{'on' if self.header else 'off'}"
            + (" +sentences" if self.sentence_cuts else "")
            + (" +breadcrumb" if self.breadcrumb else "")
        )

    def _chunk(self, capture: dict) -> list[Chunk]:
        return capture_to_chunks(capture, **self.chunk_config())
