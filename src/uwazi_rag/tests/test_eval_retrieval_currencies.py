"""The currency-ladder worked examples (Step 3.6 scorecard honesty upgrade).

Paragraph currency (coverage@k, coverage@char-budget), chunk currency (P@k,
R-precision) and the existing recall/MRR are pinned here on hand-built golds
and rankings — each case is the hand-computed scenario that justifies the
lenses: what chunk credit hides, what coverage exposes, and where the char
budget cuts. One bookkeeping test runs ``row_golds`` over a real capture to
prove the anchor/grouping data coverage needs actually arrives. Pure functions
only — no mocks, no store, no network (AGENTS.md testing policy).
"""

from __future__ import annotations

from typing import Any

import pytest

from uwazi_rag.use_cases.eval_retrieval import (
    COVERAGE_CHAR_BUDGET,
    ChunkConfig,
    DocKey,
    GradedSet,
    Hit,
    RowGold,
    RunFacts,
    captures_by_doc_key,
    coverage_at_char_budget,
    coverage_at_k,
    precision_at_k,
    r_precision,
    recall_at_k,
    render,
    row_golds,
    score_rows,
)
from uwazi_rag.use_cases.fetch_document import raw_capture_json
from uwazi_rag.use_cases.index_captures import capture_to_chunks

INSTANCE = "unit0123456789"
DOC_KEY: DocKey = (INSTANCE, "doc", "en")


def _hit(chunk_id: str, score: float = 0.5) -> Hit:
    return Hit(chunk_id=chunk_id, doc_key=DOC_KEY, score=score)


def _pgold(row_id: str, anchors: tuple[int, ...], grouping: dict[int, tuple[str, ...]]) -> RowGold:
    """A hand-built gold: anchors + per-paragraph chunk grouping (chunk gold = the union)."""
    paragraph_chunks = tuple((pid, frozenset(grouping.get(pid, ()))) for pid in anchors)
    return RowGold(
        row_id=row_id,
        origin="synthetic",
        query_language="en",
        expected_language="en",
        doc_key=DOC_KEY,
        gold_chunk_ids=frozenset(cid for ids in grouping.values() for cid in ids),
        anchor_paragraphs=anchors,
        paragraph_chunks=paragraph_chunks,
    )


def _run_facts() -> RunFacts:
    return RunFacts(
        label="currency lens",
        started_at_utc="2026-10-05T00:00:00+00:00",
        elapsed_seconds=0.0,
        golden_path="golden.jsonl",
        rows=1,
        synthetic_rows=1,
        manual_rows=0,
        store_path="store.json",
        store_chunks=3,
        store_model="m",
        store_dimensions=8,
        store_created_at_utc="0",
        config=ChunkConfig(),
        false_retrieval_threshold=0.55,
    )


# ---------------------------------------------------------------------------
# Worked example: the blob — one chunk holding every anchor
# ---------------------------------------------------------------------------


def test_blob_at_rank_1_makes_coverage_and_recall_agree() -> None:
    """When one chunk carries all the text, both currencies read the same number."""
    gold = _pgold("blob", anchors=(0, 1, 2), grouping={0: ("BLOB",), 1: ("BLOB",), 2: ("BLOB",)})
    hits = [_hit("BLOB", 0.9), _hit("decoy1", 0.4), _hit("decoy2", 0.3)]

    for k in (1, 5, 10):
        assert coverage_at_k(hits, gold, k) == pytest.approx(1.0)
        assert recall_at_k(hits, gold.gold_chunk_ids, k) == pytest.approx(1.0)
        assert coverage_at_k(hits, gold, k) == pytest.approx(recall_at_k(hits, gold.gold_chunk_ids, k))

    # and when the blob is buried at rank 2, both go 0 → 1 together
    buried = [_hit("decoy1", 0.4), _hit("BLOB", 0.39)]
    assert coverage_at_k(buried, gold, 1) == recall_at_k(buried, gold.gold_chunk_ids, 1) == 0.0
    assert coverage_at_k(buried, gold, 2) == recall_at_k(buried, gold.gold_chunk_ids, 2) == 1.0


# ---------------------------------------------------------------------------
# Worked example: thin vs fat packing — chunk credit hides, coverage exposes
# ---------------------------------------------------------------------------


