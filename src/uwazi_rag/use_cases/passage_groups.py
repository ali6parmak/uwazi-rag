"""Step 3.5: cut captures into question-anchoring passage groups (pure).

A *passage group* is the golden dataset's grouping unit: consecutive keepable
paragraphs — the same drop rule as the chunker, shared code not a copy —
packed up to ``GROUP_TARGET_CHARS``; a single longer paragraph is its own
(unsplittable) group. Unlike the chunker, whose constants the eval harness
sweeps, this rule is FIXED: questions anchor to ``paragraph_ids``, which
survive any chunk configuration.

Sampling is deterministic: one seeded RNG per capture with a fixed draw order
(first the group indices, then one cross-language flag per sampled group), so
a re-run always selects the same groups and flags.
"""

from __future__ import annotations

import random

from uwazi_rag.domain.passage_group import PassageGroup
from uwazi_rag.use_cases.chunking import keepable

# The grouping rule is FIXED and independent of the chunker constants (PLAN.md
# Step 3.5) — the chunker's numbers get swept by the harness, this one never.
GROUP_TARGET_CHARS = 1200
GROUPS_PER_DOCUMENT = 2
CROSS_LANGUAGE_RATIO = 0.25
# Records the sampling draw itself, not just the seed rule: bumping it (or
# changing SEED_PREFIX) re-draws which groups get questions. Documented in
# data/eval/about.md so every dataset generation is reproducible.
SAMPLING_SEED = 20261001
SEED_PREFIX = "uwazi-rag/golden/v1"


def numbered_keepable_paragraphs(paragraphs: list[dict]) -> list[tuple[int, dict]]:
    """``(paragraph_id, paragraph)`` per keepable paragraph, in document order.

    ``paragraph_id`` is the paragraph's 0-based index in the raw capture
    (dropped paragraphs leave gaps) — the deterministic canonical index golden
    rows anchor to. Raw positions (not a dense renumber) stay valid if the
    drop rule ever changes and point straight into the capture JSON.
    """
    return [(index, paragraph) for index, paragraph in enumerate(paragraphs) if keepable(paragraph)]


def build_passage_groups(
    paragraphs: list[dict],
    *,
    instance_key: str,
    shared_id: str,
    language: str,
    file_id: str,
    title: str,
) -> list[PassageGroup]:
    """Pack numbered keepable paragraphs into passage groups.

    Greedy: append the next paragraph while the joined text stays within
    ``GROUP_TARGET_CHARS``; close the group before pushing past it. A single
    paragraph longer than the target is its own group — never split, so a
    group's text is always whole paragraphs, in document order.

    Deterministic: same input → same groups, with ``group_id`` derived like
    ``chunk_id`` (identity tuple + zero-padded index).
    """
    groups: list[PassageGroup] = []
    buffer: list[tuple[int, dict]] = []

    def flush() -> None:
        if not buffer:
            return
        index = len(groups)
        texts = [str(paragraph["text"]).strip() for _, paragraph in buffer]
        ids = [paragraph_id for paragraph_id, _ in buffer]
        pages = [int(paragraph["pageNumber"]) for _, paragraph in buffer if paragraph.get("pageNumber") is not None]
        groups.append(
            PassageGroup(
                group_id=f"{instance_key}:{shared_id}:{language}:g{index:04d}",
                instance_key=instance_key,
                shared_id=shared_id,
                language=language,
                file_id=file_id,
                group_index=index,
                title=title,
                paragraph_ids=ids,
                text="\n".join(texts),
                page_start=min(pages) if pages else None,
                page_end=max(pages) if pages else None,
            )
        )
        buffer.clear()

    for paragraph_id, paragraph in numbered_keepable_paragraphs(paragraphs):
        text = str(paragraph["text"]).strip()
        joined = len("\n".join(str(paragraph["text"]).strip() for _, paragraph in buffer))
        if buffer and joined + 1 + len(text) > GROUP_TARGET_CHARS:
            flush()
        buffer.append((paragraph_id, paragraph))
    flush()
    return groups


