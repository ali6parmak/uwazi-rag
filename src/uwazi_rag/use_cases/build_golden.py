"""Step 3.5, dataset half: generate the golden retrieval-eval set.

Questions anchor to paragraphs, never chunk ids: the grouping unit is a
:class:`~uwazi_rag.domain.passage_group.PassageGroup` (see
:mod:`uwazi_rag.use_cases.passage_groups`), so the dataset survives the
chunk-parameter sweeps the scorecard half runs later. Pipeline:

1. cut every capture into passage groups and sample
   ``uwazi_rag.use_cases.passage_groups.GROUPS_PER_DOCUMENT`` per capture with
   a seeded RNG (every document answers; captures are per-language, so
   languages stratify for free)
2. draft 2 questions per sampled group with one LLM call (one specific, one
   broader; for a seeded subset of groups both go in the *other* language)
3. validate (word bounds, no 5-consecutive-word copies from the passage,
   dedup) and stream rows to ``golden.jsonl``

The prompt/parser/validator/row-assembly/manual-merge helpers are pure and
offline-testable; only the orchestration touches the ``LlmPort``. A run ends
in a human-verification prompt — generation never auto-approves its own rows.
"""

from __future__ import annotations

import json
import re
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import IO, Any

from loguru import logger

from uwazi_rag.configuration import EVAL_LANGUAGES
from uwazi_rag.domain.passage_group import PassageGroup
from uwazi_rag.ports.llm_port import LlmPort
from uwazi_rag.use_cases.index_captures import load_captures
from uwazi_rag.use_cases.passage_groups import (
    CROSS_LANGUAGE_RATIO,
    GROUP_TARGET_CHARS,
    GROUPS_PER_DOCUMENT,
    SAMPLING_SEED,
    SEED_PREFIX,
    build_passage_groups,
    sample_groups,
    sampling_seed,
)

GOLDEN_FILE = "golden.jsonl"
MANUAL_FILE = "manual.jsonl"
PASSAGES_FILE = "passages.jsonl"
ABOUT_FILE = "about.md"

# One LLM call per sampled group asks for exactly this many questions.
QUESTIONS_PER_GROUP = 2
# Validator bounds around the prompt's "max ~20 words" instruction.
MIN_QUESTION_WORDS = 3
MAX_QUESTION_WORDS = 24
# The prompt forbids copying 5 consecutive words from the excerpt; re-check
# it offline so compliance does not depend on the model's good will.
COPY_RUN = 5
# Cheap insurance: when a reply is unparseable (garbage, fences mangled), ask
# one more time before counting the group as failed. Adapter errors (HTTP,
# network) are never retried — they abort the run.
PARSE_RETRIES = 1

LANGUAGE_NAMES = {"en": "English", "es": "Spanish"}

# Verbatim prompt shape (settled design; keep the constraints, tune wording).
# Rendered with ``str.format`` — JSON braces doubled.
PROMPT_TEMPLATE = """You are building a search test set. Below is an excerpt from a human-rights document.
Write the questions in: {query_language}
Write 2 questions that a real person might type into a search box, which this excerpt
answers, and which it answers BETTER than other documents would. Rules:
- one very specific question, one broader/vaguer question
- max ~20 words each, natural phrasing
- don't copy 5 consecutive words from the excerpt
- return strict JSON only: [{{"form": "specific", "question": "..."}}, ...]
Excerpt (title removed, just text):
{passage_text}"""

ROW_SCHEMA = (
    "{id, question, origin, query_language, source_group_id, "
    "expected: {instance_key, shared_id, language, file_id, paragraph_ids, text}}"
)

# The manual.jsonl template's example rows anchor to a real sampled group's
# identity for the schema demo (the first usable capture; preferred capture
# may not exist in a given corpus). The question strings are placeholders on
# purpose: origin "example" is never merged, and a realistic-looking question
# would be factually wrong for whatever passage the fallback anchors to.
TEMPLATE_EXAMPLE_SHARED_ID = "64hnagcpvk"
TEMPLATE_EXAMPLE_LANGUAGE = "en"
TEMPLATE_QUESTIONS: tuple[tuple[str, str], ...] = (
    ("en", "TODO replace me — one very specific question about this passage's concrete facts"),
    ("es", "TODO replace me — one broader question that still only this passage answers best (cross-language example)"),
)


