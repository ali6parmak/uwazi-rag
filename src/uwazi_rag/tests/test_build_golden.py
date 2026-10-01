"""Step 3.5 tests: golden-set generation + manual merge, offline.

Orchestration runs against the committed real captures through the tests'
deterministic :class:`EchoJsonLlm` (the ``HashingEmbedding`` equivalent for
chats); the prompt/parser/validator/row/merge helpers are exercised directly
as pure functions (AGENTS.md testing policy).
"""

import json
from pathlib import Path
from typing import Any

import pytest

from uwazi_rag.configuration import FIXTURES_DIR
from uwazi_rag.ports.llm_port import LlmPort
from uwazi_rag.tests.echo_llm import (
    DuplicateJsonLlm,
    EchoJsonLlm,
    EmptyListLlm,
    FlakyJsonLlm,
    GarbageJsonLlm,
)
from uwazi_rag.use_cases.build_golden import (
    GOLDEN_FILE,
    MANUAL_FILE,
    PASSAGES_FILE,
    TEMPLATE_QUESTIONS,
    build_generation_prompt,
    build_golden_dataset,
    build_manual_template,
    copy_run_violation,
    make_golden_rows,
    merge_manual_rows,
    other_language,
    parse_question_list,
    question_problem,
    read_jsonl,
    select_questions,
    write_jsonl,
    write_passages_file,
)
from uwazi_rag.use_cases.passage_groups import (
    build_passage_groups,
    sample_groups,
    sampling_seed,
)

FIXTURES = ["64hnagcpvk_en.json", "ar22d4v4i5s_en.json", "ar22d4v4i5s_es.json"]
GOLD_SCHEMA = ["id", "question", "origin", "query_language", "source_group_id", "expected"]
EXPECTED_SCHEMA = ["instance_key", "shared_id", "language", "file_id", "paragraph_ids", "text"]
PASSAGE_SCHEMA = [
    "group_id",
    "instance_key",
    "shared_id",
    "language",
    "file_id",
    "group_index",
    "title",
    "paragraph_ids",
    "text",
    "page_start",
    "page_end",
]


def _capture(name: str) -> dict:
    capture: dict = json.loads((FIXTURES_DIR / name).read_text(encoding="utf-8"))
    return capture


def _capture_dir(tmp_path: Path, names: list[str]) -> Path:
    raw_dir = tmp_path / "raw" / "bdd5a7c445847b35"
    raw_dir.mkdir(parents=True, exist_ok=True)
    for name in names:
        capture = _capture(name)
        (raw_dir / f"{capture['shared_id']}_{capture['language']}.json").write_text(
            json.dumps(capture, ensure_ascii=False), encoding="utf-8"
        )
    return raw_dir


def _run(tmp_path: Path, names: list[str], llm: LlmPort | None = None, **kwargs: Any) -> tuple[Any, Path]:
    """One full generation run over real fixtures, into a fresh eval dir."""
    eval_dir = tmp_path / "eval"
    stats = build_golden_dataset(
        raw_dir=_capture_dir(tmp_path, names),
        llm=llm or EchoJsonLlm(),
        output_dir=eval_dir,
        llm_description="test LLM",
        **kwargs,
    )
    return stats, eval_dir


def _jsonl(eval_dir: Path, name: str) -> list[dict[str, Any]]:
    return read_jsonl(eval_dir / name)


# --- generation (orchestrator, offline via EchoJsonLlm) -----------------------


