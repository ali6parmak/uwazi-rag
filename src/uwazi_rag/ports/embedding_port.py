from __future__ import annotations

from abc import ABC, abstractmethod


class EmbeddingPort(ABC):
    """Port for turning text into embedding vectors (e.g. via Ollama).

    An embedding is a fixed-length list of floats describing a text's meaning;
    similar meanings get similar vectors, across languages and wordings. The
    model and its vector size live in configuration, never in code
    (PLAN.md golden rule 7).
    """

    @abstractmethod
    def embed(self, texts: list[str]) -> list[list[float]]:
        """Embed a batch of texts — one vector per input, in the same order.

        Batching is part of the contract: adapters should send the whole list
        in one request when the provider allows it.
        """