def build_generation_prompt(group: PassageGroup, query_language: str) -> str:
    """The verbatim generation prompt for one passage group.

    ``query_language`` is rendered with its human name when known; the excerpt
    is the group text — paragraph text only, never the title or page furniture.
    """
    named = LANGUAGE_NAMES.get(query_language, query_language)
    return PROMPT_TEMPLATE.format(query_language=named, passage_text=group.text)


def parse_question_list(raw: str) -> list[str]:
    """Parse a model reply into question strings, order preserved.

    Expects a strict JSON array of ``{"form": …, "question": …}`` objects;
    tolerates a single ````` … ```` ``` ```` code fence (models like to wrap
    JSON). Items without a non-empty ``question`` string are skipped; an array
    with none of those is a parse failure. Raises ``ValueError`` otherwise —
    the caller counts it as one failed group.
    """
    if not raw or not raw.strip():
        raise ValueError("the model returned an empty reply")
    candidate = raw.strip()
    if candidate.startswith("```"):
        match = re.search(r"```[a-zA-Z0-9]*\n(.*)\n?```", candidate, flags=re.DOTALL)
        if not match:
            raise ValueError("reply looked like a code fence but contained none to close")
        candidate = match.group(1)
    try:
        payload = json.loads(candidate)
    except json.JSONDecodeError as error:
        raise ValueError(f"reply is not valid JSON ({error})") from error
    if not isinstance(payload, list):
        raise ValueError("reply JSON is not an array")
    questions = [
        item["question"]
        for item in payload
        if isinstance(item, dict) and isinstance(item.get("question"), str) and item["question"].strip()
    ]
    if not questions:
        raise ValueError("reply JSON array had no objects with a non-empty 'question'")
    return questions


def question_tokens(text: str) -> list[str]:
    """Lower-cased word tokens — unicode-aware, so Spanish accents group correctly."""
    return re.findall(r"\w+", text.lower())


def copy_run_violation(question: str, passage: str, run: int = COPY_RUN) -> bool:
    """True when the question copies consecutive words from the passage.

    Two shapes are rejected: any ``run``-word window of the question appearing
    as a consecutive run in the passage, and — for questions shorter than
    ``run`` — the whole question being one verbatim passage fragment (a
    3-word question that quotes the passage is still a copy).
    """
    question_words = question_tokens(question)
    if not question_words:
        return False
    passage_words = question_tokens(passage)
    window = min(len(question_words), run)
    passage_runs = {" ".join(passage_words[start : start + window]) for start in range(len(passage_words) - window + 1)}
    return any(
        " ".join(question_words[start : start + window]) in passage_runs for start in range(len(question_words) - window + 1)
    )


def question_problem(question: str, passage: str) -> str | None:
    """None when a draft question is acceptable, else the reason it is rejected."""
    if not question or not question.strip():
        return "empty"
    words = question_tokens(question)
    if len(words) < MIN_QUESTION_WORDS:
        return "too_short"
    if len(words) > MAX_QUESTION_WORDS:
        return "too_long"
    if copy_run_violation(question, passage):
        return "copied_from_passage"
    return None


def normalized_question(question: str) -> str:
    """Dedup key: token sequence, with case and punctuation folded away."""
    return " ".join(question_tokens(question))


def select_questions(
    candidates: list[str], *, passage: str, limit: int = QUESTIONS_PER_GROUP
) -> tuple[list[str], list[str]]:
    """Validate one group's draft questions and keep at most ``limit`` (pure).

    Returns ``(kept, rejection_reasons)`` — ``"duplicate"`` in the reasons
    marks questions already asked by this group (counted as deduped, not
    invalid).
    """
    kept: list[str] = []
    reasons: list[str] = []
    seen: list[str] = []
    for question in candidates:
        if len(kept) >= limit:
            reasons.append("beyond_limit")
            continue
        problem = question_problem(question, passage)
        if problem:
            reasons.append(problem)
            continue
        key = normalized_question(question)
        if key in seen:
            reasons.append("duplicate")
            continue
        seen.append(key)
        kept.append(question)
    return kept, reasons


def other_language(language: str, eval_languages: Sequence[str]) -> str | None:
    """The other configured language for cross-language questions, if defined.

    ``None`` means stay in the capture's own language (the language is not in
    ``eval_languages``, or the config does not name exactly two languages).
    """
    if language not in eval_languages or len(set(eval_languages)) != 2:
        return None
    return next(code for code in eval_languages if code != language)