def test_generation_writes_the_full_dataset_from_real_fixtures(tmp_path: Path) -> None:
    stats, eval_dir = _run(tmp_path, FIXTURES)

    assert stats.captures_used == 3
    assert stats.skipped_not_ready == 0 and stats.skipped_no_groups == 0
    assert stats.groups_sampled == 6
    assert stats.groups_generated == 6 and stats.groups_failed == 0
    # the orchestrator must draw exactly what the documented sampling rule draws
    expected_cross = 0
    for name in FIXTURES:
        capture = _capture(name)
        groups = build_passage_groups(
            capture["paragraphs"],
            instance_key=capture["instance_key"],
            shared_id=capture["shared_id"],
            language=capture["language"],
            file_id=capture["file"]["id"],
            title=capture["title"],
        )
        plan = sample_groups(groups, seed=sampling_seed(capture["instance_key"], capture["shared_id"], capture["language"]))
        expected_cross += sum(1 for group, cross in plan if cross and other_language(group.language, "en,es".split(",")))
    assert stats.cross_language_groups == expected_cross
    assert stats.rows_written == 12  # EchoJsonLlm always yields 2 validator-passing questions

    golden = _jsonl(eval_dir, GOLDEN_FILE)
    assert len(golden) == stats.rows_written
    first = golden[0]  # load_captures sorts 64hnagcpvk_en first; the seeded draw picked g0002
    assert list(first) == GOLD_SCHEMA
    assert list(first["expected"]) == EXPECTED_SCHEMA
    assert first["origin"] == "synthetic"
    assert first["source_group_id"].startswith(f"{_capture(FIXTURES[0])['instance_key']}:64hnagcpvk:en:g")
    assert first["id"] == f"{first['source_group_id']}:q1"
    assert first["query_language"] == "en" == first["expected"]["language"]

    passages = _jsonl(eval_dir, PASSAGES_FILE)
    assert len(passages) == 6
    texts = {row["group_id"]: row["text"] for row in passages}
    for row in golden:
        assert row["expected"]["text"] == texts[row["source_group_id"]]
    for passage in passages:
        assert list(passage) == PASSAGE_SCHEMA

    manual = _jsonl(eval_dir, MANUAL_FILE)
    assert [row["id"] for row in manual] == ["template-1", "template-2"]
    assert all(row["origin"] == "example" for row in manual)

    about = (eval_dir / "about.md").read_text(encoding="utf-8")
    assert "test LLM" in about and "20261001" in about and "25%" in about
    assert "don't copy 5 consecutive words from the excerpt" in about
    assert "en, es" in about
    assert list(eval_dir.glob("*.tmp")) == []  # only final files remain


def test_cross_language_groups_ask_in_the_other_language(tmp_path: Path) -> None:
    stats, eval_dir = _run(tmp_path, ["ar22d4v4i5s_en.json", "ar22d4v4i5s_es.json"], cross_language_ratio=1.0)

    assert stats.cross_language_groups == stats.groups_sampled > 0
    for row in _jsonl(eval_dir, GOLDEN_FILE):
        expected_language = row["expected"]["language"]
        assert row["query_language"] == ("es" if expected_language == "en" else "en")


def test_dry_run_prints_a_plan_without_files_or_llm_calls(tmp_path: Path) -> None:
    stats, eval_dir = _run(tmp_path, ["64hnagcpvk_en.json"], llm=GarbageJsonLlm(), dry_run=True)

    assert stats.captures_used == 1
    assert stats.groups_sampled == 2
    assert stats.rows_written == 0 and stats.groups_failed == 0  # no LLM calls were made
    assert stats.plan_lines and "g000" in stats.plan_lines[0]
    assert not eval_dir.exists()  # nothing written at all


def test_garbage_replies_fail_their_group_but_the_run_survives(tmp_path: Path) -> None:
    stats, eval_dir = _run(tmp_path, ["64hnagcpvk_en.json"], llm=GarbageJsonLlm())

    assert stats.rows_written == 0
    assert stats.groups_failed == stats.groups_sampled
    assert "unparseable reply" in stats.failures[0]
    assert (eval_dir / GOLDEN_FILE).exists()  # the (empty) draft is still written
    assert _jsonl(eval_dir, PASSAGES_FILE)  # ground truth survives for review


def test_unparseable_reply_gets_one_retry_before_failing(tmp_path: Path) -> None:
    flaky = FlakyJsonLlm()
    stats, _ = _run(tmp_path, ["64hnagcpvk_en.json"], llm=flaky)

    assert flaky.calls == 2 * stats.groups_sampled  # every group needed its retry
    assert stats.groups_generated == stats.groups_sampled
    assert stats.rows_written == 2 * stats.groups_sampled


def test_question_less_replies_fail_their_group_with_a_reason(tmp_path: Path) -> None:
    stats, _ = _run(tmp_path, ["64hnagcpvk_en.json"], llm=EmptyListLlm())

    assert stats.groups_failed == stats.groups_sampled
    assert any("non-empty 'question'" in failure for failure in stats.failures)


