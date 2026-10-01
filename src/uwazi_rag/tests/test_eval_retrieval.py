"""Step 3.5, scorecard tests: paragraph→chunk mapping + retrieval metrics.

Fully offline (AGENTS.md testing policy): real committed fixtures, the real
chunker, the tests' deterministic ``HashingEmbedding`` and the approved
in-memory ``NaiveVectorStore`` — no mocks, no stubs, no network. The live
Ollama scorecard is the `uwazi-rag eval` command, never pytest.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from uwazi_rag.adapters.naive_vector_store import NaiveVectorStore
from uwazi_rag.configuration import FIXTURES_DIR
from uwazi_rag.tests.hash_embedding import HashingEmbedding
from uwazi_rag.use_cases.chunking import TARGET_MAX_CHARS, build_chunks
from uwazi_rag.use_cases.eval_retrieval import (
    RETRIEVAL_DEPTH,
    ChunkConfig,
    GradedSet,
    Hit,
    RowGold,
    RunFacts,
    captures_by_doc_key,
    config_kwargs,
    doc_gold_rank,
    first_gold_rank,
    paragraph_chunk_map,
    recall_at_k,
    render,
    row_golds,
    score_rows,
    verify_store_chunks,
)
from uwazi_rag.use_cases.fetch_document import raw_capture_json
from uwazi_rag.use_cases.index_captures import capture_to_chunks, index_captures

DIMENSIONS = 64
FIXTURES = ["64hnagcpvk_en.json", "ar22d4v4i5s_en.json", "ar22d4v4i5s_es.json"]
INSTANCE = "bdd5a7c445847b35"


def _capture(name: str) -> dict:
    capture: dict = json.loads((FIXTURES_DIR / name).read_text(encoding="utf-8"))
    return capture


def _paras(texts: list[str], page: int = 1) -> list[dict]:
    return [{"type": "Text", "pageNumber": page, "text": text} for text in texts]


def _tiny_capture(
    paragraphs: list[dict],
    *,
    shared_id: str,
    language: str = "en",
    title: str = "Tiny Doc",
) -> dict:
    return raw_capture_json(
        shared_id=shared_id,
        language=language,
        instance_key=INSTANCE,
        title=title,
        template_id="t0",
        template_name="Report",
        file_id="f0f0f0f0",
        file_name="doc.pdf",
        segmentation_status="ready",
        paragraphs=paragraphs,
    )


def _gold(
    row_id: str,
    *,
    language: str = "en",
    origin: str = "synthetic",
    doc: str | None = None,
    query_language: str | None = None,
) -> RowGold:
    doc_id = doc or f"doc{row_id}"
    return RowGold(
        row_id=row_id,
        origin=origin,
        query_language=query_language or language,
        expected_language=language,
        doc_key=(INSTANCE, doc_id, language),
        gold_chunk_ids=frozenset({f"{INSTANCE}:{doc_id}:{language}:f:0000"}),
    )


def _hit(doc: str, score: float = 0.5, index: int = 0, doc_lang: str = "en") -> Hit:
    return Hit(chunk_id=f"{INSTANCE}:{doc}:{doc_lang}:f:{index:04d}", doc_key=(INSTANCE, doc, doc_lang), score=score)


# ---------------------------------------------------------------------------
# Paragraph → chunk mapping
# ---------------------------------------------------------------------------


def test_map_covers_keepable_positions_and_skips_dropped_gaps() -> None:
    paragraphs = [
        {"type": "Page header", "pageNumber": 1, "text": "repeated boilerplate"},
        {"type": "Text", "pageNumber": 1, "text": "alpha holds the opener."},
        {"type": "Picture", "pageNumber": 1, "text": ""},
        {"type": "Text", "pageNumber": 2, "text": "beta closes the capture."},
    ]
    chunks = build_chunks(
        paragraphs,
        instance_key=INSTANCE,
        shared_id="aaaa1111bbbb",
        language="en",
        file_id="f0f0f0f0",
        entity_title="Tiny Doc",
        template_name="Report",
    )
    mapping = paragraph_chunk_map(chunks)
    assert set(mapping) == {1, 3}  # dropped positions 0 and 2 leave gaps, never map
    assert all(len(ids) == 1 for ids in mapping.values())
    assert chunks[0].paragraph_ids == [1, 3]  # tiny doc: everything fits one chunk


def test_long_paragraph_maps_to_all_of_its_piece_chunks() -> None:
    long_text = " ".join(f"witness sentence number {i} describes the raid in detail" for i in range(40))
    assert len(long_text) > 300
    paragraphs = _paras(["opener.", long_text, "closing note."])
    chunks = build_chunks(
        paragraphs,
        instance_key=INSTANCE,
        shared_id="aaaa1111bbbb",
        language="en",
        file_id="f0f0f0f0",
        entity_title="Tiny Doc",
        template_name="Report",
        **config_kwargs(ChunkConfig(target_max_chars=300, overlap_ratio=0.0, prepend_header=False)),
    )
    mapping = paragraph_chunk_map(chunks)
    owning = [chunk.chunk_index for chunk in chunks if chunk.chunk_id in set(mapping[1])]
    assert len(owning) >= 8  # one 1000+ char paragraph is spread across many chunks
    assert owning == list(range(1, len(chunks)))  # consecutive: opener alone, then all piece chunks
    assert chunks[0].paragraph_ids == [0]  # opener never shares with the split paragraph
    assert chunks[-1].paragraph_ids == [1, 2]  # the tail piece shares with the closer
    assert mapping[2] == [chunks[-1].chunk_id]


def test_mapping_is_monotonic_and_complete_on_real_fixtures() -> None:
    for name in FIXTURES:
        capture = _capture(name)
        chunks = capture_to_chunks(capture)
        mapping = paragraph_chunk_map(chunks)
        keepable_ids = {
            index
            for index, paragraph in enumerate(capture["paragraphs"])
            if str(paragraph.get("text", "")).strip()
            and str(paragraph.get("type", "")).lower() not in {"page header", "page footer"}
        }
        assert set(mapping) == keepable_ids, name  # every paragraph is covered exactly once-ish

        last_pid: int | None = None
        for chunk in chunks:
            if chunk.paragraph_ids:
                if last_pid is not None:
                    assert chunk.paragraph_ids[0] >= last_pid, (
                        name,
                        chunk.chunk_id,
                    )  # document order (equal only at split boundaries)
                last_pid = max(chunk.paragraph_ids)


def test_mapped_paragraph_text_lives_in_its_chunk_body() -> None:
    for name in FIXTURES:
        capture = _capture(name)
        for chunk in capture_to_chunks(capture):
            body = chunk.text.split("\n", 1)[1]
            normalized_body = " ".join(body.split())
            for pid in chunk.paragraph_ids:
                text = " ".join(str(capture["paragraphs"][pid]["text"]).strip().split())
                if len(text) <= TARGET_MAX_CHARS:  # single-piece paragraphs must be fully contained
                    assert text in normalized_body, (name, pid)


def test_chunk_identity_ignores_the_header_flag() -> None:
    capture = _capture("ar22d4v4i5s_en.json")
    base = capture_to_chunks(capture)
    bare = capture_to_chunks(capture, prepend_header=False)
    assert [chunk.chunk_id for chunk in bare] == [chunk.chunk_id for chunk in base]
    assert not bare[0].text.startswith(capture["title"])  # no header line
    assert base[0].text.startswith(capture["title"])
    map_base = paragraph_chunk_map(base)
    map_bare = paragraph_chunk_map(bare)
    assert {pid: frozenset(ids) for pid, ids in map_base.items()} == {pid: frozenset(ids) for pid, ids in map_bare.items()}


def test_overlap_change_keeps_every_paragraph_covered() -> None:
    long_text = "law text sentence about jurisdiction " * 60  # ~2280 chars, gets split
    capture = _tiny_capture(
        _paras(["intro paragraph on procedure.", long_text, "outro on remedies."]), shared_id="longdoc1", title="Long Law"
    )
    base = capture_to_chunks(capture)
    tight = capture_to_chunks(capture, overlap_ratio=0.0)
    keepable_ids = {0, 1, 2}
    assert set(paragraph_chunk_map(tight)) == keepable_ids
    assert set(paragraph_chunk_map(base)) == keepable_ids
    # the sweep must actually change something, or `eval`'s config check could
    # never catch a mislabeled run: split pieces still cut at different points
    assert {chunk.text for chunk in tight} != {chunk.text for chunk in base}


def test_build_chunks_validates_sweep_knobs() -> None:
    kwargs: dict[str, Any] = dict(
        instance_key=INSTANCE,
        shared_id="aaaa1111bbbb",
        language="en",
        file_id="f0f0f0f0",
        entity_title="Tiny Doc",
        template_name="Report",
    )
    with pytest.raises(ValueError, match="target_max_chars"):
        build_chunks(_paras(["short."]), **kwargs, target_max_chars=0)
    with pytest.raises(ValueError, match="overlap_ratio"):
        build_chunks(_paras(["short."]), **kwargs, overlap_ratio=0.5)
    with pytest.raises(ValueError, match="overlap_ratio"):
        build_chunks(_paras(["short."]), **kwargs, overlap_ratio=-0.1)


# ---------------------------------------------------------------------------
# Gold building
# ---------------------------------------------------------------------------


def test_row_golds_anchors_chunks_and_splits_unanswerable() -> None:
    capture = _capture("ar22d4v4i5s_en.json")
    paragraphs = capture["paragraphs"]
    keepable_ids = [i for i, p in enumerate(paragraphs) if str(p.get("text", "")).strip()]
    expected = {
        "instance_key": capture["instance_key"],
        "shared_id": capture["shared_id"],
        "title": capture["title"],
        "language": capture["language"],
        "file_id": capture["file"]["id"],
        "paragraph_ids": keepable_ids[10:12],
        "text": "irrelevant",
    }
    rows: list[dict[str, Any]] = [
        {
            "id": "ok",
            "question": "q?",
            "origin": "manual",
            "query_language": "en",
            "source_group_id": "g",
            "expected": expected,
        },
        {
            "id": "none",
            "question": "q?",
            "origin": "manual",
            "query_language": "en",
            "source_group_id": None,
            "expected": None,
        },
        {
            "id": "gone",
            "question": "q?",
            "origin": "synthetic",
            "query_language": "en",
            "source_group_id": "g",
            "expected": {**expected, "shared_id": "zzzzzzzzzz"},
        },
        {
            "id": "filemoved",
            "question": "q?",
            "origin": "synthetic",
            "query_language": "en",
            "source_group_id": "g",
            "expected": {**expected, "file_id": "deadbeef"},
        },
    ]
    graded = row_golds(rows, captures=captures_by_doc_key([capture]), config=ChunkConfig())

    assert [gold.row_id for gold in graded.golds] == ["ok"]
    assert graded.golds[0].gold_chunk_ids, "paragraphs 10..11 must live in at least one chunk"
    assert graded.golds[0].doc_key == (capture["instance_key"], capture["shared_id"], "en")
    assert [gold.row_id for gold in graded.unanswerable] == ["none"]
    assert len(graded.ungradable) == 2
    assert all("no capture for" in note or "file_id" in note for note in graded.ungradable)


def test_row_golds_reports_anchors_of_dropped_paragraphs() -> None:
    capture = _capture("ar22d4v4i5s_en.json")
    paragraphs = capture["paragraphs"]
    dropped = next(
        i
        for i, p in enumerate(paragraphs)
        if not (str(p.get("text", "")).strip() and str(p.get("type", "")).lower() not in {"page header", "page footer"})
    )
    keepable_ids = [i for i, p in enumerate(paragraphs) if str(p.get("text", "")).strip()]
    expected = {
        "instance_key": capture["instance_key"],
        "shared_id": capture["shared_id"],
        "title": capture["title"],
        "language": capture["language"],
        "file_id": capture["file"]["id"],
        "paragraph_ids": [dropped, *keepable_ids[10:12]],
        "text": "irrelevant",
    }
    rows = [
        {
            "id": "mixed",
            "question": "q?",
            "origin": "manual",
            "query_language": "en",
            "source_group_id": "g",
            "expected": expected,
        }
    ]
    graded = row_golds(rows, captures=captures_by_doc_key([capture]), config=ChunkConfig())

    gold = graded.golds[0]
    assert gold.unmapped_paragraph_ids == (dropped,)
    assert graded.anomalies and "not keepable" in graded.anomalies[0]
    assert graded.golds[0].gold_chunk_ids, "the keepable anchors still grade"


# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------


def test_chunk_level_metrics_rank_and_recall_and_mrr() -> None:
    gold = frozenset({f"{INSTANCE}:aaa:en:f:0001"})
    hits = [_hit("aaa", 0.9, 0), _hit("bbb", 0.8, 0), _hit("aaa", 0.6, 1), _hit("ccc", 0.5, 0)]
    assert first_gold_rank(hits, gold) == 3
    assert recall_at_k(hits, gold, 1) == 0.0
    assert recall_at_k(hits, gold, 3) == 1.0
    assert recall_at_k(hits, gold, 10) == 1.0


def test_metrics_with_gold_out_of_the_ranking_score_zero() -> None:
    gold = frozenset({"x:0009"})
    hits = [_hit("aaa", 0.9), _hit("bbb", 0.8)]
    assert first_gold_rank(hits, gold) == 0
    assert recall_at_k(hits, gold, 10) == 0.0
    assert doc_gold_rank(hits, (INSTANCE, "xxx", "en")) == 0


def test_doc_metrics_dedupe_documents_in_first_hit_order() -> None:
    hits = [_hit("bbb", 0.9), _hit("bbb", 0.8, 1), _hit("aaa", 0.7, 5)]
    assert doc_gold_rank(hits, (INSTANCE, "aaa", "en")) == 2
    assert doc_gold_rank(hits, (INSTANCE, "bbb", "en")) == 1


def test_metrics_on_an_empty_ranking() -> None:
    gold = frozenset({"x:0000"})
    assert first_gold_rank([], gold) == 0
    assert recall_at_k([], gold, 5) == 0.0
    assert doc_gold_rank([], (INSTANCE, "aaa", "en")) == 0


# ---------------------------------------------------------------------------
# Config guard + config parsing
# ---------------------------------------------------------------------------


def test_verify_store_chunks_flags_a_mismatched_chunk_config() -> None:
    capture = _capture("ar22d4v4i5s_en.json")
    built = capture_to_chunks(capture)
    narrower = capture_to_chunks(capture, target_max_chars=600)
    assert len(narrower) > len(built)

    ok = verify_store_chunks(
        {chunk.chunk_id: chunk.text for chunk in built},
        {chunk.chunk_id: chunk.text for chunk in capture_to_chunks(capture)},
    )
    assert not ok.fatal
    bad = verify_store_chunks(
        {chunk.chunk_id: chunk.text for chunk in built},
        {chunk.chunk_id: chunk.text for chunk in narrower},
    )
    assert bad.fatal
    assert bad.missing_in_store
    assert not bad.extra_in_store


def test_chunk_config_from_store_parses_and_rejects_junk() -> None:
    assert ChunkConfig.from_store(None) == ChunkConfig()
    config = ChunkConfig.from_store({"target_max_chars": 900, "overlap_ratio": 0.3, "prepend_header": False})
    assert config == ChunkConfig(target_max_chars=900, overlap_ratio=0.3, prepend_header=False)
    with pytest.raises(ValueError, match="chunk_config"):
        ChunkConfig.from_store({"target_max_chars": 900})
    with pytest.raises(ValueError, match="overlap_ratio"):
        ChunkConfig.from_store({"target_max_chars": 900, "overlap_ratio": 0.9, "prepend_header": True})


# ---------------------------------------------------------------------------
# Scorecard aggregation + rendering
# ---------------------------------------------------------------------------


def _graded_set() -> GradedSet:
    golds = [
        _gold("r1", language="en", origin="synthetic"),
        _gold("r2", language="en", origin="manual"),
        _gold("r3", language="es", origin="synthetic", doc="docr3", query_language="en"),
        _gold("r4", language="es", origin="manual"),
    ]
    return GradedSet(golds=golds, unanswerable=[RowGold(row_id="u1", origin="manual", query_language="en")])


def test_scorecard_scopes_match_hand_computed_means() -> None:
    graded = _graded_set()
    hits_by_row = {
        "r1": [_hit("docr1", 0.9)],  # gold first
        "r2": [_hit("nope", 0.9), _hit("docr2", 0.8)],  # gold second
        "r3": [_hit("docr3", 0.9, doc_lang="es")],  # cross-language gold first
        "r4": [_hit("else", 0.9), _hit("other", 0.8)],  # miss
        "u1": [_hit("whatever", 0.6531)],
    }
    card = score_rows(graded, hits_by_row, false_retrieval_threshold=0.5)

    assert card.answerable_rows == 4
    by_label = {scope.label: scope for scope in card.scopes}
    assert [scope.label for scope in card.scopes] == [
        "all",
        "en",
        "es",
        "synthetic",
        "manual",
        "cross-language",
        "same-language",
    ]
    assert by_label["all"].n == 4
    assert by_label["all"].chunk.recall[1] == pytest.approx(0.5)  # r1, r3 hit@1; r2, r4 miss@1
    assert by_label["all"].chunk.mrr == pytest.approx(0.625)  # 1.0, 0.5, 1.0, 0.0
    assert by_label["all"].doc.mrr == pytest.approx(0.625)
    assert by_label["en"].n == 2
    assert by_label["en"].chunk.mrr == pytest.approx(0.75)  # 1.0 and 0.5
    assert by_label["en"].doc.mrr == pytest.approx(0.75)
    assert by_label["es"].chunk.recall[1] == pytest.approx(0.5)
    assert by_label["es"].chunk.mrr == pytest.approx(0.5)  # 1.0 (cross) and 0.0
    assert by_label["synthetic"].n == 2
    assert by_label["synthetic"].chunk.recall[1] == pytest.approx(1.0)  # r1, r3 (cross) both perfect
    assert by_label["manual"].chunk.recall[1] == pytest.approx(0.0)  # r2 misses@1, r4 misses
    assert by_label["manual"].chunk.mrr == pytest.approx(0.25)  # 0.5 and 0.0
    assert by_label["cross-language"].n == 1  # only r3 (en query, es doc)
    assert by_label["cross-language"].chunk.recall[1] == pytest.approx(1.0)
    assert by_label["same-language"].n == 3  # r1, r2, r4
    card = score_rows(graded, hits_by_row, false_retrieval_threshold=0.5)

    assert card.answerable_rows == 4
    by_label = {scope.label: scope for scope in card.scopes}
    assert [scope.label for scope in card.scopes] == [
        "all",
        "en",
        "es",
        "synthetic",
        "manual",
        "cross-language",
        "same-language",
    ]
    assert by_label["all"].n == 4
    assert by_label["all"].chunk.recall[1] == pytest.approx(0.5)  # r1 hit@1, r2 miss@1, r3 hit@1, r4 miss@1
    assert by_label["en"].n == 2
    assert by_label["en"].chunk.recall[1] == pytest.approx(0.5)
    assert by_label["en"].chunk.mrr == pytest.approx(0.75)  # 1.0 and 0.5
    assert by_label["es"].chunk.recall[1] == pytest.approx(0.5)
    assert by_label["es"].chunk.mrr == pytest.approx(0.5)  # 1.0 and 0.0
    assert by_label["synthetic"].n == 2
    assert by_label["synthetic"].chunk.recall[1] == pytest.approx(1.0)
    assert by_label["manual"].chunk.recall[1] == pytest.approx(0.0)
    assert by_label["cross-language"].n == 1
    assert by_label["cross-language"].chunk.recall[1] == pytest.approx(1.0)
    assert by_label["same-language"].n == 3

    assert card.unanswerable.rows == 1
    assert card.unanswerable.top1_scores == {"u1": pytest.approx(0.6531)}
    assert card.unanswerable.false_retrievals == ("u1",)  # 0.6531 ≥ 0.5


def test_unanswerable_rows_never_enter_recall_or_mrr() -> None:
    graded = _graded_set()
    hits_by_row = {
        "r1": [_hit("docr1", 0.9)],
        "r2": [_hit("docr2", 0.8)],
        "r3": [_hit("docr3", 0.9, doc_lang="es")],
        "r4": [_hit("else", 0.9)],
        "u1": [_hit("whatever", 0.9)],
    }
    card = score_rows(graded, hits_by_row, false_retrieval_threshold=0.5)
    assert card.answerable_rows == 4
    assert card.unanswerable.false_retrieval_rate == pytest.approx(1.0)
    assert card.unanswerable.rows == 1

    # a lower threshold keeps the identical top score out of the false bucket
    card_lax = score_rows(graded, hits_by_row, false_retrieval_threshold=0.95)
    assert card_lax.unanswerable.false_retrieval_rate == 0.0


def test_threshold_boundary_is_inclusive_and_validated() -> None:
    graded = _graded_set()
    hits_by_row = {"r1": [_hit("docr1", 0.9)], "u1": [_hit("whatever", 0.5)]}
    # r2..r4 have no hits → zero scores; u1's 0.5 == threshold counts as a false retrieval
    card = score_rows(
        GradedSet(golds=graded.golds[:1], unanswerable=graded.unanswerable), hits_by_row, false_retrieval_threshold=0.5
    )
    assert card.unanswerable.false_retrievals == ("u1",)
    with pytest.raises(ValueError, match="false_retrieval_threshold"):
        score_rows(GradedSet(), {}, false_retrieval_threshold=1.1)


def test_render_produces_markdown_block_and_console_variant() -> None:
    graded = _graded_set()
    hits_by_row = {
        "r1": [_hit("docr1", 0.9)],
        "r2": [_hit("docr2", 0.8)],
        "r3": [_hit("docr3", 0.9, doc_lang="es")],
        "r4": [_hit("else", 0.9)],
        "u1": [_hit("whatever", 0.6531)],
    }
    card = score_rows(graded, hits_by_row, false_retrieval_threshold=0.5)
    run = RunFacts(
        label="unit test",
        started_at_utc="2026-10-01T00:00:00+00:00",
        elapsed_seconds=1.5,
        golden_path="data/eval/golden.jsonl",
        rows=5,
        synthetic_rows=2,
        manual_rows=3,
        store_path="data/naive_store.json",
        store_chunks=10,
        store_model="test-model",
        store_dimensions=16,
        store_created_at_utc="2026-01-01T00:00:00+00:00",
        config=ChunkConfig(),
        false_retrieval_threshold=0.5,
    )
    block = render(run, card, heading=True)
    assert block.startswith("## 2026-10-01T00:00:00+00:00 — unit test\n")
    assert "| scope | n | chunk R@1 | chunk R@5 | chunk R@10 | chunk MRR | doc R@1 | doc R@5 | doc R@10 | doc MRR |" in block
    assert "| all | 4 |" in block and "| en | 2 |" in block
    assert "false-retrieval 1/1 (100.0%)" in block and "u1 0.6531" in block
    plain = render(run, card, heading=False)
    assert not plain.startswith("##")
    assert "store: `data/naive_store.json`" in plain


# ---------------------------------------------------------------------------
# Offline end-to-end: real chunker + real store + deterministic embedder
# ---------------------------------------------------------------------------


def test_full_scorecard_round_trip_on_tiny_synthetic_corpus(tmp_path: Path) -> None:
    bern = _tiny_capture(
        _paras(
            [
                "Bicycle accidents in Bern rose last August, the municipal report said plainly.",
                "Helmet use among Bern cycling commuters doubled, the health office announced today.",
                "The Bern council debates new bike lanes next month near the central station.",
            ]
        ),
        shared_id="bern1111",
        title="Bern Bikes",
    )
    swan = _tiny_capture(
        _paras(
            [
                "Algae blooms tinted Swan Lake green while the pollution office took samples.",
                "Swan Lake swimming bans were extended by the environmental agency this summer.",
                "Fish die-offs at Swan Lake followed the July heatwave, biologists confirmed.",
            ]
        ),
        shared_id="swan2222",
        title="Swan Lake",
    )
    gold_rows: list[dict[str, Any]] = []
    for row_id, (capture, pid) in {
        "bern_row": (bern, 0),
        "swan_row": (swan, 1),
        "cross_row": (swan, 2),
    }.items():
        gold_rows.append(
            {
                "id": row_id,
                "question": str(capture["paragraphs"][pid]["text"]).strip(),  # the strongest oracle a test can use
                "origin": "synthetic",
                "query_language": "en",
                "source_group_id": "g0",
                "expected": {
                    "instance_key": capture["instance_key"],
                    "shared_id": capture["shared_id"],
                    "title": capture["title"],
                    "language": capture["language"],
                    "file_id": capture["file"]["id"],
                    "paragraph_ids": [pid],
                    "text": str(capture["paragraphs"][pid]["text"]),
                },
            }
        )
        if row_id == "cross_row":  # the query text is still an exact match; only the label differs
            gold_rows[-1]["query_language"] = "es"
    gold_rows.append(
        {
            "id": "unanswerable",
            "question": "quantum flux capacitor unicorn migration routes",
            "origin": "manual",
            "query_language": "en",
            "source_group_id": None,
            "expected": None,
        }
    )

    raw_dir = tmp_path / "raw" / INSTANCE
    raw_dir.mkdir(parents=True)
    for capture in (bern, swan):
        (raw_dir / f"{capture['shared_id']}_{capture['language']}.json").write_text(json.dumps(capture), encoding="utf-8")

    config = ChunkConfig(target_max_chars=200, overlap_ratio=0.0)
    store = NaiveVectorStore(
        dimensions=DIMENSIONS,
        embedding_model="hash-test",
        chunk_config={
            "target_max_chars": config.target_max_chars,
            "overlap_ratio": config.overlap_ratio,
            "prepend_header": config.prepend_header,
        },
    )
    embedder = HashingEmbedding(DIMENSIONS)
    index_captures(
        raw_dir=raw_dir,
        store=store,
        embedder=embedder,
        expected_dimensions=DIMENSIONS,
        target_max_chars=config.target_max_chars,
        overlap_ratio=config.overlap_ratio,
        prepend_header=config.prepend_header,
    )
    expected_chunks = [chunk for capture in (bern, swan) for chunk in capture_to_chunks(capture, **config_kwargs(config))]
    assert len(store) == len(expected_chunks)  # one chunk per <=200-char packing

    graded = row_golds(gold_rows, captures=captures_by_doc_key([bern, swan]), config=config)
    assert [gold.row_id for gold in graded.golds] == ["bern_row", "swan_row", "cross_row"]
    assert [gold.row_id for gold in graded.unanswerable] == ["unanswerable"]

    hits_by_row: dict[str, list[Hit]] = {}
    for gold in (*graded.golds, *graded.unanswerable):
        row = next(row for row in gold_rows if row["id"] == gold.row_id)
        vector = embedder.embed([str(row["question"])])[0]
        hits_by_row[gold.row_id] = [
            Hit(chunk_id=chunk.chunk_id, doc_key=(chunk.instance_key, chunk.shared_id, chunk.language), score=score)
            for chunk, score in store.search(vector, k=RETRIEVAL_DEPTH)
        ]

    card = score_rows(graded, hits_by_row, false_retrieval_threshold=0.5)
    by_label = {scope.label: scope for scope in card.scopes}
    assert by_label["all"].chunk.recall[1] == pytest.approx(1.0)  # exact-text oracle ranks gold first
    assert by_label["all"].doc.recall[1] == pytest.approx(1.0)
    assert by_label["all"].doc.mrr == pytest.approx(1.0)
    assert by_label["cross-language"].chunk.recall[1] == pytest.approx(1.0)
    assert card.unanswerable.top1_scores["unanswerable"] < 0.5  # garbage query, tiny lexical overlap
    assert card.unanswerable.false_retrieval_rate == 0.0
    assert card.ungradable == ()
