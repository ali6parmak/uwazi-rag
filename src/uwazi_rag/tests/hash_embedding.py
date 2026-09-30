"""Test-only deterministic ``EmbeddingPort`` — hashed character n-grams.

AGENTS.md's testing policy bans mocks/stubs but blesses real offline
implementations (the in-memory vector store). This is the embedder
equivalent: real code, deterministic, network-free. It proves *orchestration*
(chunk → embed → store → search round-trips); it must never be used to judge
semantic quality — that is what the live bge-m3 cross-language run is for.
"""

from __future__ import annotations

import hashlib

from uwazi_rag.ports.embedding_port import EmbeddingPort


class HashingEmbedding(EmbeddingPort):
    """Signed feature-hashing of lower-cased character n-grams.

    Same text → same vector (deterministic); different texts share buckets
    proportionally to shared n-grams. Any dimension count, so tests can be
    tiny (e.g. 2 or 16 dims) and fast.
    """

    def __init__(self, dimensions: int = 64, ngram: int = 4) -> None:
        if dimensions < 1:
            raise ValueError(f"dimensions must be >= 1, got {dimensions}")
        self.dimensions = dimensions
        self.ngram = ngram

    def embed(self, texts: list[str]) -> list[list[float]]:
        return [self._embed_one(text) for text in texts]

    def _embed_one(self, text: str) -> list[float]:
        normalized = " ".join(text.lower().split())
        vector = [0.0] * self.dimensions
        for start in range(max(0, len(normalized) - self.ngram + 1)):
            gram = normalized[start : start + self.ngram]
            digest = hashlib.sha1(gram.encode("utf-8")).digest()
            bucket = int.from_bytes(digest[:4], "big") % self.dimensions
            vector[bucket] += 1.0 if digest[4] % 2 == 0 else -1.0
        return vector