def test_within_group_duplicates_count_as_deduped(tmp_path: Path) -> None:
    stats, eval_dir = _run(tmp_path, ["64hnagcpvk_en.json"], llm=DuplicateJsonLlm())

    assert stats.rows_deduped == 3  # within-group ×2 (each group offered the identical pair) + cross-group ×1
    assert stats.rows_written == 1  # the identical pair collapses to a single row
    assert stats.groups_failed == 1  # the second group only offered the duplicate
    golden = _jsonl(eval_dir, GOLDEN_FILE)
    assert len(golden) == 1 and golden[0]["id"].endswith(":q1")


def test_run_samples_every_capture_even_below_the_default(tmp_path: Path) -> None:
    stats, _ = _run(tmp_path, FIXTURES, samples_per_document=1)
    assert stats.groups_sampled == 3
    assert stats.rows_written == 6

    stats_all, _ = _run(tmp_path, ["64hnagcpvk_en.json"], samples_per_document=999)
    assert stats_all.groups_sampled == stats_all.groups_total  # bounded by the group count


def test_passages_only_rebuilds_the_review_file_byte_identically_offline(tmp_path: Path) -> None:
    stats, eval_dir = _run(tmp_path, FIXTURES)  # a full (echo-LLM) run for reference

    offline_dir = tmp_path / "offline"
    only_stats = write_passages_file(raw_dir=_capture_dir(tmp_path, FIXTURES), output_dir=offline_dir)

    assert only_stats.captures_used == stats.captures_used
    assert only_stats.groups_sampled == stats.groups_sampled > 0
    assert only_stats.outputs and only_stats.outputs[0].endswith(PASSAGES_FILE)
    # same seed + same walk → byte-identical to the full run's passages.jsonl
    assert (offline_dir / PASSAGES_FILE).read_bytes() == (eval_dir / PASSAGES_FILE).read_bytes()
    assert not (offline_dir / GOLDEN_FILE).exists()  # passages-only writes nothing else
    assert not (offline_dir / MANUAL_FILE).exists()
    assert not (offline_dir / "about.md").exists()

    write_passages_file(raw_dir=_capture_dir(tmp_path, FIXTURES), output_dir=tmp_path / "again")
    assert (tmp_path / "again" / PASSAGES_FILE).read_bytes() == (offline_dir / PASSAGES_FILE).read_bytes()


def test_template_rows_come_from_the_committed_fixture_when_present(tmp_path: Path) -> None:
    stats, eval_dir = _run(tmp_path, FIXTURES)

    manual = _jsonl(eval_dir, MANUAL_FILE)
    expected_key = _capture(FIXTURES[0])["instance_key"]
    preferred_group = f"{expected_key}:64hnagcpvk:en:g0000"
    assert manual[0]["source_group_id"] == preferred_group
    assert manual[0]["question"] == TEMPLATE_QUESTIONS[0][1]
    assert manual[1]["query_language"] == "es" and manual[0]["query_language"] == "en"
    assert stats.outputs and any(path.endswith(MANUAL_FILE) for path in stats.outputs)


# --- pure helpers --------------------------------------------------------------


def test_parse_question_list_accepts_strict_and_fenced_json() -> None:
    assert parse_question_list('[{"form": "specific", "question": "q1"}, {"question": "q2"}]') == ["q1", "q2"]
    assert parse_question_list('```json\n[{"question": "a"}]\n```') == ["a"]
    for bad in (
        "",
        "   ",
        "not json",
        "Sure! Here are your questions!",
        "```json\n[]",
        '{"question": "not an array"}',
        '[{"form": "specific"}]',
    ):
        with pytest.raises(ValueError):
            parse_question_list(bad)
    assert parse_question_list('[{"question": "ok"}, {"question": "  "}, {"question": 7}]') == ["ok"]


PASSAGE = "The Commission approved the report on November 30, 2016. Detention conditions in Peru were widely documented."


