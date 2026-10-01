"""Test-only deterministic ``LlmPort`` — answers every prompt with strict JSON.

Mirrors ``HashingEmbedding``: AGENTS.md blesses real, offline port
implementations (never mocks). The reply is derived deterministically from
the prompt's own excerpt with a gap-every-second-word scheme, so questions
never contain 5 consecutive passage words and always pass the validator.
These tests prove *orchestration* (group → prompt → reply → rows); they must
never judge generation quality — that is what the live model run plus the
human review are for.
"""

from __future__ import annotations

import json

from uwazi_rag.ports.llm_port import LlmPort

PROMPT_EXCERPT_TAG = "Excerpt (title removed, just text):"


def excerpt_of(prompt: str) -> str:
    """The passage text inside a generation prompt (everything after the tag)."""
    return prompt.split(PROMPT_EXCERPT_TAG + "\n", 1)[-1]


def _questions_from(prompt: str) -> list[dict[str, str]]:
    from uwazi_rag.use_cases.build_golden import question_tokens

    words = question_tokens(excerpt_of(prompt))
    picked = words[0::2][:12]  # gap between picks: a copied 5-word run is impossible
    return [
        {"form": "specific", "question": f"what does it say about {' '.join(picked[0:5])}?"},
        {"form": "broader", "question": f"why does this matter for {' '.join(picked[3:9])}?"},
    ]


class EchoJsonLlm(LlmPort):
    """Real port implementation: strict-JSON, validator-passing, prompt-derived replies."""

    def chat(self, messages: list[dict[str, str]]) -> str:
        return json.dumps(_questions_from(messages[-1]["content"]), ensure_ascii=False)


class GarbageJsonLlm(EchoJsonLlm):
    """A real LLM that answers prose — the parser must reject it (after retries)."""

    def chat(self, messages: list[dict[str, str]]) -> str:
        return "Sure! Here are the questions you asked for."


class EmptyListLlm(EchoJsonLlm):
    """A real LLM that returns a valid but question-less JSON array."""

    def chat(self, messages: list[dict[str, str]]) -> str:
        return json.dumps([{"form": "specific"}])


class FlakyJsonLlm(EchoJsonLlm):
    """A real LLM whose odd-numbered calls answer garbage, even-numbered calls succeed."""

    def __init__(self) -> None:
        self.calls = 0

    def chat(self, messages: list[dict[str, str]]) -> str:
        self.calls += 1
        if self.calls % 2 == 1:
            return "<not json>"
        return super().chat(messages)


class DuplicateJsonLlm(EchoJsonLlm):
    """A real LLM that asks the same question twice per group (within-group dedup)."""

    def chat(self, messages: list[dict[str, str]]) -> str:
        return json.dumps(
            [
                {"form": "specific", "question": "what changed in this collection?"},
                {"form": "broader", "question": "What changed in THIS collection!"},
            ],
            ensure_ascii=False,
        )