def make_golden_rows(
    group: PassageGroup, questions: list[str], *, query_language: str, origin: str = "synthetic"
) -> list[dict[str, Any]]:
    """Assemble golden rows in the schema every downstream consumer relies on.

    ``query_language`` is the language the questions were written in;
    ``expected.language`` stays the capture's language (they differ exactly on
    cross-language rows). Key order matches ``ROW_SCHEMA``.
    """
    return [
        {
            "id": f"{group.group_id}:q{position}",
            "question": question,
            "origin": origin,
            "query_language": query_language,
            "source_group_id": group.group_id,
            "expected": {
                "instance_key": group.instance_key,
                "shared_id": group.shared_id,
                "language": group.language,
                "file_id": group.file_id,
                "paragraph_ids": list(group.paragraph_ids),
                "text": group.text,
            },
        }
        for position, question in enumerate(questions, start=1)
    ]


@dataclass
class GoldenStats:
    """What one ``build_golden_dataset`` run did (for the CLI's report)."""

    captures_seen: int = 0
    captures_used: int = 0
    skipped_not_ready: int = 0
    skipped_no_groups: int = 0
    groups_total: int = 0
    groups_sampled: int = 0
    groups_generated: int = 0
    groups_failed: int = 0
    cross_language_groups: int = 0
    rows_written: int = 0
    rows_deduped: int = 0
    rows_invalid: int = 0
    failures: list[str] = field(default_factory=list)
    outputs: list[str] = field(default_factory=list)
    plan_lines: list[str] = field(default_factory=list)


def draft_questions(llm: LlmPort, prompt: str) -> list[str]:
    """One LLM call (+ ``PARSE_RETRIES`` on unparseable replies), questions out.

    Adapter errors propagate: a dead service must abort the run, not burn the
    remaining calls. A permanently unparseable reply becomes a ``RuntimeError``
    and the caller counts the group as failed.
    """
    problem: str | None = None
    reply = ""
    for _ in range(1 + PARSE_RETRIES):
        reply = llm.chat([{"role": "user", "content": prompt}])
        try:
            return parse_question_list(reply)
        except ValueError as error:
            problem = str(error)
    raise RuntimeError(f"unparseable reply (twice): {problem} — reply started {reply[:120]!r}")


def template_groups(captures: list[dict]) -> tuple[PassageGroup, PassageGroup] | None:
    """Two example groups for the ``manual.jsonl`` template, or None without usable captures.

    Prefers the capture the template questions were written against
    (:data:`TEMPLATE_EXAMPLE_SHARED_ID`), else the first usable one — in the
    fallback the example questions may read off-topic, which is harmless for a
    never-merged schema demo.
    """
    preferred: tuple[dict, list[PassageGroup]] | None = None
    first: tuple[dict, list[PassageGroup]] | None = None
    for capture in captures:
        if capture.get("segmentation_status") != "ready":
            continue
        file_id = (capture.get("file") or {}).get("id")
        if not file_id:
            continue
        groups = build_passage_groups(
            capture.get("paragraphs") or [],
            instance_key=str(capture.get("instance_key") or ""),
            shared_id=str(capture.get("shared_id") or ""),
            language=str(capture.get("language") or ""),
            file_id=str(file_id),
            title=str(capture.get("title") or ""),
        )
        if not groups:
            continue
        if first is None:
            first = (capture, groups)
        if capture.get("shared_id") == TEMPLATE_EXAMPLE_SHARED_ID and capture.get("language") == TEMPLATE_EXAMPLE_LANGUAGE:
            preferred = (capture, groups)
            break
    chosen = preferred or first
    if chosen is None:
        return None
    _, chosen_groups = chosen
    return chosen_groups[0], chosen_groups[min(1, len(chosen_groups) - 1)]


def build_manual_template(same: PassageGroup, cross: PassageGroup) -> list[dict[str, Any]]:
    """The 2 example rows — complete schema, ``origin: "example"``, never merged."""
    first_row = make_golden_rows(
        same, [TEMPLATE_QUESTIONS[0][1]], query_language=TEMPLATE_QUESTIONS[0][0], origin="example"
    )[0]
    first_row["id"] = "template-1"
    second_row = make_golden_rows(
        cross, [TEMPLATE_QUESTIONS[1][1]], query_language=TEMPLATE_QUESTIONS[1][0], origin="example"
    )[0]
    second_row["id"] = "template-2"
    return [first_row, second_row]


