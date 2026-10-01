"""Step 3.5 tests: passage-group extraction + seeded sampling, offline.

Real fixtures only — the grouping rule must behave identically on the exact
captures the golden dataset will be built from (AGENTS.md testing policy).
"""

import json
from typing import Any

from uwazi_rag.configuration import FIXTURES_DIR
from uwazi_rag.use_cases.chunking import keepable
from uwazi_rag.use_cases.passage_groups import (
    GROUP_TARGET_CHARS,
    SAMPLING_SEED,
    SEED_PREFIX,
    build_passage_groups,
    format_group_view,
    numbered_keepable_paragraphs,
    sample_groups,
    sampling_seed,
)

FIXTURES = ["64hnagcpvk_en.json", "ar22d4v4i5s_en.json", "ar22d4v4i5s_es.json"]


def _capture(name: str) -> dict:
    capture: dict = json.loads((FIXTURES_DIR / name).read_text(encoding="utf-8"))
    return capture


def _groups(name: str) -> list:
    capture = _capture(name)
    return build_passage_groups(
        capture["paragraphs"],
        instance_key=capture["instance_key"],
        shared_id=capture["shared_id"],
        language=capture["language"],
        file_id=capture["file"]["id"],
        title=capture["title"],
    )


def test_numbering_is_the_keepable_subsequence_in_document_order() -> None:
    for name in FIXTURES:
        capture = _capture(name)
        expected_ids = [index for index, paragraph in enumerate(capture["paragraphs"]) if keepable(paragraph)]
        numbered = numbered_keepable_paragraphs(capture["paragraphs"])
        assert [paragraph_id for paragraph_id, _ in numbered] == expected_ids, name
        assert all(keepable(paragraph) for _, paragraph in numbered), name


def test_groups_partition_the_numbered_paragraphs_in_order() -> None:
    for name in FIXTURES:
        capture = _capture(name)
        groups = _groups(name)
        keepable_ids = [paragraph_id for paragraph_id, _ in numbered_keepable_paragraphs(capture["paragraphs"])]
        assert [group.group_index for group in groups] == list(range(len(groups))), name
        # groups hold consecutive keepable paragraphs (raw positions — gaps where
        # page furniture was dropped), in document order
        assert [pid for group in groups for pid in group.paragraph_ids] == keepable_ids, name
        for group in groups:
            assert group.paragraph_ids == sorted(group.paragraph_ids), name


def test_groups_pack_to_the_target_and_never_exceed_it_across_paragraphs() -> None:
    for name in FIXTURES:
        for group in _groups(name):
            # only groups holding a single over-long paragraph may exceed the target
            assert len(group.text) <= GROUP_TARGET_CHARS or len(group.paragraph_ids) == 1, name
            stripped = [
                str(_capture(name)["paragraphs"][paragraph_id]["text"]).strip() for paragraph_id in group.paragraph_ids
            ]
            assert group.text == "\n".join(stripped), name


def test_single_long_paragraph_makes_one_unsplittable_group() -> None:
    text = "El testimonio menciona hechos concretos de agosto. " * 50
    paragraph: dict[str, Any] = {"type": "Text", "pageNumber": 7, "text": text}
    groups = build_passage_groups(
        [paragraph],
        instance_key="bdd5a7c445847b35",
        shared_id="aaaaaa1111",
        language="es",
        file_id="ffffffff11",
        title="Doc",
    )
    assert len(groups) == 1
    assert len(groups[0].text) > GROUP_TARGET_CHARS  # not split, not padded
    assert groups[0].paragraph_ids == [0]
    assert groups[0].text == text.strip()
    assert groups[0].page_start == 7 and groups[0].page_end == 7


def test_greedy_packing_closes_before_pushing_past_the_target() -> None:
    paragraphs = [
        {"type": "Text", "pageNumber": 1, "text": f"Paragraph {index} " + "contenido relevante" * 28} for index in range(5)
    ]
    groups = build_passage_groups(
        paragraphs,
        instance_key="bdd5a7c445847b35",
        shared_id="aaaaaa1111",
        language="en",
        file_id="ffffffff11",
        title="Doc",
    )
    assert [len(group.paragraph_ids) for group in groups] == [2, 2, 1]
    assert [group.text for group in groups] == [
        "Paragraph 0 " + "contenido relevante" * 28 + "\n" + "Paragraph 1 " + "contenido relevante" * 28,
        "Paragraph 2 " + "contenido relevante" * 28 + "\n" + "Paragraph 3 " + "contenido relevante" * 28,
        "Paragraph 4 " + "contenido relevante" * 28,
    ]