def test_validator_rejects_junk_and_copies() -> None:
    assert question_problem("", PASSAGE) == "empty"
    assert question_problem("   ", PASSAGE) == "empty"
    assert question_problem("yes?", PASSAGE) == "too_short"
    assert question_problem("What did they decide?", PASSAGE) is None
    too_long = " ".join(f"palabra{i}" for i in range(30))
    assert question_problem(too_long, PASSAGE) == "too_long"
    assert question_problem("approved the report on November 30", PASSAGE) == "copied_from_passage"


def test_copy_run_violation_needs_five_consecutive_copied_words() -> None:
    passage = "los derechos humanos deben respetarse siempre y en todo lugar según la corte"
    assert not copy_run_violation("¿cuántos derechos humanos se documentaron aquí?", passage)
    # a question that IS a verbatim fragment of the passage is a copy even below 5 words
    assert copy_run_violation("los derechos humanos", passage)
    assert not copy_run_violation("¿cuántos derechos?", passage)  # short but not a verbatim fragment
    assert copy_run_violation("where do they say los derechos humanos deben respetarse?", passage)


def test_select_questions_keeps_bounded_unique_valid_questions() -> None:
    passage = "the report describes detention conditions during the armed conflict era"
    kept, reasons = select_questions(
        [
            "describes detention conditions during",  # copied run → invalid
            "who approved the report?",  # kept (q1)
            "who approved the report?",  # duplicate → dedup reason
            "what conditions are described?",  # kept (q2)
            "when did detention become routine again?",  # beyond the 2-question cap
        ],
        passage=passage,
    )
    assert kept == ["who approved the report?", "what conditions are described?"]
    assert reasons == ["copied_from_passage", "duplicate", "beyond_limit"]


def test_prompt_carries_the_constraints_without_the_title() -> None:
    capture = _capture("64hnagcpvk_en.json")
    groups = build_passage_groups(
        capture["paragraphs"],
        instance_key=capture["instance_key"],
        shared_id=capture["shared_id"],
        language=capture["language"],
        file_id=capture["file"]["id"],
        title=capture["title"],
    )
    prompt = build_generation_prompt(groups[0], "en")
    assert "Write the questions in: English" in prompt
    assert "one very specific question, one broader/vaguer question" in prompt
    assert "don't copy 5 consecutive words from the excerpt" in prompt
    assert "return strict JSON only" in prompt
    assert groups[0].text in prompt
    assert capture["title"] not in prompt  # the excerpt must not carry the title/header

    assert "Write the questions in: Spanish" in build_generation_prompt(groups[0], "es")
    assert "Write the questions in: fr" in build_generation_prompt(groups[0], "fr")


def test_other_language_swaps_within_the_configured_pair() -> None:
    assert other_language("en", ("en", "es")) == "es"
    assert other_language("es", ("en", "es")) == "en"
    assert other_language("fr", ("en", "es")) is None
    assert other_language("en", ("en",)) is None


def test_make_golden_rows_follows_the_schema_exactly() -> None:
    capture = _capture("64hnagcpvk_en.json")
    group = build_passage_groups(
        capture["paragraphs"],
        instance_key=capture["instance_key"],
        shared_id=capture["shared_id"],
        language=capture["language"],
        file_id=capture["file"]["id"],
        title=capture["title"],
    )[0]
    rows = make_golden_rows(group, ["first", "second"], query_language="es")
    assert [row["id"] for row in rows] == [f"{group.group_id}:q1", f"{group.group_id}:q2"]
    for row, question in zip(rows, ("first", "second"), strict=True):
        assert list(row) == GOLD_SCHEMA
        assert row["question"] == question and row["origin"] == "synthetic"
        assert row["query_language"] == "es"  # query language, NOT the capture's
        assert row["expected"]["language"] == "en" == capture["language"]
        assert row["expected"]["text"] == group.text
        assert list(row["expected"]) == EXPECTED_SCHEMA


