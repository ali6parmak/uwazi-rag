"""Pure Okapi BM25 over chunk texts + the BM25 retrieval method (Step 3.5 method-comparison arm).

Deliberately simple and deterministic — this module exists to be raced
against pure-embedding retrieval on the same golden set, and to be
unit-testable with exact hand-computed values:

- tokenization: unicode word characters, lower-cased — accents kept (the
  corpus is en/es legal text), no stemming (the golden set's in-text number
  probes need exact-token matching; lexical fuzz can come later)
- Okapi formula with the Lucene-style non-negative idf:
  ``idf(t) = ln((N - df + 0.5) / (df + 0.5) + 1)``
  ``score(q, d) = Σ over unique query terms of idf(t) · tf·(k1+1) /
  (tf + k1 · (1 − b + b·|d|/avgdl))``
- k1 = 1.2, b = 0.75 (the classic defaults) — parameters, not magic
- repeated query terms count once; unknown terms contribute zero
- documents absent from a term score stay in the ranking at 0 (deterministic
  insertion-order tie-break), so callers can always slice a fixed depth

:class:`Bm25Retrieval` is the method instance; its settings are constructor
params. The default instance is exactly what the shared grading path's
``rank_rows(retrieval="bm25")`` computes.
"""

from __future__ import annotations

import math
import re
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any

from uwazi_rag.use_cases.eval_retrieval import RETRIEVAL_DEPTH, DocKey, Hit
from uwazi_rag.use_cases.retrieval_methods.base import RetrievalMethod

if TYPE_CHECKING:
    from uwazi_rag.ports.embedding_port import EmbeddingPort
    from uwazi_rag.use_cases.eval_run import PreparedRun

_TOKEN = re.compile(r"\w+", re.UNICODE)


def tokenize(text: str) -> tuple[str, ...]:
    """Lower-cased unicode word tokens — the whole lexical identity of BM25 here."""
    return tuple(_TOKEN.findall(text.lower()))


class Bm25Index:
    """Scanned BM25 over a fixed document set (built once per store, queried per row)."""

    def __init__(self, documents: Mapping[str, str], *, k1: float = 1.2, b: float = 0.75) -> None:
        if k1 < 0.0:
            raise ValueError(f"k1 must be >= 0, got {k1}")
        if not 0.0 <= b <= 1.0:
            raise ValueError(f"b must be in [0, 1], got {b}")
        self.k1 = k1
        self.b = b
        self.doc_ids: tuple[str, ...] = tuple(documents)
        tokens_per_doc = [tokenize(documents[doc_id]) for doc_id in self.doc_ids]
        self.doc_lengths: tuple[int, ...] = tuple(len(tokens) for tokens in tokens_per_doc)
        total = sum(self.doc_lengths)
        avgdl = total / len(self.doc_lengths) if self.doc_lengths else 0.0
        self.avgdl: float = avgdl if avgdl > 0.0 else 1.0  # all-empty corpus: keep the ratio finite
        self._df: dict[str, int] = {}
        self._postings: dict[str, list[tuple[int, int]]] = {}
        for row, tokens in enumerate(tokens_per_doc):
            frequency: dict[str, int] = {}
            for token in tokens:
                frequency[token] = frequency.get(token, 0) + 1
            for token, tf in frequency.items():
                self._df[token] = self._df.get(token, 0) + 1
                self._postings.setdefault(token, []).append((row, tf))

    def idf(self, term: str) -> float:
        """Non-negative inverse document frequency (unknown terms still score ≥ 0)."""
        df = self._df.get(term, 0)
        n = len(self.doc_ids)
        return math.log((n - df + 0.5) / (df + 0.5) + 1.0)

    def score_values(self, query: str) -> list[float]:
        """Per-document BM25 scores in insertion order (no ranking)."""
        scores = [0.0] * len(self.doc_ids)
        for term in dict.fromkeys(tokenize(query)):
            postings = self._postings.get(term)
            if not postings:
                continue
            idf = self.idf(term)
            for row, tf in postings:
                dl = self.doc_lengths[row]
                denominator = tf + self.k1 * (1.0 - self.b + self.b * dl / self.avgdl)
                scores[row] += idf * tf * (self.k1 + 1.0) / denominator
        return scores

    def score(self, query: str) -> list[tuple[str, float]]:
        """Every document best-first; ties break by insertion order (deterministic)."""
        scores = self.score_values(query)
        order = sorted(range(len(self.doc_ids)), key=lambda row: (-scores[row], row))
        return [(self.doc_ids[row], scores[row]) for row in order]


class Bm25Retrieval(RetrievalMethod):
    """Pure lexical BM25 over the store's chunk texts — no embeddings involved.

    Settings are constructor params (the :class:`Bm25Index` k1/b); the default
    instance is exactly ``rank_rows(retrieval="bm25")`` on the shared path.
    Scores are lexical saturating weights on a different scale than cosine, so
    this method is not cosine-calibrated: false-retrieval is not measured.
    """

    def __init__(self, *, k1: float = 1.2, b: float = 0.75) -> None:
        """Validate eagerly (mirrors :class:`Bm25Index`) so a bad instance fails at definition."""
        if k1 < 0.0:
            raise ValueError(f"k1 must be >= 0, got {k1}")
        if not 0.0 <= b <= 1.0:
            raise ValueError(f"b must be in [0, 1], got {b}")
        self.k1 = k1
        self.b = b

    @property
    def name(self) -> str:
        return "bm25"

    def params(self) -> dict[str, Any]:
        return {"k1": self.k1, "b": self.b}

    def describe(self) -> str:
        return f"bm25 k1={self.k1:g} b={self.b:g}"

    def rank(self, prepared: PreparedRun, *, embedder: EmbeddingPort | None = None) -> dict[str, list[Hit]]:
        """Rank chunks lexicographically — the store contributes texts only, no embeddings."""
        chunks = prepared.store.chunks()
        doc_keys: dict[str, DocKey] = {
            chunk.chunk_id: (chunk.instance_key, chunk.shared_id, chunk.language) for chunk in chunks
        }
        index = Bm25Index({chunk.chunk_id: chunk.text for chunk in chunks}, k1=self.k1, b=self.b)
        hits_by_row: dict[str, list[Hit]] = {}
        for row in prepared.rows:
            hits_by_row[str(row["id"])] = [
                Hit(chunk_id=chunk_id, doc_key=doc_keys[chunk_id], score=score)
                for chunk_id, score in index.score(str(row["question"]))[:RETRIEVAL_DEPTH]
            ]
        return hits_by_row