def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    """One compact JSON object per line, non-ASCII kept as-is (git diffs stay readable)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as stream:
        for row in rows:
            stream.write(json.dumps(row, ensure_ascii=False) + "\n")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    """Parse a JSONL file, naming the line in every error; blank lines ignored."""
    rows: list[dict[str, Any]] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as error:
            raise ValueError(f"{path.name} line {number}: not valid JSON ({error})") from error
        if not isinstance(value, dict):
            raise ValueError(f"{path.name} line {number}: expected a JSON object")
        rows.append(value)
    return rows


@dataclass
class CapturePlan:
    """One capture's sampled plan — shared by generation, dry-run and passages-only."""

    name: str
    capture: dict
    groups: list[PassageGroup]
    plan: list[tuple[PassageGroup, bool]]


def _collect_plans(
    captures: list[dict], *, samples_per_document: int, cross_language_ratio: float, failures: list[str]
) -> tuple[list[CapturePlan], int, int]:
    """Walk captures → per-capture sampled plans (pure, offline).

    Skips (and counts) captures that are not ``ready``, lack a file id (reason
    appended to ``failures``) or yield no keepable text; the walk is stable
    because ready segmentations never change.
    """
    plans: list[CapturePlan] = []
    skipped_not_ready = 0
    skipped_no_groups = 0
    for capture in captures:
        name = f"{capture['shared_id']}_{capture['language']}"
        if capture.get("segmentation_status") != "ready":
            skipped_not_ready += 1
            continue
        file_id = (capture.get("file") or {}).get("id")
        if not file_id:
            skipped_no_groups += 1
            failures.append(f"{name}: capture has no file id (skipped)")
            continue
        groups = build_passage_groups(
            capture["paragraphs"],
            instance_key=capture["instance_key"],
            shared_id=capture["shared_id"],
            language=capture["language"],
            file_id=str(file_id),
            title=capture["title"],
        )
        if not groups:
            skipped_no_groups += 1
            continue
        plan = sample_groups(
            groups,
            seed=sampling_seed(capture["instance_key"], capture["shared_id"], capture["language"]),
            per_document=samples_per_document,
            cross_language_ratio=cross_language_ratio,
        )
        plans.append(CapturePlan(name=name, capture=capture, groups=groups, plan=plan))
    return plans, skipped_not_ready, skipped_no_groups