def test_thin_and_fat_packing_read_identical_chunk_credit_but_different_coverage() -> None:
    """Same three anchors {Q, R, S}; the same safe-looking 50% chunk-credit means different texts seen.

    Thin packer: Q is split across Q1+Q2; R and S one chunk each → gold = 4 chunks.
    Fat packer: Q alone in F1; R+S share F2 → gold = 2 chunks. At k=2 both
    rankings retrieve exactly one gold chunk — chunk-credit says 50% for both —
    but thin saw two paragraph's worth of text (2/3) and fat one (1/3).
    """
    thin = _pgold("thin", anchors=(0, 1, 2), grouping={0: ("Q1", "Q2"), 1: ("R1",), 2: ("S1",)})
    fat = _pgold("fat", anchors=(0, 1, 2), grouping={0: ("F1",), 1: ("F2",), 2: ("F2",)})
    thin_hits = [_hit("Q1", 0.9), _hit("R1", 0.8), _hit("junk", 0.1)]  # misses Q2 and S1
    fat_hits = [_hit("F1", 0.9), _hit("junk", 0.1)]  # misses F2 (two anchors inside)

    assert recall_at_k(thin_hits, thin.gold_chunk_ids, 2) == pytest.approx(0.5)
    assert recall_at_k(fat_hits, fat.gold_chunk_ids, 2) == pytest.approx(0.5)
    assert coverage_at_k(thin_hits, thin, 2) == pytest.approx(2 / 3)
    assert coverage_at_k(fat_hits, fat, 2) == pytest.approx(1 / 3)

    # packaging immunity: the denominators are the anchors themselves, identical
    # rows graded under either packer — 1/3 of anchors is 1/3, whatever the gold
    # happened to chunk into. (And a split paragraph needs only ONE of its chunks.)
    assert len(thin.gold_chunk_ids) == 4 and len(fat.gold_chunk_ids) == 2
    assert coverage_at_k([_hit("Q2")], thin, 10) == pytest.approx(1 / 3)


def test_a_paragraph_covered_by_any_one_of_its_piece_chunks() -> None:
    """Coverage credits ANY chunk holding the paragraph; chunk recall needs the whole gold set."""
    gold = _pgold("split", anchors=(0,), grouping={0: ("P1", "P2", "P3")})
    hits = [_hit("P2", 0.8)]
    assert coverage_at_k(hits, gold, 1) == pytest.approx(1.0)  # one piece is enough
    assert recall_at_k(hits, gold.gold_chunk_ids, 1) == pytest.approx(1 / 3)  # chunk currency wants all three


# ---------------------------------------------------------------------------
# Worked example: single gold chunk deep in the ranking
# ---------------------------------------------------------------------------


def test_single_gold_chunk_at_rank_3_scores_zero_then_full() -> None:
    gold = _pgold("solo", anchors=(7,), grouping={7: ("G",)})
    hits = [_hit("a"), _hit("b"), _hit("G", 0.7), _hit("c"), _hit("d"), _hit("e")]

    assert coverage_at_k(hits, gold, 1) == 0.0
    assert recall_at_k(hits, gold.gold_chunk_ids, 1) == 0.0
    assert coverage_at_k(hits, gold, 3) == 1.0
    assert coverage_at_k(hits, gold, 5) == 1.0
    assert recall_at_k(hits, gold.gold_chunk_ids, 5) == 1.0


# ---------------------------------------------------------------------------
# Worked example: R-precision is P at the gold size, not at k
# ---------------------------------------------------------------------------


def test_r_precision_is_precision_at_the_gold_size_not_at_k() -> None:
    gold = frozenset({"G1", "G2"})
    hits = [_hit("G1", 0.9), _hit("x"), _hit("y"), _hit("G2", 0.6), _hit("z")]

    assert precision_at_k(hits, gold, 1) == pytest.approx(1.0)
    assert precision_at_k(hits, gold, 5) == pytest.approx(0.4)
    assert r_precision(hits, gold) == pytest.approx(0.5)  # P@|gold|=2: top-2 = {G1, x}

    # the same hits with the second gold moved up: RP → 1.0 while P@5 cannot move
    dense = [_hit("G1"), _hit("G2"), _hit("x"), _hit("y"), _hit("z")]
    assert r_precision(dense, gold) == pytest.approx(1.0)
    assert precision_at_k(dense, gold, 5) == pytest.approx(0.4)


