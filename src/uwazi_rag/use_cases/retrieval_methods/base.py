"""The retrieval-method ABC — minimal, after :mod:`uwazi_rag.ports.embedding_port`.

Everything a benchmark needs from a method is here: rank a prepared run, and
say what you are. Settings are constructor params on instances, never files;
the ABC only fixes the output contract (``{row_id: [Hit]}``) so all methods
grade identically.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

from uwazi_rag.ports.embedding_port import EmbeddingPort
from uwazi_rag.use_cases.eval_retrieval import Hit

if TYPE_CHECKING:
    # Type-only: eval_run imports this package's primitive modules, so a runtime
    # import would be circular. PreparedRun is the one graded-run object.
    from uwazi_rag.use_cases.eval_run import PreparedRun


class RetrievalMethod(ABC):
    """One ranked-retrieval strategy; parameterize it by constructing instances.

    ``rank`` produces, for every golden row of the prepared run, the ranked
    ``Hit`` list the scorecard consumes. Implementations route through the
    shared ranking path so the numbers a sweep records can never disagree with
    an ``eval`` run over the same store — the offline equivalence tests pin
    each default-parameter instance to ``rank_rows`` exactly.
    """

    # Only cosine-calibrated methods may report false-retrieval (top-1 score
    # vs a threshold). Non-cosine scores (BM25 weights, RRF 1/(k+rank) sums)
    # are on a different scale — score_rows' threshold=None semantics apply.
    cosine_calibrated: bool = False

    @property
    @abstractmethod
    def name(self) -> str:
        """The method family's name; instance settings live in ``params()``."""

    @abstractmethod
    def rank(self, prepared: PreparedRun, *, embedder: EmbeddingPort | None = None) -> dict[str, list[Hit]]:
        """Rank every golden row of ``prepared``.

        Embedding-based methods require ``embedder`` (the store's own model);
        raise a self-explaining ``ValueError`` when it is missing.
        """

    def params(self) -> dict[str, Any]:
        """This instance's settings — JSON-safe primitives, recorded in results.md."""
        return {}

    def describe(self) -> str:
        """Compact settings string for results.md cells (e.g. ``rrf k=60 w=1.0/1.0``)."""
        return self.name
