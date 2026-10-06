# Dataset home — vic-chargebook (Isaacus's "Legal RAG Bench")

Isaacus's **Legal RAG Bench** (Butler & Butler 2026, `arXiv:2603.01710`): 100
expert-written, reasoning-intensive questions answered by passages of the Judicial
College of Victoria's **Criminal Charge Book** (Australian criminal law), packaged as
4,876 fixed passages.

## Naming rationale

Its official name collides with ZeroEntropy's `legalbenchrag` by word order
("LegalBench-RAG" vs "Legal RAG Bench") — confusing on sight. The dataset is named by
its single source instead: everything in the corpus comes from the Victorian Criminal
Charge Book, so `vic-chargebook`. The official title is preserved here for citation.

## Upstream & integrity (verified 2026-10-06)

- source: HF dataset `isaacus/legal-rag-bench`
- upstream revision pin: commit `db0b31dc6d195ce9916897e1ac5e4e6209736c8a`
  (2026-03-08, "docs: add graph")
- files (upstream/): `corpus.jsonl`, `qa.jsonl`, `README.md`, `.gitattributes`, `LICENSE`
- checksums measured locally (no official sums published — these become our pin):
  - `corpus.jsonl` sha256 `3a3565bc5429f6cead90548e81f87352b449927e4be1cdd804c28d766bb9c246`
  - `qa.jsonl` sha256 `e3b869a4e293d081ec5f5b39c2058c8d27b36f611aa9f8275eb1877a7c8b38b0`

## Contents (verified by parse)

- `corpus.jsonl`: 4,876 rows, fields `{id, text, title, footnotes}` — ids unique. The
  card does not mention the `footnotes` field: passages carry footnote material the
  adapter must decide about (attach, drop, or keep — record the decision here later).
  Passages are PRE-CHUNKED (≤512 tokens, `semchunk`), Markdown-formatted text.
- `qa.jsonl`: 100 rows, fields `{id, question, answer, relevant_passage_id}` — one
  labeled relevant passage per question (singular), plus the expert answer text.
  Every `relevant_passage_id` resolves into the corpus; ids unique.
- Questions were deliberately written to be lexically dissimilar from their passages —
  the closest thing to unbiased precision labels we hold.

## License

CC BY-NC-SA 4.0 — non-commercial evaluation fine with attribution; cite the dataset
paper and MLEB (`arXiv:2510.19365`). Keep it out of any shipped/commercial artifact.

## What this dataset can decide

- **Embedding-model / retrieval-method races on real expert labels** — its questions
  counter our golden set's self-echo bias (labels independent of our generation loop).
- The gold `answer` texts also support answer-side scoring later (Step 6+ LLM judges).
- **Not** a chunker instrument: the corpus arrives pre-chunked, so a pass-through
  chunker is required and the currency currencies collapse to hit@k/MRR at passage
  level (doc level ≈ passage level). Documented as expected — measure with that in
  mind, not as a fault.
- Known gaps: no unanswerables (hand-authored rows needed); English only (en-AU);
  single-gold labels (no qrels sets); small (100 questions — treat differences as
  fragile until they clear a margin).

## Vendor context

Isaacus sells the Kanon embedders that "top" this benchmark — treat their leaderboard
as marketing context. The dataset artifact is neutral; we use it for our own sweeps.

## Status

Upstream verified and parked. Adapter (capture shaping + pass-through chunking +
golden build) NOT built — integration starts on explicit go. Its dataset id is
`vic-chargebook` (`instance_key = sha1("dataset:vic-chargebook")[:16]` at adapter
time); captures would land under `data/raw/<instance_key>/`. `upstream/` is
gitignored (disposable, re-fetchable, checksum-pinned); this file is committed.