def test_manual_template_rows_demonstrate_the_schema() -> None:
    capture = _capture("64hnagcpvk_en.json")
    groups = build_passage_groups(
        capture["paragraphs"],
        instance_key=capture["instance_key"],
        shared_id=capture["shared_id"],
        language=capture["language"],
        file_id=capture["file"]["id"],
        title=capture["title"],
    )
    rows = build_manual_template(groups[0], groups[1])
    assert [row["id"] for row in rows] == ["template-1", "template-2"]
    assert [row["origin"] for row in rows] == ["example", "example"]
    assert [row["query_language"] for row in rows] == [TEMPLATE_QUESTIONS[0][0], TEMPLATE_QUESTIONS[1][0]]
    assert [row["question"] for row in rows] == [TEMPLATE_QUESTIONS[0][1], TEMPLATE_QUESTIONS[1][1]]
    assert rows[0]["expected"]["text"] == groups[0].text
    assert rows[1]["expected"]["text"] == groups[1].text


# --- manual merge ---------------------------------------------------------------


def _valid_manual_row(passages: list[dict[str, Any]], *, query_language: str = "en", **overrides: Any) -> dict[str, Any]:
    passage = passages[0]
    row: dict[str, Any] = {
        "origin": "manual",
        "question": "Which IACHR friendly-settlement report covers Petition 1339-07 from Peru?",
        "query_language": query_language,
        "source_group_id": passage["group_id"],
        "expected": {key: passage[key] for key in EXPECTED_SCHEMA},
    }
    row.update(overrides)
    return row


def _unanswerable_row(**overrides: Any) -> dict[str, Any]:
    """A manual row for a real topic the corpus does not contain (no anchor)."""
    row: dict[str, Any] = {
        "origin": "manual",
        "question": "What is documented about conditions in the North Korean political prison camps?",
        "query_language": "en",
        "source_group_id": None,
        "expected": None,
    }
    row.update(overrides)
    return row


def test_merge_appends_valid_manual_rows_and_skips_examples(tmp_path: Path) -> None:
    stats, eval_dir = _run(tmp_path, [FIXTURES[0]])
    passages = _jsonl(eval_dir, PASSAGES_FILE)
    manual_path = eval_dir / MANUAL_FILE
    manual = _jsonl(eval_dir, MANUAL_FILE)
    extra = [
        _valid_manual_row(passages),
        _valid_manual_row(passages, query_language="es", question="¿Qué estableció el informe de la CIDH en 2016?"),
    ]
    write_jsonl(manual_path, manual + extra)

    merged = merge_manual_rows(eval_dir=eval_dir)

    assert merged.golden_rows_before == stats.rows_written
    assert merged.golden_rows_after == merged.golden_rows_before + 2
    assert merged.manual_rows_read == 4
    assert merged.manual_rows_merged == 2 and merged.example_rows_skipped == 2
    assert merged.ids_autoassigned == 2

    golden = _jsonl(eval_dir, GOLDEN_FILE)
    assert golden[-2]["id"] == "m001" and golden[-1]["id"] == "m002"
    assert all(row["origin"] == "manual" for row in golden[-2:])
    assert all(row["origin"] == "synthetic" for row in golden[:-2])  # manual rows stay separable


def test_merging_the_same_manual_row_twice_skips_instead_of_duplicating(tmp_path: Path) -> None:
    _, eval_dir = _run(tmp_path, [FIXTURES[0]])
    passages = _jsonl(eval_dir, PASSAGES_FILE)

    manual = _jsonl(eval_dir, MANUAL_FILE)  # the 2 template rows
    write_jsonl(eval_dir / MANUAL_FILE, manual + [_valid_manual_row(passages)])
    first = merge_manual_rows(eval_dir=eval_dir)  # merges the row once (m001)
    assert first.manual_rows_merged == 1 and first.manual_rows_skipped_duplicated == 0

    second = merge_manual_rows(eval_dir=eval_dir)  # same manual file again
    assert second.manual_rows_merged == 0 and second.manual_rows_skipped_duplicated == 1
    golden = _jsonl(eval_dir, GOLDEN_FILE)
    assert sum(1 for row in golden if row.get("id") == "m001") == 1


