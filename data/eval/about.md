# Golden dataset — generation recipe

Generated 2026-10-01 by `uwazi-rag build-golden`.

## Model

- LLM: Ollama chat 'glm-5.3-flash:cloud' at http://localhost:11434 (Ollama defaults, non-streaming)
- Ollama defaults (no temperature or options set on the request); non-streaming chat.

## Grouping rule (fixed, independent of the chunker)

- unit: consecutive keepable paragraphs (the chunker's drop rule) packed to ≤ 1200 chars;
  a single longer paragraph is its own (unsplittable) group
- anchor: `paragraph_ids` are 0-based positions in the raw capture (dropped paragraphs leave gaps);
  the scorecard maps them to chunks by re-chunking, so the dataset survives any chunk config

## Sampling rule

- 2 passage groups per capture, every capture answers; captures are
  per-language, so languages stratify for free
- seed: `"uwazi-rag/golden/v1/20261001/<instance_key>/<shared_id>/<language>"`, fixed draw order
  (group indices, then one cross-language flag per sampled group) — a re-run selects the same groups
- cross-language: a seeded 25% subset of sampled groups gets its questions
  generated in the other configured language (en, es),
  i.e. query_language ≠ expected.language

## Counts

| | |
|---|---|
"| captures seen / used | 77 / 77 |",
"| captures skipped (not ready / no groups) | 0 / 0 |",
"| passage groups built / sampled | 4254 / 152 |",
"| cross-language groups | 36 |",
"| groups generated / failed | 152 / 0 |",
"| rows written | 297 |",
"| rows deduped / rejected | not recorded (interrupted run — see provenance note) |",

## Failures (groups skipped during generation)

- recovered after the interrupted first run, take 2: bdd5a7c445847b35:z2vqw2dz73a:en:g0011 (2 rows, [en])
- recovered after the interrupted first run, take 2: bdd5a7c445847b35:zqp8i6fz02c:en:g0000 (2 rows, [en])

## Question-generation prompt (verbatim)

```text
You are building a search test set. Below is an excerpt from a human-rights document.
Write the questions in: {query_language}
Write 2 questions that a real person might type into a search box, which this excerpt
answers, and which it answers BETTER than other documents would. Rules:
- one very specific question, one broader/vaguer question
- max ~20 words each, natural phrasing
- don't copy 5 consecutive words from the excerpt
- return strict JSON only: [{{"form": "specific", "question": "..."}}, ...]
Excerpt (title removed, just text):
{passage_text}
```

## Row schema

`{id, question, origin, query_language, source_group_id, expected: {instance_key, shared_id, language, file_id, paragraph_ids, text}}`

- `origin`: `synthetic` (LLM-drafted) or `manual` (hand-written, merged via
  `uwazi-rag build-golden --merge-manual`).
- unanswerable manual rows (a real topic the corpus does not contain) carry
  `"source_group_id": null, "expected": null`; the scorecard expects nothing relevant for them.
- `manual.jsonl` starts as an origin-example schema template; the reviewed dataset
  has human-written `manual` rows in its place.
- `passages.jsonl` holds the sampled groups (ground truth for review; paragraph ids indexed
  as above) and is derived/disposable, so it is gitignored. `golden.jsonl`, `manual.jsonl`,
  `about.md` are committed.

## Provenance note

- The first generation run was killed by a tool timeout after 149/152 sampled groups; salvage
  passes re-ran the exact pipeline functions for the interrupted groups (takes 1-2 mis-set their
  query language; take 3 removed the 4 affected rows and re-drafted them in the language the
  seeded plan assigns).
- Rows rejected/deduped *during* the interrupted run were counted only in that process and are
  not recorded here; every row on disk passed the validator and the global question dedup.
- 7 groups carry 1 question (the second draft was rejected), the rest carry 2.
- Cross-language rows on disk: 69 (query_language ≠ expected.language).

## Review & manual rows (2026-10-01)

Human verification pass, as the step requires.

Synthetic triage: of the 297 draft rows, 42 were deleted after review —
4 had a referent a reader could not know ("this case", unnamed "the petition" /
"the judge" / "the petitioner"), 13 were yes/no quiz questions with no distinctive
anchor, 25 were questions the whole corpus answers equally well. Borderline rows
that carry a distinctive anchor stayed (e.g. GNRD, REDD+, "artículo 388", the 1998
suspended-sentence appeal). A re-run of the ≥5-word copy check found no verbatim
passage-quote survivors. 255 synthetic rows remain.

Manual rows: 15 appended (origin `manual`, ids `m001`–`m015`; re-running
`build-golden --merge-manual` skips them as already-merged):

- 3 keyword-literal probes quoting exact distinctive terms: "Serie A No. 2"
  (OC-2/82's citation label — lives in the doc title, so it also tests chunk-header
  indexing), IACHR case number 11.769 (registration date, Report 27/08), and
  Law 1084 (the 180-day judgment deadline in Report 58/14).
- 3 paraphrases written to near-zero token overlap with their gold passage
  (audited offline against `expected.text`): the born-alive termination statistic
  (European Centre for Law and Justice), the Dow/UCC summons (Amnesty, Bhopal),
  the 1972 Peirano fraud (Report 123/06).
- 2 cross-language rows (query_language ≠ expected.language), both en → es:
  carbon credits / conservation funds on indigenous land (AIDA + partners statement,
  the only es-only REDD coverage), and Dial vs Trinidad & Tobago's Port-of-Spain
  cell counts (no en capture of that case exists).
- 2 broad topical word-bag queries of the kind a busy user types:
  "police violence recommendations" (Report 26/09) and
  "electronic waste and human rights" (Human Rights Advocates statement).
- 2 metadata-ish rows whose answer lives in the chunk header (title + template,
  which v1 does index) — expectations modest: the author of the Iranian
  minority-rights written statement, and OIM/UNICEF as the repatriation
  protocol's co-publishers.
- 3 unanswerable rows — real topics absent from all 77 captures (verified by
  grep): Guantánamo Bay detention, treatment of Rohingya people, North Korean
  political prison camps. `"source_group_id": null, "expected": null`, en × 2 /
  es × 1; the scorecard must treat them as expected-nothing-relevant.
