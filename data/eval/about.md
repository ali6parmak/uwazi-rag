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
  `uwazi-rag build-golden --merge-manual`). The two `"example"` rows in `manual.jsonl`
  are schema demos and are never merged.
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