def test_merge_validates_and_aborts_without_touching_golden(tmp_path: Path) -> None:
    _, eval_dir = _run(tmp_path, [FIXTURES[0]])
    passages = _jsonl(eval_dir, PASSAGES_FILE)
    manual_examples = _jsonl(eval_dir, MANUAL_FILE)
    golden_bytes = (eval_dir / GOLDEN_FILE).read_bytes()

    mismatched = _valid_manual_row(passages)
    mismatched["expected"] = {**mismatched["expected"], "paragraph_ids": [0, 99]}
    golden = _jsonl(eval_dir, GOLDEN_FILE)
    cases = [
        _valid_manual_row(passages, origin="synthetic"),
        _valid_manual_row(passages, question="   "),
        _valid_manual_row(passages, query_language="fr"),
        {**_valid_manual_row(passages), "source_group_id": "bdd5a7c445847b35:none:en:g9999"},
        {**_valid_manual_row(passages), "expected": "not an object"},
        mismatched,
        _valid_manual_row(passages, id=golden[0]["id"]),  # id collides with a synthetic row
    ]
    for index, bad in enumerate(cases):
        write_jsonl(eval_dir / MANUAL_FILE, manual_examples + [bad])
        with pytest.raises(ValueError):
            merge_manual_rows(eval_dir=eval_dir)
        assert (eval_dir / GOLDEN_FILE).read_bytes() == golden_bytes, f"case {index} ({bad.get('origin', '?')})"

    (eval_dir / MANUAL_FILE).write_text('{"origin": "manual", bare\n', encoding="utf-8")
    with pytest.raises(ValueError, match="not valid JSON"):
        merge_manual_rows(eval_dir=eval_dir)


def test_merge_requires_an_existing_dataset(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError, match="build-golden"):
        merge_manual_rows(eval_dir=tmp_path / "empty")


def test_merge_accepts_unanswerable_rows_without_an_anchor(tmp_path: Path) -> None:
    _, eval_dir = _run(tmp_path, [FIXTURES[0]])
    manual_examples = _jsonl(eval_dir, MANUAL_FILE)  # the 2 template rows
    write_jsonl(eval_dir / MANUAL_FILE, manual_examples + [_unanswerable_row()])

    stats = merge_manual_rows(eval_dir=eval_dir)

    assert stats.manual_rows_merged == 1 and stats.ids_autoassigned == 1
    golden = _jsonl(eval_dir, GOLDEN_FILE)
    row = golden[-1]
    assert row["id"] == "m001" and row["origin"] == "manual"
    assert row["source_group_id"] is None and row["expected"] is None
    assert "camps" in row["question"]  # question survives untouched


def test_merge_rejects_rows_with_only_one_null_field(tmp_path: Path) -> None:
    _, eval_dir = _run(tmp_path, [FIXTURES[0]])
    passages = _jsonl(eval_dir, PASSAGES_FILE)
    manual_examples = _jsonl(eval_dir, MANUAL_FILE)
    golden_bytes = (eval_dir / GOLDEN_FILE).read_bytes()

    only_null_anchor = _valid_manual_row(passages)
    only_null_anchor["source_group_id"] = None
    only_null_expected = _valid_manual_row(passages)
    only_null_expected["expected"] = None
    cases = [only_null_anchor, only_null_expected]

    for index, bad in enumerate(cases):
        write_jsonl(eval_dir / MANUAL_FILE, manual_examples + [bad])
        with pytest.raises(ValueError, match="null together"):
            merge_manual_rows(eval_dir=eval_dir)
        assert (eval_dir / GOLDEN_FILE).read_bytes() == golden_bytes, f"case {index}"


def test_merging_an_unanswerable_row_twice_skips_instead_of_duplicating(tmp_path: Path) -> None:
    _, eval_dir = _run(tmp_path, [FIXTURES[0]])
    manual_examples = _jsonl(eval_dir, MANUAL_FILE)  # the 2 template rows
    write_jsonl(eval_dir / MANUAL_FILE, manual_examples + [_unanswerable_row()])
    first = merge_manual_rows(eval_dir=eval_dir)
    assert first.manual_rows_merged == 1

    second = merge_manual_rows(eval_dir=eval_dir)  # same manual file again
    assert second.manual_rows_merged == 0 and second.manual_rows_skipped_duplicated == 1
    golden = _jsonl(eval_dir, GOLDEN_FILE)
    assert sum(1 for row in golden if row.get("question") == _unanswerable_row()["question"]) == 1
