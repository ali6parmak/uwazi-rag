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

## Adapter contract (when built)

- one capture PER PASSAGE — the passage is the atomic retrieval unit; its capture holds ONE
  paragraph (the passage text verbatim), so the gold anchor for a labeled passage is always
  paragraph position 0
- pass-through chunking (a dedicated `PassThroughChunker` in `chunking_methods/`): passages
  arrive pre-chunked, so one capture paragraph → one chunk, no merging/splitting; grading's
  byte-verify still re-chunks via the recorded chunk config (`passthrough 4096/on`), which on
  single-paragraph captures is byte-equal to the merge path
- **the `footnotes` field decision (recorded 2026-10-06 when this adapter landed):** footnotes
  ride along VERBATIM as a sidecar capture field — preserved for provenance and later
  attach/drop experiments, but NEVER chunked. Passage = upstream ships it (`text` only), so the
  instrument stays faithful to the published benchmark until a sweep argues otherwise. 1,907 of
  4,876 passages carry footnote material.
- ids unique + slash-free (checked at build); titles may repeat (2,761 unique over 4,876) —
  identity is the passage id, not the title

## Dataset identity (at adapter time)

- dataset id `vic-chargebook`; `instance_key = sha1("dataset:vic-chargebook")[:16] =
  c49c2465f4afa801`; captures under `data/raw/c49c2465f4afa801/` (4876 files, one per passage)
- golden/manual: `data/eval/datasets/vic-chargebook/{golden.jsonl, manual.jsonl}` (committed);
  golden row ids are `<passage-id>:qNNN` (passages asked twice exist — 5 of them)
- hand-authored unanswerables live in `manual.jsonl` (commit-time input, merged at build) and
  give the false-retrieval lens its substrate

## Status (adapter landed 2026-10-06, Step 4a)

Adapter BUILT: one capture per passage, pass-through chunking, golden rows by labeled passage;
spans/labels verified at build (100/100 labels resolve; checksums pinned in `checksums.txt`).
Currencies: hit-rate/MRR at passage level (pre-chunked corpus), plus doc-R as the same thing.
A first recorded sweep lands in `data/eval/results.md` under `— dataset vic-chargebook —` blocks
once Ollama is up. `upstream/` stays gitignored (disposable, re-fetchable, checksum-pinned);
`golden.jsonl`/`manual.jsonl` are committed, rebuilt byte-identically by `uwazi-rag dataset`.