def build_golden_dataset(
    *,
    raw_dir: Path,
    llm: LlmPort,
    output_dir: Path,
    samples_per_document: int = GROUPS_PER_DOCUMENT,
    limit: int | None = None,
    cross_language_ratio: float = CROSS_LANGUAGE_RATIO,
    eval_languages: Sequence[str] = EVAL_LANGUAGES,
    llm_description: str = "",
    dry_run: bool = False,
) -> GoldenStats:
    """Generate the golden dataset (PLAN.md Step 3.5, dataset half).

    Drafts questions for every sampled passage group, validates and dedups
    them, and writes ``golden.jsonl`` / ``passages.jsonl`` / ``about.md`` (and
    the ``manual.jsonl`` template when absent). Single-group failures are
    counted and skipped, never fatal; adapter errors abort the whole run. Rows
    stream to a temp file renamed on completion, so a killed run never
    corrupts the previous dataset. ``dry_run`` prints the plan only.
    """
    if samples_per_document < 1:
        raise ValueError(f"samples_per_document must be >= 1, got {samples_per_document}")
    if limit is not None and limit < 1:
        raise ValueError(f"limit must be >= 1, got {limit}")
    captures = load_captures(raw_dir)
    if limit is not None:
        captures = captures[:limit]

    stats = GoldenStats(captures_seen=len(captures))
    golden_stream: IO[str] | None = None
    sampled_passages: list[PassageGroup] = []
    seen_questions: set[str] = set()
    golden_tmp = output_dir / f"{GOLDEN_FILE}.tmp"
    if not dry_run:
        output_dir.mkdir(parents=True, exist_ok=True)
        golden_stream = golden_tmp.open("w", encoding="utf-8")

    plans, skipped_not_ready, skipped_no_groups = _collect_plans(
        captures,
        samples_per_document=samples_per_document,
        cross_language_ratio=cross_language_ratio,
        failures=stats.failures,
    )
    stats.skipped_not_ready = skipped_not_ready
    stats.skipped_no_groups = skipped_no_groups

    for capture_plan in plans:
        stats.captures_used += 1
        stats.groups_total += len(capture_plan.groups)
        stats.groups_sampled += len(capture_plan.plan)
        if not dry_run:
            sampled_passages.extend(group for group, _ in capture_plan.plan)
            logger.info(
                f"golden: {capture_plan.name} — {len(capture_plan.groups)} groups, sampling {len(capture_plan.plan)}"
            )
        if dry_run:
            stats.plan_lines.append(
                _describe_group_plan(capture_plan.name, len(capture_plan.groups), capture_plan.plan, eval_languages)
            )
            continue

        for group, cross_language in capture_plan.plan:
            swap = other_language(group.language, eval_languages) if cross_language else None
            query_language = swap or group.language
            if query_language != group.language:
                stats.cross_language_groups += 1
            try:
                drafts = draft_questions(llm, build_generation_prompt(group, query_language))
            except RuntimeError as error:
                stats.groups_failed += 1
                stats.failures.append(f"{group.group_id}: {error}")
                continue
            kept, reasons = select_questions(drafts, passage=group.text)
            stats.rows_deduped += sum(1 for reason in reasons if reason == "duplicate")
            stats.rows_invalid += sum(1 for reason in reasons if reason != "duplicate")
            fresh = _add_rows(
                make_golden_rows(group, kept, query_language=query_language),
                stream=golden_stream,
                seen_questions=seen_questions,
                stats=stats,
            )
            if fresh == 0:
                stats.groups_failed += 1
                reason = ", ".join(sorted(set(reasons))) or "every question duplicated an earlier group"
                stats.failures.append(f"{group.group_id}: no usable questions ({reason})")
            else:
                stats.groups_generated += 1
                stats.rows_written += fresh

    if dry_run:
        return stats

    assert golden_stream is not None  # guaranteed above unless dry_run
    golden_stream.close()
    golden_path = output_dir / GOLDEN_FILE
    golden_tmp.replace(golden_path)
    stats.outputs.append(str(golden_path))

    passages_path = output_dir / PASSAGES_FILE
    write_jsonl(passages_path, [group.model_dump() for group in sampled_passages])
    stats.outputs.append(str(passages_path))

    about_path = output_dir / ABOUT_FILE
    about_path.write_text(
        format_about(
            stats,
            llm_description=llm_description,
            samples_per_document=samples_per_document,
            cross_language_ratio=cross_language_ratio,
            eval_languages=eval_languages,
        ),
        encoding="utf-8",
    )
    stats.outputs.append(str(about_path))

    template = template_groups(captures)
    manual_path = output_dir / MANUAL_FILE
    if template and not manual_path.exists():
        write_jsonl(manual_path, build_manual_template(*template))
        stats.outputs.append(str(manual_path))
    return stats


def write_passages_file(
    *,
    raw_dir: Path,
    output_dir: Path,
    samples_per_document: int = GROUPS_PER_DOCUMENT,
    limit: int | None = None,
    cross_language_ratio: float = CROSS_LANGUAGE_RATIO,
) -> GoldenStats:
    """Recreate ``passages.jsonl`` offline — the sampled groups, no LLM calls.

    Deterministic: same seed and walk as a full run, so the file matches what
    a real generation would consult (byte-for-byte). Useful when the
    gitignored review file is lost or stale, without re-drafting questions.
    """
    if samples_per_document < 1:
        raise ValueError(f"samples_per_document must be >= 1, got {samples_per_document}")
    if limit is not None and limit < 1:
        raise ValueError(f"limit must be >= 1, got {limit}")
    captures = load_captures(raw_dir)
    if limit is not None:
        captures = captures[:limit]
    stats = GoldenStats(captures_seen=len(captures))
    plans, skipped_not_ready, skipped_no_groups = _collect_plans(
        captures,
        samples_per_document=samples_per_document,
        cross_language_ratio=cross_language_ratio,
        failures=stats.failures,
    )
    stats.skipped_not_ready = skipped_not_ready
    stats.skipped_no_groups = skipped_no_groups
    stats.captures_used = len(plans)
    stats.groups_total = sum(len(capture_plan.groups) for capture_plan in plans)
    groups_all = [group for capture_plan in plans for group, _ in capture_plan.plan]
    stats.groups_sampled = len(groups_all)
    passages_path = output_dir / PASSAGES_FILE
    write_jsonl(passages_path, [group.model_dump() for group in groups_all])
    stats.outputs.append(str(passages_path))
    return stats