def sampling_seed(instance_key: str, shared_id: str, language: str) -> str:
    """The per-capture seed string whose draw is documented in about.md."""
    return f"{SEED_PREFIX}/{SAMPLING_SEED}/{instance_key}/{shared_id}/{language}"


def format_group_view(group: PassageGroup, *, all_groups: list[PassageGroup], sampled_ids: set[str]) -> str:
    """Dev view of one passage group plus its neighbors, for triage and manual authoring.

    ``sampled_ids`` marks which groups of the capture appear in
    ``passages.jsonl`` — those are the anchoring targets for manual rows. The
    view still renders a neighbor that is not sampled, so you can read the
    passage in context and decide whether to anchor it (then ask for a merge
    that accepts unsampled groups — or re-anchor to the nearest sampled one).
    """
    total = len(all_groups)
    pages = f"pages {group.page_start}..{group.page_end}" if group.page_start is not None else "no pages"
    heading = f"{group.shared_id} ({group.language}) — {group.title}"
    lines = [
        f"capture : {heading}",
        f"file    : {group.file_id}",
        f"group   : {group.group_id} (g{group.group_index:04d} of {total}) — paragraphs "
        f"{group.paragraph_ids[0]}..{group.paragraph_ids[-1]}, {pages}, {len(group.text)} chars",
    ]
    if group.group_id in sampled_ids:
        lines.append("status  : sampled — valid manual-row anchor; its expected block is in passages.jsonl")
    else:
        sampled_here = sorted(other.group_id.rsplit(":", 1)[-1] for other in all_groups if other.group_id in sampled_ids)
        hint = (
            f"this capture's sampled groups: {', '.join(sampled_here)}"
            if sampled_here
            else "this capture has no sampled groups"
        )
        lines.append(f"status  : NOT sampled — `--merge-manual` only accepts groups listed in passages.jsonl; {hint}")
    lines.append("text    :")
    lines.extend(f"    {line}" for line in group.text.splitlines())
    lines.append("neighbors:")
    for position, label in ((group.group_index - 1, "←"), (group.group_index + 1, "→")):
        if not 0 <= position < total:
            continue
        neighbor = all_groups[position]
        status = "sampled" if neighbor.group_id in sampled_ids else "not sampled"
        preview = " ".join(neighbor.text.split())[:90]
        neighbor_pages = f"page {neighbor.page_start}" if neighbor.page_start is not None else "—"
        lines.append(
            f"  {label} g{neighbor.group_index:04d} ({status}), {neighbor_pages}, {len(neighbor.text)} ch — {preview}"
        )
    return "\n".join(lines)


def sample_groups(
    groups: list[PassageGroup],
    *,
    seed: str,
    per_document: int = GROUPS_PER_DOCUMENT,
    cross_language_ratio: float = CROSS_LANGUAGE_RATIO,
) -> list[tuple[PassageGroup, bool]]:
    """Deterministically pick which groups get questions, and which are cross-language.

    ``random.Random(seed)`` with a fixed draw order — first the group indices
    (sorted), then one flag per sampled group — yields the same selection and
    flags for the same seed. ``cross_language_ratio`` is the per-group
    probability of writing the questions in the other language; ``0.0`` and
    ``1.0`` pin it for tests.
    """
    if per_document < 1:
        raise ValueError(f"per_document must be >= 1, got {per_document}")
    if not 0.0 <= cross_language_ratio <= 1.0:
        raise ValueError(f"cross_language_ratio must be in [0, 1], got {cross_language_ratio}")
    if not groups:
        return []
    rng = random.Random(seed)
    indices = sorted(rng.sample(range(len(groups)), min(per_document, len(groups))))
    sampled = [groups[index] for index in indices]
    flags = [rng.random() < cross_language_ratio for _ in sampled]
    return list(zip(sampled, flags, strict=True))
