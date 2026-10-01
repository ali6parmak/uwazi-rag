"""Pure BM25 tests: exact hand-computed Okapi values + ranking behavior.

Fully offline (AGENTS.md testing policy). Corpus and queries kept tiny so
the expected numbers were computed by hand from the formula (k1 = 1.2,
b = 0.75, Lucene-style idf): for the 2-doc corpus below,

  idf("cat") = ln((2 − 1 + 0.5)/(1 + 0.5) + 1) = ln(2)
  d("cat dog cat") against "cat":
      tf = 2, |d| = 3, avgdl = 2 →
      tf-part = 2·2.2 / (2 + 1.2·(0.25 + 0.75·3/2)) = 4.4/3.65 = 88/73
      score = 88/73 · ln 2 ≈ 0.83557468

Everything else follows the same arithmetic; each expected value is written
out in its test.
"""

from __future__ import annotations

import pytest

from uwazi_rag.use_cases.bm25 import Bm25Index, tokenize

TWO_DOCS = {"d0": "cat dog cat", "d1": "bird"}
THREE_DOCS = {"x": "cat dog cat", "y": "bird", "z": "dog dog dog"}


def test_tokenize_lowers_and_keeps_unicode_words() -> None:
    assert tokenize("CaT, DoG!!") == ("cat", "dog")
    assert tokenize("La comisión registró las detenciones") == (
        "la",
        "comisión",
        "registró",
        "las",
        "detenciones",
    )
    assert tokenize("") == ()


def test_single_term_scores_match_hand_computed_okapi_values() -> None:
    index = Bm25Index(TWO_DOCS)
    ranked = index.score("cat")
    # d0 = 88/73 · ln 2 ≈ 0.83557468; d1 has no "cat" → 0.0
    assert ranked[0][0] == "d0"
    assert ranked[0][1] == pytest.approx(0.83557468, rel=1e-6)
    assert ranked[1][0] == "d1"
    assert ranked[1][1] == 0.0

    ranked_bird = index.score("bird")
    # d1: tf-part = 2.2 / 1.75 = 44/35, score = 44/35 · ln 2 ≈ 0.87138503 (smallest |d| wins)
    assert ranked_bird[0][0] == "d1"
    assert ranked_bird[0][1] == pytest.approx(0.87138503, rel=1e-6)
    assert ranked_bird[1][1] == 0.0


def test_multi_term_query_sums_per_unique_term_and_flips_the_ranking() -> None:
    index = Bm25Index(TWO_DOCS)
    ranked = index.score("cat bird")
    # d0 keeps its "cat" score only (88/73 · ln 2), d1 its "bird" score only:
    # "cat bird" → the bird-doc outranks the cat-doc exactly as in single-term.
    assert [doc_id for doc_id, _ in ranked] == ["d1", "d0"]
    assert ranked[0][1] == pytest.approx(0.87138503, rel=1e-6)
    assert ranked[1][1] == pytest.approx(0.83557468, rel=1e-6)


def test_repeated_query_terms_count_once() -> None:
    index = Bm25Index(TWO_DOCS)
    assert index.score("cat cat cat") == index.score("cat")


def test_unknown_terms_score_zero_in_insertion_order() -> None:
    index = Bm25Index(TWO_DOCS)
    ranked = index.score("zebra")
    assert ranked == [("d0", 0.0), ("d1", 0.0)]  # tie-break: insertion order


def test_case_and_punctuation_do_not_change_scores() -> None:
    index = Bm25Index(TWO_DOCS)
    assert index.score("  CaT!  ") == index.score("cat")


def test_document_frequency_lowers_idf_and_respects_length_normalization() -> None:
    index = Bm25Index(THREE_DOCS)
    # N = 3: idf("cat") = ln(8/3) ≈ 0.98082925 (df 1); idf("dog") = ln(1.6) ≈ 0.47000363 (df 2)
    assert index.idf("cat") == pytest.approx(0.98082925, rel=1e-6)
    assert index.idf("dog") == pytest.approx(0.47000363, rel=1e-6)
    # "dog" hits the 3×-repetition doc (z) and the 1×-repetition doc (x):
    # tf saturation keeps z ahead of x but far from 3× ahead; y stays at 0.
    ranked = index.score("dog")
    assert [doc_id for doc_id, _ in ranked] == ["z", "x", "y"]
    z_score, x_score = ranked[0][1], ranked[1][1]
    assert z_score > x_score > 0.0
    assert z_score / x_score < 3.0  # tf-saturation: more term mass, sublinear return


def test_bm25_beats_vague_semantics_on_exact_tokens_in_a_store() -> None:
    """Integration: BM25 over real chunk texts retrieves the exact-number chunk at rank 1."""
    from uwazi_rag.use_cases.chunking import build_chunks

    paragraphs = [
        {"type": "Text", "pageNumber": 1, "text": "The commission opened case file 1987-042 in its July session."},
        {
            "type": "Text",
            "pageNumber": 1,
            "text": "Separate chapters describe the humanitarian consequences and the press visit.",
        },
    ]
    chunks = build_chunks(
        paragraphs,
        instance_key="instance0000000",
        shared_id="numbersdoc",
        language="en",
        file_id="f2f2f2f2",
        entity_title="Number Probe",
        template_name="Report",
        target_max_chars=60,  # force several pieces so the ranking discriminates
    )
    assert len(chunks) >= 2
    index = Bm25Index({chunk.chunk_id: chunk.text for chunk in chunks})
    ranked = index.score("1987-042")
    assert ranked[0][0] == chunks[0].chunk_id  # the chunk containing the number
    assert ranked[0][1] > 0.0
    assert ranked[1][1] == 0.0  # everything else is untouched by the query


def test_index_validates_parameters() -> None:
    with pytest.raises(ValueError, match="k1"):
        Bm25Index(TWO_DOCS, k1=-0.1)
    with pytest.raises(ValueError, match="b"):
        Bm25Index(TWO_DOCS, b=1.1)
    with pytest.raises(ValueError, match="b"):
        Bm25Index(TWO_DOCS, b=-0.1)


def test_empty_corpus_and_empty_documents_never_divide_by_zero() -> None:
    empty = Bm25Index({})
    assert empty.score("cat") == []
    blank = Bm25Index({"a": "", "b": "   "})
    assert blank.avgdl == 1.0  # guarded, not 0
    assert blank.score("cat") == [("a", 0.0), ("b", 0.0)]