def test_page_furniture_and_empty_boxes_never_join_a_group() -> None:
    paragraphs = [
        {"type": "Picture", "pageNumber": 1, "text": ""},
        {"type": "Page header", "pageNumber": 2, "text": "Serie A No. 2"},
        {"type": "Page footer", "pageNumber": 2, "text": "www.example.org"},
        {"type": "Text", "pageNumber": 2, "text": "  The real content lives here.  "},
        {"type": "Text", "pageNumber": 3, "text": "And continues overleaf."},
    ]
    groups = build_passage_groups(
        paragraphs,
        instance_key="bdd5a7c445847b35",
        shared_id="aaaaaa1111",
        language="en",
        file_id="ffffffff11",
        title="Doc",
    )
    assert len(groups) == 1
    assert groups[0].paragraph_ids == [3, 4]  # raw positions — the three dropped ones leave gaps
    assert groups[0].text == "The real content lives here.\nAnd continues overleaf."
    assert groups[0].page_start == 2 and groups[0].page_end == 3


def test_group_ids_are_deterministic_and_identity_shaped() -> None:
    for name in FIXTURES:
        capture = _capture(name)
        groups = _groups(name)
        for group in groups:
            assert (
                group.group_id
                == f"{capture['instance_key']}:{capture['shared_id']}:{capture['language']}:g{group.group_index:04d}"
            ), name
            assert group.title == capture["title"]
            assert group.file_id == capture["file"]["id"]
        rebuilt = _groups(name)
        assert [group.model_dump() for group in rebuilt] == [group.model_dump() for group in groups], name


def test_sampling_is_deterministic_and_respects_per_document() -> None:
    groups = _groups("ar22d4v4i5s_en.json")
    assert len(groups) > 2
    for per_document in (1, 2, 3, 99):
        first = sample_groups(groups, seed=sampling_seed("bdd5a7c445847b35", "ar22d4v4i5s", "en"), per_document=per_document)
        second = sample_groups(
            groups, seed=sampling_seed("bdd5a7c445847b35", "ar22d4v4i5s", "en"), per_document=per_document
        )
        assert first == second
        assert len(first) == min(per_document, len(groups))
        assert len({group.group_id for group, _ in first}) == len(first)
        assert [group.group_index for group, _ in first] == sorted(group.group_index for group, _ in first)


def test_cross_language_flags_follow_the_ratio() -> None:
    groups = _groups("64hnagcpvk_en.json")
    seed = sampling_seed("bdd5a7c445847b35", "64hnagcpvk", "en")
    assert all(not cross for _, cross in sample_groups(groups, seed=seed, cross_language_ratio=0.0))
    assert all(cross for _, cross in sample_groups(groups, seed=seed, cross_language_ratio=1.0))


def test_sample_groups_rejects_invalid_settings() -> None:
    groups = _groups("64hnagcpvk_en.json")
    seed = sampling_seed("bdd5a7c445847b35", "64hnagcpvk", "en")
    assert sample_groups([], seed=seed) == []
    try:
        sample_groups(groups, seed=seed, per_document=0)
    except ValueError as error:
        assert "per_document" in str(error)
    else:
        raise AssertionError("per_document=0 must fail")
    try:
        sample_groups(groups, seed=seed, cross_language_ratio=1.5)
    except ValueError as error:
        assert "cross_language_ratio" in str(error)
    else:
        raise AssertionError("ratio 1.5 must fail")


def test_sampling_seed_documentation_matches_the_rule() -> None:
    assert sampling_seed("bdd5a7c445847b35", "64hnagcpvk", "en") == (
        f"uwazi-rag/golden/v1/{SAMPLING_SEED}/bdd5a7c445847b35/64hnagcpvk/en"
    )
    assert SEED_PREFIX  # referenced by data/eval/about.md — the seed must stay explainable


def test_format_group_view_shows_text_neighbors_and_sampled_status() -> None:
    paragraphs = [
        {"type": "Text", "pageNumber": page, "text": f"Paragraph {index} " + "contenido relevante" * 28}
        for index, page in enumerate((1, 1, 2, 2, 3), start=0)
    ]
    groups = build_passage_groups(
        paragraphs,
        instance_key="bdd5a7c445847b35",
        shared_id="aaaaaa1111",
        language="es",
        file_id="ffffffff11",
        title="Doc title",
    )
    assert len(groups) == 3  # [2, 2, 1] packing

    middle = format_group_view(groups[1], all_groups=groups, sampled_ids={groups[0].group_id})
    assert groups[1].group_id in middle
    assert groups[1].text.splitlines()[0] in middle  # the full passage is shown
    assert "← g0000 (sampled)" in middle and "→ g0002 (not sampled)" in middle
    assert "sampled groups: g0000" in middle  # hint names the anchoring targets
    assert "Doc title" in middle and "ffffffff11" in middle

    first = format_group_view(groups[0], all_groups=groups, sampled_ids={groups[0].group_id})
    assert "← " not in first and "→ g0001" in first
    last = format_group_view(groups[2], all_groups=groups, sampled_ids=set())
    assert "← g0001 (not sampled)" in last and "\n→ " not in last