def _add_rows(
    rows: list[dict[str, Any]],
    *,
    stream: IO[str] | None,
    seen_questions: set[str],
    stats: GoldenStats,
) -> int:
    """Write non-duplicate rows (cross-group dedup), returning how many survived."""
    fresh = 0
    for row in rows:
        key = normalized_question(str(row["question"]))
        if key in seen_questions:
            stats.rows_deduped += 1
            continue
        seen_questions.add(key)
        if stream is not None:
            stream.write(json.dumps(row, ensure_ascii=False) + "\n")
        fresh += 1
    return fresh


def _describe_group_plan(
    name: str, groups_total: int, plan: list[tuple[PassageGroup, bool]], eval_languages: Sequence[str]
) -> str:
    """One dry-run line: which groups would get questions, sizes, cross picks."""
    parts: list[str] = []
    for group, cross in plan:
        query = (other_language(group.language, eval_languages) if cross else None) or group.language
        parts.append(
            f"{group.group_id.rsplit(':', 1)[-1]} ({len(group.text)} ch, paras "
            f"{group.paragraph_ids[0]}..{group.paragraph_ids[-1]}"
            + (f", {group.language}→{query})" if query != group.language else ", same language)")
        )
    return f"{name}: {groups_total} groups → sampled: {', '.join(parts)}"


def format_about(
    stats: GoldenStats,
    *,
    llm_description: str,
    samples_per_document: int,
    cross_language_ratio: float,
    eval_languages: Sequence[str],
) -> str:
    """The recipe for this dataset — enough to reproduce or audit the run."""
    generated_on = datetime.now(timezone.utc).date().isoformat()
    parts: list[str] = [
        "# Golden dataset — generation recipe",
        "",
        f"Generated {generated_on} by `uwazi-rag build-golden`.",
        "",
        "## Model",
        "",
        f"- LLM: {llm_description or 'not recorded'}",
        "- Ollama defaults (no temperature or options set on the request); non-streaming chat.",
        "",
        "## Grouping rule (fixed, independent of the chunker)",
        "",
        f"- unit: consecutive keepable paragraphs (the chunker's drop rule) packed to ≤ {GROUP_TARGET_CHARS} chars;",
        "  a single longer paragraph is its own (unsplittable) group",
        "- anchor: `paragraph_ids` are 0-based positions in the raw capture (dropped paragraphs leave gaps);",
        "  the scorecard maps them to chunks by re-chunking, so the dataset survives any chunk config",
        "",
        "## Sampling rule",
        "",
        f"- {samples_per_document} passage groups per capture, every capture answers; captures are",
        "  per-language, so languages stratify for free",
        f'- seed: `"{SEED_PREFIX}/{SAMPLING_SEED}/<instance_key>/<shared_id>/<language>"`, fixed draw order',
        "  (group indices, then one cross-language flag per sampled group) — a re-run selects the same groups",
        f"- cross-language: a seeded {cross_language_ratio:.0%} subset of sampled groups gets its questions",
        f"  generated in the other configured language ({', '.join(eval_languages)}),",
        "  i.e. query_language ≠ expected.language",
        "",
        "## Counts",
        "",
        "| | |",
        "|---|---|",
        f"| captures seen / used | {stats.captures_seen} / {stats.captures_used} |",
        f"| captures skipped (not ready / no groups) | {stats.skipped_not_ready} / {stats.skipped_no_groups} |",
        f"| passage groups built / sampled | {stats.groups_total} / {stats.groups_sampled} |",
        f"| cross-language groups | {stats.cross_language_groups} |",
        f"| groups generated / failed | {stats.groups_generated} / {stats.groups_failed} |",
        f"| rows written | {stats.rows_written} |",
        f"| rows deduped / rejected | {stats.rows_deduped} / {stats.rows_invalid} |",
        "",
    ]
    if stats.failures:
        parts.append("## Failures (groups skipped during generation)")
        parts.append("")
        parts.extend(f"- {reason}" for reason in stats.failures)
        parts.append("")
    parts.extend(
        [
            "## Question-generation prompt (verbatim)",
            "",
            "```text",
            PROMPT_TEMPLATE,
            "```",
            "",
            "## Row schema",
            "",
            f"`{ROW_SCHEMA}`",
            "",
            "- `origin`: `synthetic` (LLM-drafted) or `manual` (hand-written, merged via",
            "  `uwazi-rag build-golden --merge-manual`).",
            "- unanswerable manual rows (a real topic the corpus does not contain) carry",
            '  `"source_group_id": null, "expected": null`; the scorecard expects nothing relevant for them.',
            "- `manual.jsonl` starts as an origin-example schema template; the reviewed dataset",
            "  has human-written `manual` rows in its place.",
            "- `passages.jsonl` holds the sampled groups (ground truth for review; paragraph ids indexed",
            f"  as above) and is derived/disposable, so it is gitignored. `{GOLDEN_FILE}`, `{MANUAL_FILE}`,",
            f"  `{ABOUT_FILE}` are committed.",
        ]
    )
    return "\n".join(parts) + "\n"