# ---------------------------------------------------------------------------
# Worked example: the char-budget lens packs whole chunks and stops at overflow
# ---------------------------------------------------------------------------


def test_char_budget_packs_whole_chunks_and_stops_at_the_overflow() -> None:
    gold = _pgold("budget", anchors=(0,), grouping={0: ("C2",)})
    lengths = {"C1": 2000, "C2": 1000, "C3": 100}
    hits = [_hit("C1"), _hit("C2"), _hit("C3")]

    # the boundary is inclusive: exactly the budget's worth of chunks still pack
    assert coverage_at_char_budget(hits, gold, lengths, 3000) == pytest.approx(1.0)
    # one char less and C2 would overflow: unseen, though it ranks 2nd
    assert coverage_at_char_budget(hits, gold, lengths, 2999) == pytest.approx(0.0)
    # prefix semantics: a later tiny chunk never rescues an earlier overflow
    assert coverage_at_char_budget(hits, gold, lengths, 2100) == pytest.approx(0.0)


def test_char_budget_needs_a_length_for_every_hit_chunk() -> None:
    gold = _pgold("loud", anchors=(0,), grouping={0: ("C1",)})
    with pytest.raises(ValueError, match="char length"):
        coverage_at_char_budget([_hit("C1")], gold, {}, 3000)


def test_score_rows_skips_only_the_budget_lens_without_char_lengths() -> None:
    gold = _pgold("r1", anchors=(0, 1), grouping={0: ("c0",), 1: ("c1",)})
    graded = GradedSet(golds=[gold])
    hits = [_hit("c0", 0.9), _hit("c1", 0.4)]

    card = score_rows(graded, {"r1": hits}, false_retrieval_threshold=None)
    scope = card.scopes[0]
    assert scope.paragraph.coverage[1] == pytest.approx(0.5)
    assert scope.paragraph.coverage[5] == pytest.approx(1.0)
    assert scope.paragraph.budget_coverage is None  # unmeasured, not guessed

    lengths = {"c0": 1200, "c1": 1500}
    card_len = score_rows(graded, {"r1": hits}, false_retrieval_threshold=None, chunk_char_lengths=lengths)
    # 1200 + 1500 = 2700 ≤ 3000: both gold chunks pack inside the default budget
    assert card_len.scopes[0].paragraph.budget_coverage == pytest.approx(1.0)
    assert card_len.char_budget == COVERAGE_CHAR_BUDGET

    with pytest.raises(ValueError, match="char_budget"):
        score_rows(graded, {"r1": hits}, false_retrieval_threshold=None, char_budget=0)


# ---------------------------------------------------------------------------
# row_golds carries the anchor bookkeeping (real chunker, real capture)
# ---------------------------------------------------------------------------


def _capture_with_split_paragraph() -> dict:
    long_text = "detail sentence about detention conditions " * 30
    return raw_capture_json(
        shared_id="splitdoc1",
        language="en",
        instance_key=INSTANCE,
        title="Split Doc",
        template_id="t0",
        template_name="Report",
        file_id="f0f0f0f0",
        file_name="doc.pdf",
        segmentation_status="ready",
        paragraphs=[
            {"type": "Text", "pageNumber": 1, "text": "opener."},
            {"type": "Text", "pageNumber": 1, "text": long_text},
            {"type": "Picture", "pageNumber": 1, "text": ""},
            {"type": "Text", "pageNumber": 2, "text": "closing note."},
        ],
    )


