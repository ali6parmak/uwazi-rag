from __future__ import annotations

import httpx

from uwazi_rag.configuration import EMBEDDING_MODEL, OLLAMA_BASE_URL
from uwazi_rag.ports.embedding_port import EmbeddingPort


class OllamaEmbeddings(EmbeddingPort):
    """EmbeddingPort adapter backed by Ollama's batch endpoint.

    Calls ``POST {OLLAMA_BASE_URL}/api/embed`` with ``{"model": …,
    "input": [...]}`` — ``input`` being a list gives us batching for free
    (PLAN.md Step 3). Response shape: ``{"embeddings": [[float, …], …]}``
    (requires Ollama >= 0.3, where ``/api/embed`` replaced ``/api/embeddings``).
    """

    def __init__(
        self,
        model: str | None = None,
        base_url: str | None = None,
        timeout: float = 300.0,
    ) -> None:
        self.model = model or EMBEDDING_MODEL
        self.base_url = (base_url or OLLAMA_BASE_URL).rstrip("/")
        self.timeout = timeout

    def embed(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        try:
            response = httpx.post(
                f"{self.base_url}/api/embed",
                json={"model": self.model, "input": texts},
                timeout=self.timeout,
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as error:
            detail = error.response.text[:200]
            raise RuntimeError(
                f"Ollama returned HTTP {error.response.status_code} for model '{self.model}' at {self.base_url}: {detail}"
            ) from error
        except httpx.HTTPError as error:
            raise RuntimeError(
                f"Could not reach Ollama at {self.base_url} — is it running? (start it with `ollama serve`) | {error}"
            ) from error

        embeddings = response.json().get("embeddings")
        if not isinstance(embeddings, list) or len(embeddings) != len(texts):
            raise RuntimeError(
                f"Unexpected Ollama /api/embed response shape: expected an 'embeddings' list with {len(texts)} vector(s)."
            )
        return embeddings
