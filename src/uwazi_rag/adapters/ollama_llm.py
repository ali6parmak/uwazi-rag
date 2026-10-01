from __future__ import annotations

import httpx

from uwazi_rag.configuration import LLM_MODEL, OLLAMA_BASE_URL
from uwazi_rag.ports.llm_port import LlmPort


class OllamaLlm(LlmPort):
    """LlmPort adapter backed by Ollama's chat endpoint.

    Calls ``POST {OLLAMA_BASE_URL}/api/chat`` with ``{"model": …, "messages":
    …, "stream": false}`` and returns ``data["message"]["content"]``. The
    golden-set model is often cloud-served through the local daemon, so the
    default timeout is generous.
    """

    def __init__(self, model: str | None = None, base_url: str | None = None, timeout: float = 600.0) -> None:
        self.model = model or LLM_MODEL
        self.base_url = (base_url or OLLAMA_BASE_URL).rstrip("/")
        self.timeout = timeout
        if not self.model:
            raise RuntimeError(
                "LLM_MODEL is not set — add it to .env (e.g. LLM_MODEL=glm-5.3-flash:cloud); "
                "models come from config, never code (PLAN.md golden rule 7)"
            )

    def chat(self, messages: list[dict[str, str]]) -> str:
        try:
            response = httpx.post(
                f"{self.base_url}/api/chat",
                json={"model": self.model, "messages": messages, "stream": False},
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

        message = response.json().get("message")
        content = message.get("content") if isinstance(message, dict) else None
        if not isinstance(content, str) or not content.strip():
            raise RuntimeError("Unexpected Ollama /api/chat response shape: expected non-empty text at message.content.")
        return content