def test_row_golds_records_anchors_and_their_per_paragraph_chunk_grouping() -> None:
    capture = _capture_with_split_paragraph()
    rows: list[dict[str, Any]] = [
        {
            "id": "mixed",
            "question": "q?",
            "origin": "manual",
            "query_language": "en",
            "source_group_id": "g",
            "expected": {
                "instance_key": capture["instance_key"],
                "shared_id": capture["shared_id"],
                "title": capture["title"],
                "language": capture["language"],
                "file_id": capture["file"]["id"],
                "paragraph_ids": [0, 1, 2, 3],
                "text": "irrelevant",
            },
        }
    ]
    config = ChunkConfig(target_max_chars=300, overlap_ratio=0.0)
    grader = row_golds(rows, captures=captures_by_doc_key([capture]), config=config)
    gold = grader.golds[0]

    assert gold.anchor_paragraphs == (0, 1, 2, 3)
    grouping = {pid: frozenset(cids) for pid, cids in gold.paragraph_chunks}
    assert len(grouping[1]) >= 2, "the split paragraph must span several chunks"
    assert grouping[2] == frozenset(), "the dropped picture paragraph can never be covered"
    assert grouping[0] and grouping[3], "the whole paragraphs keep their chunk(s)"
    assert gold.gold_chunk_ids == frozenset().union(*grouping.values())
    assert gold.unmapped_paragraph_ids == (2,)
    assert grader.anomalies and "not keepable" in grader.anomalies[0]

    # the honesty the lens buys: retrieving every mapped chunk caps coverage at
    # 3/4 (paragraph 2 was dropped by the chunker and is genuinely unseen),
    # while chunk recall — which only counts mapped chunks — reads a full 100%.
    hits = [_hit(cid, 0.9 - 0.01 * index) for index, cid in enumerate(sorted(gold.gold_chunk_ids))]
    assert coverage_at_k(hits, gold, len(hits)) == pytest.approx(3 / 4)
    assert recall_at_k(hits, gold.gold_chunk_ids, len(hits)) == pytest.approx(1.0)


def test_split_paragraph_chunks_actually_cut_at_the_config() -> None:
    """Guard for the scenario above: the 300-char config must really split the long paragraph."""
    capture = _capture_with_split_paragraph()
    chunks = capture_to_chunks(capture, target_max_chars=300, overlap_ratio=0.0, prepend_header=False)
    assert any(set(chunk.paragraph_ids) == {1} for chunk in chunks), "the long paragraph's own piece chunks"


# ---------------------------------------------------------------------------
# Scorecard + render: new columns land, old columns unchanged
# ---------------------------------------------------------------------------


def test_scorecard_scopes_and_render_carry_the_new_currency_columns() -> None:
    gold = _pgold("r1", anchors=(0, 1), grouping={0: ("c0",), 1: ("c1",)})
    graded = GradedSet(golds=[gold])
    hits = [_hit("c0", 0.9), _hit("c1", 0.4)]  # both gold chunks in the top ranks

    card = score_rows(
        graded,
        {"r1": hits},
        false_retrieval_threshold=None,
        chunk_char_lengths={"c0": 1200, "c1": 1500, "decoy": 900},
    )
    scope = card.scopes[0]
    assert scope.paragraph.coverage[1] == pytest.approx(0.5)  # only para 0's chunk in top-1
    assert scope.paragraph.coverage[5] == pytest.approx(1.0)
    assert scope.paragraph.budget_coverage == pytest.approx(1.0)  # 2700 chars pack within 3000
    assert scope.chunk.precision[1] == pytest.approx(1.0)
    assert scope.chunk.precision[5] == pytest.approx(2 / 5)
    assert scope.chunk.r_precision == pytest.approx(1.0)  # P@|gold|=2: both gold in top-2

    block = render(_run_facts(), card, heading=False)
    assert "| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR |" in block
    assert "cov@1 | cov@5 | cov@10 | cov@3000 | P@1 | P@5 | P@10 | RP |" in block
    assert "systematically pessimistic" in block
    assert "coverage lens: cov@k" in block
    # the full "all" row, hand-computed: doc metrics are 1.0 (gold doc is the only doc hit)
    assert (
        "| all | 1 | 50.0% | 100.0% | 100.0% | 1.000 | 100.0% | 100.0% | 100.0% | 1.000 "
        "| 50.0% | 100.0% | 100.0% | 100.0% | 100.0% | 40.0% | 20.0% | 100.0% |" in block
    )


def test_render_shows_the_unmeasured_budget_lens_as_a_dash() -> None:
    gold = _pgold("r1", anchors=(0,), grouping={0: ("c0",)})
    card = score_rows(GradedSet(golds=[gold]), {"r1": [_hit("c0")]}, false_retrieval_threshold=None)

    block = render(_run_facts(), card, heading=False)
    scope_row = next(line for line in block.splitlines() if line.startswith("| all |"))
    cells = [cell.strip() for cell in scope_row.strip("|").split("|")]
    assert cells[-1] == "100.0%"  # RP
    assert cells[-5] == "—"  # cov@budget: no char lengths → reported, never guessed
