from __future__ import annotations

from abc import ABC, abstractmethod


class LlmPort(ABC):
    """Port for instructing a large-language model (e.g. via Ollama).

    Step 3.5 uses it to draft golden-set questions — the only contract needed
    is "send this conversation, give me the reply text". Step 6 fleshes the
    port out for RAG answering. The model name lives in configuration, never
    in code (PLAN.md golden rule 7).
    """

    @abstractmethod
    def chat(self, messages: list[dict[str, str]]) -> str:
        """Send chat messages (``{"role": ..., "content": ...}``), return the reply text.

        Blocking, non-streaming: the promise is the complete reply, one string.
        """