REVIEW_GUIDE = """\
STOP here — human verification is the next step:
1. Triage the draft rows in golden.jsonl. Ground truth for each question is its passage in
   passages.jsonl (join on source_group_id) — open one in context with
   `uv run uwazi-rag show-group <group_id>`. Delete junk — watch for:
   - questions that talk about "this document/excerpt" (the model never saw a document)
   - questions the whole corpus answers equally well (nothing makes this passage best)
   - questions copying 5+ consecutive words from the passage
   - yes/no questions, or questions about the document's metadata rather than its text
2. Hand-write your ~15-20 rows in manual.jsonl (replace the two template rows; keep
   origin "manual"; copy each expected block from passages.jsonl). Cover:
   - exact keyword / article-number / date queries
   - paraphrases with NO wording overlap with the passage (anti self-echo)
   - cross-language questions (query_language different from expected.language)
   - broad topical queries a human would really type
   - near-duplicate fact pairs across documents (does retrieval discriminate?)
   - 2-3 questions with no good answer in the corpus, carrying null for both
     source_group_id and expected (the scorecard expects no relevant hits)
3. `uv run uwazi-rag build-golden --merge-manual` validates + appends your rows to golden.jsonl.
4. Commit golden.jsonl, manual.jsonl and about.md (passages.jsonl stays untracked)."""


def describe_run(stats: GoldenStats) -> str:
    """The end-of-run report: stats, file paths, then the verification guide."""
    lines = [
        f"captures : {stats.captures_used}/{stats.captures_seen} used — "
        f"{stats.skipped_not_ready} not ready, {stats.skipped_no_groups} without keepable text",
        f"passages : {stats.groups_total} groups built — {stats.groups_sampled} sampled, "
        f"{stats.cross_language_groups} cross-language",
        f"questions: {stats.rows_written} written — {stats.rows_deduped} deduped, {stats.rows_invalid} rejected, "
        f"{stats.groups_failed} groups failed",
    ]
    if stats.failures:
        shown = stats.failures[:10]
        lines.extend(f"  ! {reason}" for reason in shown)
        if len(stats.failures) > len(shown):
            lines.append(f"  … and {len(stats.failures) - len(shown)} more failures")
    lines.append("wrote    : " + "; ".join(stats.outputs or ["(nothing)"]))
    lines.append("")
    lines.append(REVIEW_GUIDE)
    return "\n".join(lines)


@dataclass
class MergeStats:
    """What one ``merge_manual_rows`` run did."""

    golden_rows_before: int
    golden_rows_after: int
    manual_rows_read: int
    manual_rows_merged: int
    manual_rows_skipped_duplicated: int
    example_rows_skipped: int
    ids_autoassigned: int


