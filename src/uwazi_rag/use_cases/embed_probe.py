"""The Step 0 probe: embed one sentence and report what came back.

Kept as a pure function over the ``EmbeddingPort`` so the driver stays thin
and the result type is trivially inspectable.
"""

from __future__ import annotations

from dataclasses import dataclass

from uwazi_rag.ports.embedding_port import EmbeddingPort

PREVIEW_VALUES = 5


@dataclass(frozen=True)
class EmbedProbeResult:
    """What the smoke test learned about the configured embedding model."""

    model: str
    base_url: str
    text: str
    vector: list[float]

    @property
    def dimensions(self) -> int:
        return len(self.vector)

    @property
    def preview(self) -> list[float]:
        return [round(value, 6) for value in self.vector[:PREVIEW_VALUES]]


def run_embed_probe(
    embeddings: EmbeddingPort,
    *,
    text: str,
    model: str,
    base_url: str,
) -> EmbedProbeResult:
    """Embed one sentence and return the vector with display metadata."""
    (vector,) = embeddings.embed([text])
    return EmbedProbeResult(model=model, base_url=base_url, text=text, vector=vector)


def format_probe_report(probe: EmbedProbeResult, expected_dimensions: int) -> str:
    """Render the scorecard-looking output for the CLI (pure, testable)."""
    ok = probe.dimensions == expected_dimensions
    verdict = "OK" if ok else f"MISMATCH (expected {expected_dimensions}, from config)"
    return "\n".join(
        [
            f"ollama : {probe.base_url}",
            f"model  : {probe.model}",
            f"text   : {probe.text!r}",
            f"vector : {probe.dimensions} values — {verdict}",
            f"first  : {probe.preview}",
        ]
    )
