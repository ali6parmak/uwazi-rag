"""Shared grading-run tests (`eval` and `benchmark`'s one code path).

Fully offline (AGENTS.md testing policy): tiny synthetic captures + the real
chunker + the real ``index_captures`` + the tests' deterministic
``HashingEmbedding`` + a real saved ``NaiveVectorStore``. No mocks, no stubs,
no network — the live Ollama scorecard is the `eval` command, never pytest.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from uwazi_rag.adapters.naive_vector_store import NaiveVectorStore
from uwazi_rag.tests.hash_embedding import HashingEmbedding
from uwazi_rag.use_cases.eval_retrieval import (
    RESULTS_HEADER,
    ChunkConfig,
    first_gold_rank,
    render,
    score_rows,
)
from uwazi_rag.use_cases.eval_run import (
    EvalInputsError,
    append_results,
    build_run_facts,
    prepare_run,
    rank_rows,
)
from uwazi_rag.use_cases.fetch_document import raw_capture_json
from uwazi_rag.use_cases.index_captures import capture_to_chunks, index_captures, load_captures

DIMENSIONS = 32
INSTANCE = "bench0123456789"


def _capture(shared_id: str, language: str, title: str, paragraph_texts: list[str]) -> dict[str, Any]:
    paragraphs = [{"type": "Text", "pageNumber": 1 + index // 2, "text": text} for index, text in enumerate(paragraph_texts)]
    return raw_capture_json(
        shared_id=shared_id,
        language=language,
        instance_key=INSTANCE,
        title=title,
        template_id="t0",
        template_name="IACHR Report",
        file_id="f1f1f1f1",
        file_name="report.pdf",
        segmentation_status="ready",
        paragraphs=paragraphs,
    )


def _padded(text: str, count: int = 400) -> str:
    return " ".join([text] * (count // (len(text) + 1)))


EN_PARAGRAPHS = [
    _padded("Witnesses described the night raid on the village bridge with exact times and unit insignia."),
    _padded("The commission recorded the detentions in its annex and cross-checked the register entries."),
    _padded("Reparations were discussed separately in the closing session of the delegation visit."),
]
ES_PARAGRAPHS = [
    _padded("Los testigos describieron el asalto nocturno al puente con horas y siglas de la unidad."),
    _padded("La comisión registró las detenciones en su anexo y cotejó las entradas del registro."),
    _padded("Las reparaciones se discutieron por separado en la sesión de cierre de la visita."),
]
DECOY_PARAGRAPHS = [
    _padded("Maritime insurance arbitration clauses dominate the annexes of the shipping contract dispute."),
    _padded("The carrier liability ceiling was renegotiated under the freight forwarding agreement."),
    _padded("Demurrage charges accumulated during the port closure week and were later waived."),
]


@pytest.fixture()
def corpus(tmp_path: Path) -> tuple[Path, Path, Path, NaiveVectorStore]:
    """Tmp raw dir + saved store + golden file: two target docs, a decoy, one stale golden row."""
    raw_dir = tmp_path / "raw"
    en = _capture("docen1111", "en", "Night Raid Report", EN_PARAGRAPHS)
    es = _capture("doces1111", "es", "Informe del asalto nocturno", ES_PARAGRAPHS)
    decoy = _capture("decoy1111", "en", "Shipping Contract Report", DECOY_PARAGRAPHS)
    for capture in (en, es, decoy):
        raw_dir.mkdir(parents=True, exist_ok=True)
        path = raw_dir / f"{capture['shared_id']}_{capture['language']}.json"
        path.write_text(json.dumps(capture, ensure_ascii=False), encoding="utf-8")

    embedder = HashingEmbedding(dimensions=DIMENSIONS)
    store = NaiveVectorStore(
        dimensions=DIMENSIONS,
        embedding_model="hashing",
        chunk_config={"target_max_chars": 1800, "overlap_ratio": 0.15, "prepend_header": True},
    )
    stats = index_captures(raw_dir=raw_dir, store=store, embedder=embedder, expected_dimensions=DIMENSIONS)
    assert stats.chunks_indexed == 3, "each ~1,200-char capture must land in exactly one chunk"
    store_path = tmp_path / "store.json"
    store.save(store_path)

    rows = [
        {
            "id": "q-en",
            "question": " ".join(EN_PARAGRAPHS[0].split()),
            "origin": "synthetic",
            "query_language": "en",
            "source_group_id": "g-en",
            "expected": {
                "instance_key": en["instance_key"],
                "shared_id": en["shared_id"],
                "language": "en",
                "title": en["title"],
                "file_id": en["file"]["id"],
                "paragraph_ids": capture_to_chunks(en)[0].paragraph_ids,
                "text": "irrelevant",
            },
        },
        {
            "id": "q-es",
            "question": " ".join(ES_PARAGRAPHS[1].split()),
            "origin": "synthetic",
            "query_language": "en",  # cross-language row: asked in en, gold is es
            "source_group_id": "g-es",
            "expected": {
                "instance_key": es["instance_key"],
                "shared_id": es["shared_id"],
                "language": "es",
                "title": es["title"],
                "file_id": es["file"]["id"],
                "paragraph_ids": capture_to_chunks(es)[0].paragraph_ids,
                "text": "irrelevant",
            },
        },
        {
            "id": "q-un",
            "question": "quantum flux monitoring instrumentation grid",
            "origin": "manual",
            "query_language": "en",
            "source_group_id": None,
            "expected": None,
        },
        {
            "id": "q-gone",
            "question": "anything about a vanished document",
            "origin": "synthetic",
            "query_language": "en",
            "source_group_id": "g-gone",
            "expected": {
                "instance_key": INSTANCE,
                "shared_id": "zzzzzzzz",
                "language": "en",
                "title": "Gone",
                "file_id": "f1f1f1f1",
                "paragraph_ids": [0, 1],
                "text": "irrelevant",
            },
        },
    ]
    golden_path = tmp_path / "golden.jsonl"
    golden_path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows), encoding="utf-8")
    return raw_dir, store_path, golden_path, store


def test_prepare_run_loads_and_verifies_the_shared_path(corpus: tuple[Path, Path, Path, NaiveVectorStore]) -> None:
    raw_dir, store_path, golden_path, _store = corpus
    prepared = prepare_run(store_path=store_path, raw_dir=raw_dir, golden_path=golden_path)

    assert prepared.config == ChunkConfig()
    assert not prepared.check.fatal
    assert not prepared.check.extra_in_store
    assert [gold.row_id for gold in prepared.graded.golds] == ["q-en", "q-es"]
    assert len(prepared.graded.ungradable) == 1  # q-gone: capture identity is missing on purpose
    assert len(prepared.graded.unanswerable) == 1  # q-un: expected null


def test_rank_rows_ranks_the_gold_chunk_first_deterministically(
    corpus: tuple[Path, Path, Path, NaiveVectorStore],
) -> None:
    raw_dir, store_path, golden_path, store = corpus
    prepared = prepare_run(store_path=store_path, raw_dir=raw_dir, golden_path=golden_path)

    hits_by_row = rank_rows(prepared, retrieval="embedding", embedder=HashingEmbedding(dimensions=DIMENSIONS))
    assert set(hits_by_row) == {"q-en", "q-es", "q-un", "q-gone"}  # every row gets a ranking
    assert all(len(hits) == len(store) for hits in hits_by_row.values())  # tiny store: full depth

    for gold in prepared.graded.golds:
        assert first_gold_rank(hits_by_row[gold.row_id], gold.gold_chunk_ids) == 1, gold.row_id

    card = score_rows(prepared.graded, hits_by_row, false_retrieval_threshold=0.99)
    all_scope = card.scopes[0]
    assert all_scope.label == "all" and all_scope.n == 2
    assert all_scope.chunk.recall[1] >= 0.5  # own-chunk first
    assert all_scope.doc.recall[1] == 1.0
    assert all_scope.doc.mrr == 1.0
    assert card.unanswerable.top1_scores["q-un"] < 0.99  # far from the gold chunks' scores
    assert card.unanswerable.false_retrievals == ()


def test_rank_rows_rejects_wrong_method_missing_embedder_and_model_mismatch(
    corpus: tuple[Path, Path, Path, NaiveVectorStore],
) -> None:
    raw_dir, store_path, golden_path, store = corpus
    prepared = prepare_run(store_path=store_path, raw_dir=raw_dir, golden_path=golden_path)

    with pytest.raises(ValueError, match="not implemented"):
        rank_rows(prepared, retrieval="fancy")
    with pytest.raises(ValueError, match="needs an embedder"):
        rank_rows(prepared, retrieval="embedding", embedder=None)

    # A store loaded under another model's name must refuse the hashing embedder.
    other_path = store_path.parent / "other-model.json"
    other = NaiveVectorStore(dimensions=DIMENSIONS, embedding_model="other-model")
    other.upsert(store.chunks(), [[0.0] * DIMENSIONS for _ in store.chunks()])
    other.save(other_path)
    other_prepared = prepare_run(store_path=other_path, raw_dir=raw_dir, golden_path=golden_path)
    with pytest.raises(ValueError, match="differs from the store's model"):
        rank_rows(other_prepared, retrieval="embedding", embedder=HashingEmbedding(dimensions=DIMENSIONS))


def test_prepare_run_refuses_a_store_that_lies_about_its_chunk_config(
    corpus: tuple[Path, Path, Path, NaiveVectorStore],
) -> None:
    raw_dir, store_path, golden_path, _store = corpus
    # Chunks actually built at 600 max-chars, but the recorded chunk_config claims 1800:
    # re-chunking the captures at the recorded config then disagrees with the store.
    lying = NaiveVectorStore(
        dimensions=DIMENSIONS,
        embedding_model="hashing",
        chunk_config={"target_max_chars": 1800, "overlap_ratio": 0.15, "prepend_header": True},
    )
    index_captures(
        raw_dir=raw_dir,
        store=lying,
        embedder=HashingEmbedding(dimensions=DIMENSIONS),
        expected_dimensions=DIMENSIONS,
        target_max_chars=600,
    )
    assert all(len(capture_to_chunks(capture, target_max_chars=600)) >= 2 for capture in load_captures(raw_dir))
    lying_path = store_path.parent / "lying.json"
    lying.save(lying_path)

    with pytest.raises(EvalInputsError, match="chunk config"):
        prepare_run(store_path=lying_path, raw_dir=raw_dir, golden_path=golden_path)


def test_prepare_run_reports_a_disagreeing_corpus(
    corpus: tuple[Path, Path, Path, NaiveVectorStore],
) -> None:
    raw_dir, store_path, _golden_path, _store = corpus
    stale_path = store_path.parent / "stale-golden.jsonl"
    stale_row = (
        '{"id": "s1", "question": "q", "origin": "synthetic", "query_language": "en", '
        '"expected": {"instance_key": "0000000000000000", "shared_id": "nope", "language": "en", '
        '"file_id": "ffffffff", "paragraph_ids": [0], "text": "x"}}'
    )
    stale_path.write_text(stale_row, encoding="utf-8")
    with pytest.raises(EvalInputsError, match="no golden row could be graded"):
        prepare_run(store_path=store_path, raw_dir=raw_dir, golden_path=stale_path)


def test_build_run_facts_and_render_match_the_eval_block_shape(
    corpus: tuple[Path, Path, Path, NaiveVectorStore],
) -> None:
    raw_dir, store_path, golden_path, _store = corpus
    prepared = prepare_run(store_path=store_path, raw_dir=raw_dir, golden_path=golden_path)
    hits = rank_rows(prepared, retrieval="embedding", embedder=HashingEmbedding(dimensions=DIMENSIONS))
    card = score_rows(prepared.graded, hits, false_retrieval_threshold=0.99)
    run = build_run_facts(
        prepared,
        label="unit — shared path",
        started_at_utc="2026-10-01T00:00:00+00:00",
        elapsed_seconds=1.5,
        false_retrieval_threshold=0.99,
    )

    rendered = render(run, card, heading=True)
    assert "## 2026-10-01T00:00:00+00:00 — unit — shared path" in rendered
    assert f"store: `{prepared.store_path}` — 3 chunks, hashing ({DIMENSIONS}d)" in rendered
    assert "max-chars 1800, overlap 0.15, header on" in rendered
    assert "| all | 2 |" in rendered
    assert "Unanswerable: 1 rows" in rendered
    assert "q-gone" in rendered  # ungradable notes surface — nothing silently dropped


def test_append_results_writes_the_header_exactly_once(tmp_path: Path) -> None:
    results_path = tmp_path / "results.md"
    append_results(results_path, "## block one\n")
    append_results(results_path, "## block two\n")

    text = results_path.read_text(encoding="utf-8")
    assert text.startswith(RESULTS_HEADER)
    assert text.count(RESULTS_HEADER) == 1
    assert "## block one" in text and "## block two" in text
    assert text.index("## block one") < text.index("## block two")  # append-only order