def merge_manual_rows(*, eval_dir: Path, eval_languages: Sequence[str] = EVAL_LANGUAGES) -> MergeStats:
    """Validate hand-written rows in ``manual.jsonl`` and append them to ``golden.jsonl``.

    Merge-only: no LLM calls. Every ``origin: "manual"`` row must reference a
    ``source_group_id`` that exists in ``passages.jsonl`` and copy that
    group's ``expected`` block exactly; missing ids are auto-assigned
    ``m<NNN>``. Unanswerable rows (``source_group_id`` and ``expected`` both
    ``None``) need no passage anchor. ``origin: "example"`` template rows are
    skipped with a count; any other problem aborts the merge before the
    golden file is touched.
    """
    golden_path = eval_dir / GOLDEN_FILE
    manual_path = eval_dir / MANUAL_FILE
    passages_path = eval_dir / PASSAGES_FILE
    for path in (golden_path, manual_path, passages_path):
        if not path.exists():
            raise FileNotFoundError(f"{path} is missing — generate the dataset with `uwazi-rag build-golden` first")
    golden = read_jsonl(golden_path)
    passages_rows = read_jsonl(passages_path)
    manual = read_jsonl(manual_path)
    passages: dict[str, dict[str, Any]] = {}
    for row in passages_rows:
        group_id = str(row.get("group_id") or "")
        if not group_id:
            raise ValueError(f"{PASSAGES_FILE}: a row has no group_id")
        if group_id in passages:
            raise ValueError(f"{PASSAGES_FILE}: group_id {group_id!r} appears twice")
        passages[group_id] = row

    taken = {str(row["id"]) for row in golden if row.get("id")}
    golden_questions = {normalized_question(str(row.get("question") or "")) for row in golden}
    validated: list[dict[str, Any]] = []
    example_rows_skipped = 0
    manual_rows_skipped_duplicated = 0
    manual_rows_read = len(manual)
    for number, row in enumerate(manual, start=1):
        if row.get("origin") == "example":
            example_rows_skipped += 1
            continue
        problem = _manual_row_problem(row, passages=passages, taken=taken, eval_languages=eval_languages)
        if problem:
            raise ValueError(f"{MANUAL_FILE} line {number}: {problem}")
        if normalized_question(str(row["question"])) in golden_questions:
            # already merged by an earlier run — manual.jsonl is append-friendly
            manual_rows_skipped_duplicated += 1
            continue
        if row.get("id"):
            taken.add(str(row["id"]))
        validated.append(row)

    merged: list[dict[str, Any]] = [*golden]
    ids_autoassigned = 0
    auto = 0
    for row in validated:
        if not row.get("id"):
            while True:
                auto += 1
                candidate = f"m{auto:03d}"
                if candidate not in taken:
                    break
            row = {**row, "id": candidate}
            ids_autoassigned += 1
        merged.append(row)

    tmp = eval_dir / f"{GOLDEN_FILE}.tmp"
    write_jsonl(tmp, merged)
    tmp.replace(golden_path)
    return MergeStats(
        golden_rows_before=len(golden),
        golden_rows_after=len(merged),
        manual_rows_read=manual_rows_read,
        manual_rows_merged=len(validated),
        manual_rows_skipped_duplicated=manual_rows_skipped_duplicated,
        example_rows_skipped=example_rows_skipped,
        ids_autoassigned=ids_autoassigned,
    )


def _manual_row_problem(
    row: dict[str, Any], *, passages: dict[str, dict[str, Any]], taken: set[str], eval_languages: Sequence[str]
) -> str | None:
    """Why a hand-written row cannot merge (None = mergeable), message names the fix."""
    if row.get("origin") != "manual":
        return f"origin must be 'manual' (row has {row.get('origin')!r})"
    question = row.get("question")
    if not isinstance(question, str) or not question.strip():
        return "question must be a non-empty string"
    query_language = row.get("query_language")
    if not isinstance(query_language, str) or query_language not in eval_languages:
        return f"query_language must be one of {', '.join(eval_languages)}"
    source_group_id = row.get("source_group_id")
    if source_group_id is None and row.get("expected") is None:
        # Unanswerable row: a real topic the corpus does not contain — no anchor
        # exists, so the scorecard later expects nothing relevant to come back.
        return None
    if (source_group_id is None) != (row.get("expected") is None):
        return "an unanswerable row needs source_group_id and expected to be null together, or neither of them null"
    if not isinstance(source_group_id, str) or not source_group_id:
        return "source_group_id must be a non-empty string"
    passage = passages.get(source_group_id)
    if passage is None:
        return f"source_group_id {source_group_id!r} is not in {PASSAGES_FILE}"
    expected = row.get("expected")
    if not isinstance(expected, dict):
        return "expected must be an object copied from passages.jsonl"
    for name, want in (
        ("instance_key", passage["instance_key"]),
        ("shared_id", passage["shared_id"]),
        ("language", passage["language"]),
        ("file_id", passage["file_id"]),
        ("paragraph_ids", passage["paragraph_ids"]),
        ("text", passage["text"]),
    ):
        if expected.get(name) != want:
            return f"expected.{name} does not match passage {source_group_id!r} — copy the block from {PASSAGES_FILE}"
    row_id = row.get("id")
    if row_id is not None and (not isinstance(row_id, str) or not row_id.strip()):
        return "id, when present, must be a non-empty string"
    if isinstance(row_id, str) and row_id in taken:
        return f"id {row_id!r} is already used — ids must be unique"
    return None
