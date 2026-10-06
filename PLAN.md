# Uwazi RAG — step-by-step build plan

This plan is written for a first real RAG project. Work through it **one step at a time**,
each step ends with something that actually runs. Every step has a short "Learn" section
explaining the idea behind it, in plain words.

Copy this file and `AGENTS.md` into the root of the new project when you scaffold it (Step 0).

---

## What we are building

A standalone service (working name: `uwazi-rag`) that:

1. **Reads** documents and metadata from a Uwazi instance (via its HTTP API, using the
   `uwazi-API` Python package).
2. **Understands** them: turns text into embeddings (lists of numbers that capture meaning)
   with Ollama models, and stores them in a vector database.
3. **Searches by meaning**: "witness enforced disappearance" finds documents that say
   "testigo desaparecido" — across languages, without exact keyword matches.
4. **Answers questions** with citations that link back into Uwazi
   (`/{language}/entity/{sharedId}`, down to the page number).
5. Later: serves **many Uwazi instances** from one place (the global repository direction).
   We build for one local instance now, but never hardcode "one instance" into the core.

Two products come out of this:

- **Semantic search** — ranked entity results (`sharedId`s) for the Uwazi search bar.
- **RAG answers** — natural-language answers, cited with entity + page.

## What this plan assumes

- A local Uwazi installation you control (you can edit its code and env vars).
- Ollama for models (embeddings + chat). Cloud models via your Ollama subscriptions can be
  swapped in later — everything model-related sits behind a port, so it stays swappable.
- The `uwazi-API` package installed from the sibling repo as an editable dependency.
- The Uwazi team will own real Uwazi-side changes long-term; our Uwazi-side work stays small,
  feature-flagged, and shaped so it could become an upstream PR.

## Facts this plan relies on (verified in the source)

- `sharedId` is the identity of an entity across all its language rows. It is the key your
  service returns to Uwazi.
- Uwazi extracts PDF text server-side. Rich, page-aware paragraph data is available at
  `GET /api/v2/files/:id/segmentation` (admin credentials needed; requires the segmentation
  feature). Raw PDFs are downloadable at `GET /api/files/:filename`. Per-page extracted text
  also exists in Mongo (`files.fullText`) but is not served over HTTP.
- Uwazi's AI assistant feature calls an external service with a simple job contract:
  `POST {url}/api/v1/jobs` with `{message, credentials: {url, username, password}}` →
  `{job_id}`, then polls `GET {url}/api/v1/jobs/{job_id}` →
  `{job_id, status: pending|running|completed|failed, result}`
  (see `uwazi/app/api/aiAssistant/infrastructure/ExternalAIAssistantService.ts`).
  Your `uwazi_agent` REST driver already implements exactly this contract — copy it.
- Change signals: every save/delete writes a row in the Mongo `updatelogs` collection
  (`{namespace, mongoId, timestamp, deleted}`) — this is what Uwazi's own sync worker uses.
  Entities also have a numeric `editDate` that grows on every edit.
- Permissions: an entity is visible to anonymous users only when `published`. We index
  **published entities only** in v1.
- Uwazi once had a semantic search integration (remnant: `uwazi/app/api/config/semanticSearch.ts`,
  `SEMANTIC_SEARCH_URL`) — so an upstream search-bar contribution has precedent.

## Golden rules (best practices, distilled)

1. **Thin vertical slices.** Every step ends with something that runs end-to-end. No step
   builds "half a layer".
2. **Retrieval before generation.** A good answer is impossible without good retrieval.
   Build and measure retrieval first; generation is the easy part.
3. **Ports and pure functions.** Anything external (Ollama, Postgres, Uwazi HTTP) sits behind
   a port (interface). All logic (chunking, prompt building, citation formatting, ranking)
   is pure and testable offline.
4. **The index is disposable.** It must always be rebuildable from Uwazi alone. The pipeline
   is the product, the index is a cache.
5. **Published-only in v1.** Never leak unpublished content through search results.
6. **Cite only what you retrieved.** The answer model may only reference sources we gave it.
   If retrieval found nothing relevant, the answer is "not found in this collection".
7. **Model names and vector sizes live in config.** Never hardcoded, never assumed.
8. **Chunk identity = `(instance_key, sharedId, language, file_id, chunk_index)`.**
   `instance_key = sha1(instance_url)[:16]` — the same trick as `uwazi_property_filler`.
9. **Measure before tuning.** The eval harness (Step 7) gates every change to chunking,
   embeddings, or prompts. No "it feels better" changes.
10. **Reuse, don't rebuild.** The `uwazi-API` package already solved Uwazi auth, paging,
    file/segmentation fetching, metadata flattening, retry/backoff, and LLM provider ports.

## How to work with an AI assistant on this plan

- Do **one step at a time**. Paste the whole step into the AI, plus the paths of files it
  should read or copy from (the cheat sheet at the bottom lists them).
- For each step, ask for **domain models and tests first**, then implementation. Tests use
  real captured data as fixtures (Step 1 produces them), so they run offline with no mocks.
- After each step: run the CLI yourself, run the new test file
  (`python -m pytest src/uwazi_rag/tests/test_<module>.py -v`), commit.
- When a Uwazi behavior surprises you, verify in `uwazi/` source or in the sibling repo's
  `.notes/` files (mostly correct, somewhat stale — double-check against code).
- Ask the AI to **explain why** for every choice. You are learning RAG, not just shipping it.
- When you change chunking, embedding model, or prompt: run the eval harness before/after
  and keep the numbers in `data/eval/results.md`.

---

## The plan at a glance

| # | Step | You'll have… | New thing you learn |
|---|------|--------------|---------------------|
| 0 | Skeleton + Ollama | runnable project, first embedding printed | project shape, what an embedding is |
| 1 | Fetch one document | real Uwazi text saved as a fixture | the Uwazi data plane (segmentation) |
| 2 | Chunking | tested chunk builder | chunk size, overlap, context headers |
| 3 | Naive search | CLI search over one document | cosine similarity, top-k |
| 3.5 | Eval harness, early | golden set + recall/MRR scorecard on the 77-doc index | measurement before scale |
| 4 | Index a collection | whole template indexed | pipelines, idempotency, caching |
| 5 | pgvector + hybrid | real vector store with keyword fusion | ANN indexes, hybrid search, RRF |
| 6 | Answers + citations | `ask` command with linked sources | grounding, prompt design |
| 7 | Eval harness | scorecard over a golden question set | recall@k, MRR, regression testing |
| 8 | HTTP service | running API with the Uwazi job contract | async jobs, service design |
| 9 | Bert panel | answers inside Uwazi's UI | proxy pattern, per-user credentials |
| 10 | Incremental sync | index stays fresh as Uwazi changes | change feeds, cursors |
| 11 | Search-bar mode | semantic toggle in the Uwazi library | feature flags, upstream-shaped patch |
| 12 | Global repository | design doc for multi-instance | tenancy, hosting |

Phases: A = steps 0–4 (core in the terminal), B = 5–8 (production-shaped core),
C = 9–11 (plug into Uwazi), D = 12 (future direction).

---

## Step 0 — Project skeleton + first embedding

**Goal:** a runnable project and proof that Ollama can turn text into numbers.

**Build:**
- `uv init` a new repo (Python 3.12+), src layout, hatchling — same style as `python_uwazi_API`.
- Package `src/uwazi_rag/` with the folders: `domain/`, `adapters/`, `use_cases/`, `drivers/`
  (plus `configuration.py` reading env vars).
- Dependency on the sibling project, editable:
  ```toml
  [project]
  dependencies = ["uwazi-API", "fastapi", "uvicorn", "pydantic", "loguru", "httpx", "numpy", "psycopg[binary,pool]"]

  [tool.uv.sources]
  uwazi-API = { path = "../python_uwazi_API", editable = true }
  ```
- CLI entry point `uwazi-rag` (stdlib `argparse` is fine) with subcommands. Most start as
  stubs: `fetch`, `index`, `search`, `ask`, `eval`, `serve`, `sync`.
- Env file (`.env`, never committed): `UWAZI_URL`, `UWAZI_USER`, `UWAZI_PASSWORD` (admin —
  segmentation needs it), `OLLAMA_BASE_URL` (default `http://localhost:11434`),
  `EMBEDDING_MODEL=bge-m3`, `SERVICE_PORT=5060` (siblings use 5051/5054/5055/5056/7050 —
  avoid collisions).
- Copy `AGENTS.md` (from this folder) into the repo root, next to this `PLAN.md`.
- `ollama pull bge-m3` — a multilingual embedding model (human rights collections are rarely
  single-language). Check `ollama list` for what you already have.
- First command: `uwazi-rag hello` → calls Ollama's `POST /api/embed` with a sentence and
  prints the vector length (1024 for bge-m3) and the first few numbers.
- One trivial pytest to confirm the test setup.

**Learn:** an *embedding* is a list of numbers describing meaning. Similar meanings → similar
number lists, regardless of language or wording. The number of values (dimensions, here 1024)
is a property of the model — read it from config, verify it at startup with a probe embed.
Some model families want prefixes like `"query: "` / `"passage: "` in front of text (the E5
family does; bge-m3 does not) — check the model card before switching models.

**Done when:** `uv run uwazi-rag hello` prints a 1024-length vector, and `uv run pytest` is green.

---

## Step 1 — Pull one real document's text out of Uwazi

**Goal:** real data in hand, captured as a reusable fixture.

**Build:**
- Use `UwaziClient` (from `uwazi_api`) to log in to your local instance.
- Find an entity that has a PDF: `client.search` with a `types` filter (template id) or a
  `searchTerm`.
- Fetch its segmentation: `FileService.get_segmentation(...)` in
  `python_uwazi_API/src/uwazi_api/use_cases/file_service.py` — it already handles the
  entity-language ↔ document-language mismatch (`en` vs `eng`, see
  `uwazi_api/domain/constants.py`).
- Save to `data/raw/<instance_key>/<sharedId>_<language>.json`: entity title, template name,
  and the segmentation paragraphs (`text`, `pageNumber`, position fields).
- Save the **same JSON under `tests/fixtures/`** — this real captured data powers your
  offline unit tests from Step 2 onward (fits the AGENTS.md testing policy: no network, no
  mocks, real data as fixtures).
- Command: `uwazi-rag fetch <sharedId> --language en`.

**Learn:** the *data plane*. Uwazi already ran PDF extraction for us — the segmentation is
page-aware paragraph text, which is exactly what we need for citable chunks. Note the
immutability rules the sibling repo discovered: a file's storage filename never changes
content (uploads mint new names), and a `ready` segmentation for a given `file_id` never
changes — so both are safe to cache forever. If an entity has no segmentation (feature off,
or a scanned PDF with no text layer), record that; Step 4 handles it.

**Done when:** the fetch command writes the JSON and prints the paragraph count; the fixture
file exists in `tests/fixtures/`.

---

## Step 2 — Chunking (pure logic, first real tests)

**Goal:** turn paragraphs into retrieval-sized pieces with identity and context.

**Build:**
- Domain model `Chunk`: `chunk_id`, `instance_key`, `shared_id`, `language`, `file_id`,
  `chunk_index`, `text`, `page_start`, `page_end`.
- Pure function `build_chunks(segmentation, entity_context) -> list[Chunk]` in
  `domain/` or `use_cases/`. Rules to start with (tune later **with the eval harness**):
  - Merge adjacent paragraphs until roughly 1,200–1,800 characters (≈ 300–500 tokens in most
    languages). Split anything longer.
  - Add a small overlap (~15%) when splitting, so a sentence cut in half is still findable.
  - Prepend a context header to each chunk, e.g.
    `"{entity title} — {template name} (page {n})"`. A chunk alone often loses "who/what this
    is about"; the header restores it at embedding time.
  - Record the page range (from the paragraphs' `pageNumber`).
- Tests from the Step 1 fixture: chunk counts stable, no text lost (concatenated chunks
  contain all paragraph text), page ranges correct, long paragraphs split, tiny ones merged.

**Learn:** *chunking* is the highest-leverage, least glamorous part of RAG. Small chunks =
precise matches but lost context; large chunks = full context but the meaning gets diluted
("a little bit about everything"). Overlap protects sentences that straddle a cut. The
context header is a cheap trick that fixes the most common failure ("found a paragraph, but
about the wrong document"). You will revisit these numbers in Step 7 — that's normal.

**Done when:** tests pass on the fixture; `uwazi-rag fetch ... && <chunk cmd>` prints chunk
count, average size, and page coverage for your document.

---

## Step 3 — Embed and search, the naive way (on purpose)

**Goal:** your first working semantic search — and an understanding of what a vector
database actually does for you.

**Build:**
- Port `EmbeddingPort` with method `embed(texts: list[str]) -> list[list[float]]`.
- Adapter `OllamaEmbeddings` calling `POST {OLLAMA_BASE_URL}/api/embed` with
  `{"model": EMBEDDING_MODEL, "input": [...]}` (input is a list → batching for free).
- `NaiveVectorStore`: holds `(chunk, vector)` pairs in memory; search = cosine similarity
  (numpy) against every vector, return top-k. Persist to a JSON file so you don't re-embed
  during dev.
- Command: `uwazi-rag search "your question" --file data/raw/...json` → embeds query, compares,
  prints top-5 chunks with entity title, page number, and similarity score.

**Learn:** *cosine similarity* compares the direction of two vectors, not their length —
"how close in meaning". A naive scan is O(n); fine for thousands of chunks, hopeless for
millions. This step exists so you feel exactly what a real vector database adds: a smart
index (ANN — approximate nearest neighbors — fast but not exhaustive), persistence, and
metadata filtering. Keep this naive store forever — it becomes your offline test double.

**Done when:** you search for something in a *different language* than the document, and the
correct paragraphs come back. That's the "it works" moment of embeddings.

---

## Step 3.5 — Eval harness, early (a 77-document measuring stick)

**Goal:** before mass indexing makes every experiment expensive, build the scorecard that
turns "my chunks feel fine" into recall@k and MRR numbers — then use it to settle chunking
and embedding-model decisions *before* Step 4 commits thousands of chunks to disk. Runs
entirely on the existing 77-capture / 2,850-chunk index; no new infrastructure beyond one
thin port.

**Build:**
- A thin `LlmPort` (`ports/llm_port.py`) + `OllamaLlm` adapter (`POST /api/chat`, no
  streaming) — fleshed out in Step 6; the golden builder only needs "answer this prompt".
  The LLM model name comes from config (`LLM_MODEL` in `.env`; any instruct model already
  pulled in Ollama works — config, never code).
- `use_cases/passage_groups.py` + `use_cases/build_golden.py`: questions anchor to
  **paragraphs**, never to chunk ids — chunk anchors die the moment the
  `--max-chars`/`--overlap` sweep changes the chunker, paragraph anchors survive any chunk
  config. The grouping unit is a *passage group*: consecutive keepable paragraphs (same
  drop rule as the chunker, shared code not a copy) packed up to ~1,200 chars; a single
  longer paragraph is its own (unsplittable) group. Keepable paragraphs are anchored by
  their 0-based position in the raw capture (dropped paragraphs leave gaps) — the
  deterministic canonical index. Sampling is
  seeded/deterministic: 2 passage groups per capture, every document covered, stratified
  by language (captures are per-language); a seeded 25% subset of groups gets its
  questions generated in the **other** language (cross-language rows, previewing
  cross-language recall). One LLM call per group asks for exactly 2 questions (one very
  specific, one broader/vaguer, ≤ ~20 words, natural phrasing, no 5-consecutive-word
  copies from the excerpt, strict JSON array), excerpt WITHOUT title/header/page numbers.
  `data/eval/golden.jsonl` rows:
  `{id, question, origin, query_language, source_group_id, expected: {instance_key,
  shared_id, language, file_id, paragraph_ids, text}}` — self-grounded by construction:
  the passage a question was generated *from* is its gold pair. Known bias ("self-echo":
  the question shares vocabulary with its passage, inflating absolute scores) — push
  against it with the specific/broader pair, generate from passage text *without the
  header*, and treat scores as **relative** (config A vs config B), never absolute.
  Stratified-by-subgroup scoring waits for Step 4 (the subgroup label isn't recorded in
  captures yet).
- `uwazi-rag build-golden` writes: `golden.jsonl` (the synthetic draft), `passages.jsonl`
  (the sampled groups — derived/disposable, gitignored), `about.md` (the full recipe:
  model, defaults, prompt text, sampling rule, counts, date) and `manual.jsonl` — a
  2-example-row template (`origin: "example"`, shown for schema only, never merged).
  `--merge-manual` is a merge-only mode (no LLM calls): it validates hand-written rows
  (`origin: "manual"`, must reference a real `source_group_id`) and appends them to
  `golden.jsonl`, keeping manual rows separable by origin. Generated rows are streamed to
  a temp file and renamed on completion, so a killed run never corrupts the previous
  dataset; individual group failures (unparseable reply, junk questions) are counted and
  skipped, never fatal.
- **Human verification is part of the step:** sample-review the synthetic rows, delete
  junk, and hand-write ~15–20 questions into `data/eval/manual.jsonl` (`origin: "manual"`;
  the Step 3 cross-language demo query is already #1). `data/eval/` is committed
  versioned material (an exception to "data is disposable", already carved out in
  `.gitignore`).
- `use_cases/eval_retrieval.py` (pure): golden rows anchor `paragraph_ids`, so first map
  expected paragraphs → `chunk_id`s under the chunk config being graded, then from ranked
  `chunk_id`s → **recall@k** and **MRR**, reported at *both* chunk level and document
  level. Document-level keeps comparisons fair across chunk sizes (bigger chunks trivially
  inflate chunk-level recall); chunk-level shows precision of the granule itself.
  Aggregate per language.
- `uwazi-rag eval --label "…" (--store …)` un-stubs: embeds every golden question,
  retrieves top-k from a store, prints the scorecard, appends a dated row to
  `data/eval/results.md` (append-only log — re-run freely, never overwrite).
- `build-index` grows a small benchmark surface: `--max-chars`, `--overlap`, `--no-header`
  (defaulting to the Step 2 constants from `use_cases/chunking.py`). Chunking parameters
  were hypotheses until now; this step is where they become decisions.
- The benchmark protocol: fix `golden.jsonl`; sweep chunk configs, then Ollama embedding
  models (bge-m3 vs shortlisted alternates, e.g. `nomic-embed-text` / arctic-embed-class,
  one store per model — the store's model/dims fingerprint keeps them apart); record both
  sweeps in `results.md` and let the numbers pick what Step 4 ships with.
- Optional external cross-check (embedding-model shortlist ONLY): a ready-made bilingual
  retrieval set in BeIR format (e.g. MIRACL-es or mMARCO-es), run from a throwaway script
  outside the core pipeline as a second opinion on the model ranking. It never gates
  chunking or pipeline decisions — foreign questions can't vote on foreign-corpus shape —
  and the in-domain protection (hand-written rows + the post-Step-4 scale-up re-check)
  stays the real anti-overfit device. Skip it unless two models tie on the golden set.

**Learn:** a small in-domain harness beats any public benchmark here — the questions users
ask human-rights collections only resemble those collections, and recall@k against a
corpus you didn't index is meaningless. Synthetic-question generation converts labeling
labor into compute; verification labor replaces authoring labor. Relative scores from
biased-but-shared questions are still fair races — the hand-written rows are the
tiebreaker when two configs look equal.

**Done when:** `data/eval/golden.jsonl` (verified) is committed; `data/eval/results.md`
has ≥2 recorded sweep blocks (one chunking, one embedding-model) with a chosen default;
Step 4 inherits those parameters.

---

## Step 3.6 — Scorecard honesty: currencies, readable stores, and the labeled-data dependency

**Goal:** before more experiments run, make the scorecard honest about *what each number
counts* — what you ship (chunks), what you need (the decider at document level), and what
the reader actually saw (paragraphs) — without changing any previously recorded number.

**Built (RECORDED — data/eval/results.md, commits 8425b31…cb02968):**

- New pure metrics on the golden rows (offline-tested worked examples in
  `tests/test_eval_retrieval_currencies.py`):
  - `cov@k` — paragraph currency: anchor paragraphs covered in top-k, a paragraph counts
    iff ANY chunk holding it is retrieved; denominator = the row's own anchors, so it is
    packaging-immune. A *lens* on one experiment; the cross-chunker decider stays the
    document level. Split paragraphs need one piece; chunk recall needs them all.
  - `cov@3000` (`COVERAGE_CHAR_BUDGET`) — same lens at a fixed retrieved-char budget:
    whole chunks pack from rank 1 while the running char total stays ≤ the budget
    (inclusive; prefix semantics — a later small chunk never rescues an overflow). Kills
    the "top-k means different text amounts" leak between packing sizes.
  - `P@k` (`|gold ∩ top-k| / k`) and `RP` (precision at `k = |gold|`; BeIR standard) —
    chunk currency: recall asks how much of the gold was collected, P asks how much of
    what was shipped was gold (the waste counter). `RP = 100%` iff the first `|gold|`
    slots are entirely gold.
- The honesty caveat is stamped on every block: the gold is self-anchored (questions were
  drafted from the passage they quote), so P/RP read systematically *pessimistic* —
  comparisons only, never absolute quality.
- `RowGold` grew additively (anchor paragraph ids + per-paragraph chunk grouping;
  unmapped anchors keep their slot and can never be covered); `eval_run.py` stayed
  byte-identical — parity is the acceptance criterion and the fresh 5-model sweep met it
  (bge-m3 / nomic-v2-moe / embeddinggemma EXACT vs the recorded comparison; the qwen
  models drift within the already-recorded non-bit-stable family).
- Readable store names replace raw fingerprint hashes:
  `<method-slug(params)>__<model-slug>-<corpus-digest8>.json` (e.g.
  `merge-1800-0.15-on__bge-m3-4d284af0.json`). Deterministic (same inputs → same file,
  cross-sweep sharing kept); validity stays content-based (recorded model + chunk_config
  + the byte-verify guard), never name-based.

**Decisions recorded at this step (user):**

- **No absolute model is "decided".** The benchmark layer is the decision instrument;
  models are compared per experiment and the config stays a knob. Verdict blocks in
  results.md remain valid as snapshots at recording time, not permanent picks.
- **Skip per-model threshold re-derivation** (qwen3-8b m013 crossing 0.55): noted, and
  not needed yet — FALSE_RETRIEVAL_THRESHOLD stays the one global config value.
- **Step 4 is re-scoped, not dropped — it now waits for labels.** Indexing thousands of
  Uwazi entities adds no gradable signal without relevance labels, and hand-labeling a
  human-rights corpus is not realistic (one person, non-expert domain). A new, properly
  labeled RAG dataset is being sourced; when it arrives, Step 4 is redefined around
  integrating it. Two facts to plan that work around:
  - The Uwazi-side plumbing (inventory paging, published-only, segmentation cache,
    idempotent chunk→embed→store) is dataset-independent — it is proven at 77-capture
    scale and carries over unchanged when the service goes live at scale.
  - The integration seam is a golden-format adapter: external relevance labels (often
    document- or paragraph-level qrels) must be mapped onto this grading path — the
    harness, metric engines and store naming all survive as-is.
- **Chunker exploration is parked behind the same dependency:** `RawChunker`,
  registry/self-describing stores in `NOT IN SCOPE` notes, and candidate `drop_footnotes`/
  `section` methods start once better labels exist to judge them on.
- **Candidates sourced and homed (2026-10-06):** two upstream corpora are verified
  (checksums) and parked under `data/datasets/*/upstream/` with committed provenance in
  each home's `about.md` — `legalbenchrag` (Pipitone & Houir Alami 2024: raw contracts,
  expert char-span labels; planned per-source ids `legalbenchrag-cuad`/`-contractnli`/
  `-maud`/`-privacyqa`; MAUD gated on its unverified license) and `vic-chargebook`
  (Isaacus's Legal RAG Bench: 4,876 fixed passages + 100 expert Q/A rows; pre-chunked
  corpus → currencies collapse to hit rates there, by design). Adapters and sweep specs
  are NOT built — integration starts on explicit go. Both are English-only; the
  Spanish hunt continues.

**Learn:** a metric's honesty lives in its denominator — fixed denominators (the row's own
anchors; the char budget; the demand size `|gold|`) make races fair, because then only
retrieval quality moves the number. And a benchmark *system* beats a "chosen model": a
picked default freezes one experiment's result into a constant, while a recorded sweep
keeps every comparison re-runnable as data arrives.

**Done when (met):** coverage/precision/RP implemented + tested (suite 165), readable
store names live, parity block recorded in results.md, plan updated; then STOP for user
review. Next work resumes once the new labeled dataset is selected.

---

## Step 4 — Index a whole collection

> **Status (2026-10-05): on hold — re-scoped around an external labeled RAG dataset;
> see Step 3.6.** The build below stays the eventual Uwazi-side shape; the labeled-
> evaluation half is redefined when the dataset is chosen.

**Goal:** from one document to a template's worth of content, resiliently.

**Build:**
- `use_cases/index_collection.py`:
  1. **Inventory:** page through `/api/search` filtered by template (the client handles the
     ES 10,000-result window paging). Published entities only.
  2. **Extract:** per entity, fetch segmentation (cached on disk forever — see Step 1's
     immutability rules).
  3. **Classify:** entities with text → chunk; entities without a document (metadata-only) →
     one chunk from title + flattened metadata values (thesaurus labels — the sibling repo has
     three implementations of Uwazi metadata flattening; reuse one, see cheat sheet);
     scanned/no-text → mark `needs_ocr`, don't fail.
  4. **Chunk → embed (in batches) → store.**
- Re-runnable: same input always produces the same `chunk_id`s; re-running overwrites, never
  duplicates. Progress logging (entity count, failures).
- Command: `uwazi-rag index --template <id>` (and `--all`).

**Learn:** the *pipeline* shape: inventory → extract → chunk → embed → store. Idempotency
(run it twice, nothing breaks) and resilience (one bad entity logs an error, the run
continues). This is also where rate-friendliness matters — the sibling client already has
retry/backoff; if you parallelize fetches, copy the adaptive-throttling executor from
`uwazi_admin_agent` (drops workers on 429s, adds them back when clean).

**Done when:** indexing a template completes on your instance; a search across the
collection returns sensible hits from multiple entities.

---

## Step 5 — Real vector store (Postgres + pgvector) and hybrid search

**Goal:** the production-shaped storage, plus the single biggest retrieval upgrade: hybrid
search.

**Build:**
- Postgres with the extension preinstalled: `docker run pgvector/pgvector:pg16`
  (you already run a Postgres for `uwazi_property_filler`; same patterns apply).
- Table `chunks`: identity columns from the `Chunk` model + `embedding vector(1024)` +
  a full-text column (`to_tsvector(language, text)`), `instance_key` column, HNSW index on
  the embedding. Apply schema from a `schema.sql` at startup (copy `uwazi_property_filler`'s
  approach).
- Port `VectorStore` (search/upsert/delete) — `NaiveVectorStore` from Step 3 now implements
  it too, for tests.
- `PgVectorStore` with two queries per search: vector similarity (pgvector `<=>` cosine
  distance) + keyword match (`websearch_to_tsquery`), then fuse the two ranked lists with
  **RRF**: `score = 1/(60 + rank_vector) + 1/(60 + rank_keyword)` (rank starts at 1).
- Metadata filters: language, template, instance_key.
- Switch the CLI to Postgres; the naive store stays for unit tests.

**Learn:** *hybrid search* = meaning (vectors) + exact terms (keyword). Vectors are weak at
exact things: statute numbers, article numbers, names, abbreviations — a keyword match
catches those. RRF (reciprocal rank fusion) merges two ranked lists by rewarding things that
rank high in either one — dead simple and hard to beat. True BM25 scoring is a later
upgrade (e.g. ParadeDB's `pg_search`) if the eval harness says you need it. This is also
your first taste of *metadata filtering* — the same mechanism that will enforce permissions
later (filter by template, language, and eventually per-user access sets). Also: the
harness from Step 3.5 grades the migration itself — vector search over pgvector on the
golden questions must match or beat the naive scan it replaces.

**Done when:** the same query works against Postgres; a keyword-heavy query (e.g. a specific
article number) now finds exact matches that pure vector search missed.

---

## Step 6 — Answers with citations (the "G" in RAG)

**Goal:** question in, grounded answer out, every claim traceable to an entity and page.

**Build:**
- Port `LlmPort` (copy the design from `uwazi_agent/adapters/llm/` — Ollama adapter
  included; your cloud-model subscriptions slot in here later).
- `use_cases/ask.py`:
  1. Embed the question, hybrid-retrieve top-k chunks (start with k=8).
  2. Order chunks **best first** in the prompt (models pay more attention to the beginning;
     the "lost in the middle" effect).
  3. Prompt: sources listed with numbers `[1] {title} (page {n}): {chunk text}`; system rules:
     *answer only from the sources; cite every claim as [n]; if the sources don't answer it,
     say so; low temperature*.
  4. Parse `[n]` markers → `Citation {shared_id, title, page, url = /{language}/entity/{shared_id}}`.
  5. Render answer + citation list as markdown.
- Command: `uwazi-rag ask "question"`.
- Hard rule (see Golden rules): the answer may only cite retrieved chunks. No retrieval →
  "I couldn't find this in the collection." — never a generic LLM answer.

**Learn:** *grounding*. Generation is easy; grounding is discipline. The citation rule is
your hallucination firewall: the model can't invent sources it was never given. Temperature
low (0–0.3): we want an extractive, faithful assistant, not a creative one. If answers are
verbose or miss things, resist tuning the prompt first — check the retrieval step with the
harness (Step 7) before touching prompts.

**Done when:** `ask` returns an answer where every citation resolves to a real entity + page
in your collection, and an unanswerable question returns "not found", not fiction.

---

## Step 7 — Evaluation harness (do not skip)

**Goal:** numbers that tell you whether retrieval/answers got better or worse.

**Build:** (Step 3.5 already built the harness early, on the 77-document index — `LlmPort`,
the golden builder, `eval_retrieval.py`, the `eval` CLI, and the chunk-parameter knobs.
This step runs it at scale and keeps it as the regression gate.)
- `data/eval/golden.jsonl`: merge your hand-written rows into Step 3.5's verified
  synthetic set; after Step 4's full indexing, extend with questions written directly
  against the indexed templates, each with the expected `sharedId`(s). Mix: keyword-y
  questions, paraphrases, wrong-language questions, one or two answerable-only-with-
  metadata questions, a couple with no good answer (should return "not found").
- Command `uwazi-rag eval`:
  - Retrieval metrics: **recall@k** (did the expected entity appear in top-k?) and **MRR**
    (mean reciprocal rank — 1.0 if expected hit is always first, ~0 if deep in the list).
  - Answer check: citation faithfulness — spot-check manually, or ask the LLM to judge
    "is this claim supported by this cited chunk?" (LLM-as-judge; still cheap).
  - Prints a scorecard; appends a dated row to `data/eval/results.md`.
- This runs against **real** Ollama + your instance, on demand — it is *not* part of pytest
  (the AGENTS.md testing policy stays intact; the harness is a tool, not a test).

**Learn:** RAG regressions are **silent** — nothing crashes when retrieval quality drops;
answers just get subtly worse. recall/MRR separate "did we find the right stuff" (retrieval)
from "did we phrase it well" (generation). From now on: change chunk size → run eval;
swap embedding model → run eval; edit prompt → run eval. You'll likely do a small sweep of
chunk sizes and k here — that's the harness doing its job.

**Done when:** the full-index scorecard runs stratified (language, and subgroup once the
Step 4 inventory records it) and is appended to `results.md` after every
chunking/retrieval/prompt change — the Step 3.5 baseline now becomes the standing
regression gate.

---

## Step 8 — HTTP service with the Uwazi job contract

**Goal:** the service Uwazi can actually talk to.

**Build:**
- FastAPI app (port from `SERVICE_PORT`, default 5060):
  - `POST /api/v1/jobs` — `{message, credentials: {url, username, password}}` → `202 {job_id}`.
    Runs `ask` in the background.
  - `GET /api/v1/jobs/{job_id}` → `{job_id, status: pending|running|completed|failed, result}`.
  - In-memory job store with TTL (copy `uwazi_agent/drivers/rest/` — same design).
  - `POST /api/v1/search` — `{query, filters?}` → `{results: [{sharedId, score, title, snippet, page, language}]}` (sync; for Step 11).
  - `GET /api/v1/status` — index stats (counts per instance/template, last sync).
- Keep credentials in memory only; never log them; treat them as Uwazi treats passwords.
- `uwazi-rag serve` runs it; health endpoint for sanity.

**Learn:** why the job contract is async — LLM answers take seconds-to-tens-of-seconds; the
caller (Uwazi) gets a `job_id` immediately and polls. And the key insight: **this exact
contract is what stock Uwazi already knows how to call** — verified in
`uwazi/app/api/aiAssistant/infrastructure/ExternalAIAssistantService.ts`. Your `uwazi_agent`
proved it works end-to-end. Also: why we take `credentials` — per-user permissions come for
free in the next step.

**Done when:** `curl POST /api/v1/jobs` + poll returns an answer with citations.

---

## Step 9 — Answers inside Uwazi: the Bert panel (zero Uwazi code changes)

**Goal:** a human asks a question **inside the Uwazi UI** and gets a cited answer.

**Build:**
- On your local Uwazi, set env vars (check exact names in `uwazi/app/api/config.ts` around
  L133–170): `FEATURE_FLAG_AI_ASSISTANT=true`, `AI_ASSISTANT_SERVICE_URL=http://localhost:5060`,
  and the external-services master switch if applicable (`EXTERNAL_SERVICES=true`).
- In the UI: the "Ask Bert" header button (Ctrl/Cmd+K) opens the chat panel; a password gate
  sends the *user's own* Uwazi password with the request; Uwazi's backend forwards
  `{message, credentials}` to your service.
- In your service, use those credentials to log into Uwazi **as that user** (the client makes
  this easy) and verify the candidate `sharedId`s you're about to cite before answering —
  `GET /api/entities?sharedId=...` respects permissions, so anything unpublished that
  slipped into your index gets filtered here. This is defense in depth on top of the
  published-only index.
- Answers render as markdown in the panel; entity links (`/{language}/entity/{sharedId}`)
  are plain markdown links and just work.

**Learn:** the *proxy pattern* — the browser never talks to your service directly; Uwazi's
backend does, server-to-server. No CORS, no exposed credentials, and the service URL is
per-tenant config. Also how credential forwarding gives you per-user permission enforcement
almost for free: you query Uwazi as the asking user, so you can't show them what they can't
see.

**Done when:** from inside Uwazi's UI, you ask a question about your collection and get a
cited, linked answer. Screenshot this — it's the milestone that makes the project real to
everyone else.

---

## Step 10 — Incremental sync (keep the index fresh)

**Goal:** edits in Uwazi show up in search without a full re-index.

**Build:**
- Primary (local, verified path): read the `updatelogs` collection directly from your
  instance's Mongo DB — `{namespace: 'entities'|'files', timestamp > cursor, deleted}` —
  exactly the mechanism Uwazi's own sync worker uses (`uwazi/app/api/sync/syncConfig.ts`).
  Store the cursor (last timestamp) in Postgres.
- For each changed entity: re-fetch → re-chunk → re-embed → upsert (same `chunk_id`s =
  overwrite) ; for deleted ones: delete chunks by `sharedId`.
- Caution (from the sibling repo's field notes): Uwazi search reads lag writes slightly
  (Elasticsearch bulk is not immediately refreshed). If you read via the API right after an
  edit, confirm freshness via `editDate` before re-indexing — the probe pattern lives in
  `uwazi_admin_agent/adapters/search_probe_adapter.py`.
- `uwazi-rag sync` command; run it from cron or a systemd timer every few minutes.
- Alternative (HTTP-only, for hosted later): poll the API by `editDate` — worth having, but
  DB access is trivial locally and `updatelogs` is the purpose-built feed.

**Learn:** *change data capture* thinking: full crawls bootstrap; change feeds maintain.
Cursors must be persisted; deletions must propagate; idempotent writes make "run it again"
always safe.

**Done when:** edit an entity in Uwazi → run `sync` → the new content is findable, without
touching the rest of the index.

---

## Step 11 — Semantic search in the Uwazi search bar (local patch, upstream-shaped)

**Goal:** the search-bar toggle from the original meeting notes — a ranked entity list from
your service, merged into normal library results.

Keep this a **small, flag-gated, stock-behavior-preserving patch** on your local Uwazi —
it is intended to eventually become a PR to HURIDOCS (they had a semantic search integration
once — precedent matters). The five seams (paths verified in the research):

1. **Feature flag:** `uwazi/app/shared/types/settingsType.d.ts` + `settingsSchema.ts`
   (features block) — add e.g. `semanticSearch: { active: boolean, url: string }`, copying
   the existing `convertToPdf` shape. Or go the env route like `aiAssistant`
   (`uwazi/app/api/config.ts` `featureFlags`).
2. **Flag to the frontend:** `uwazi/app/react/V2/shared/types.ts` (`ClientFeatureFlags`)
   + the `clientFeatureFlags` map in `uwazi/app/react/entry-server.tsx`.
3. **Toggle UI:** `uwazi/app/react/Library/components/SearchBar.tsx` — a small toggle chip
   next to the input, wrapped in `<FeatureToggle feature="semanticSearch">`.
4. **State:** the toggle rides the existing rison-encoded `?q=` URL (a `semanticSearch` key
   on `library.search` flows through `processFilters` automatically) — so it survives page
   reloads, shared links, and pagination.
5. **Backend route + hydration:** hook in `uwazi/app/react/Library/helpers/requestState.js`;
   new route modeled 1:1 on `uwazi/app/api/aiAssistant/infrastructure/express/AIAssistantRoutes.ts`
   (`needsAuthorization` + flag middleware): Uwazi calls your `POST /api/v1/search`, gets
   ranked `sharedId`s, **hydrates them inside Uwazi** via its own search (filter by
   `sharedId`s) so permissions are enforced and the frontend receives the standard
   `{rows, totalRows}` shape — the existing tiles/snippets render with zero new result
   components.

Keep the diff in a branch or a `.patch` file you can re-apply on Uwazi updates.

**Learn:** how feature flags travel (DB settings + env → SSR boot → atom/redux →
`<FeatureToggle>`), and why hydrating results *inside* Uwazi is the clean seam: your service
stays a pure ranking oracle that returns ids, Uwazi stays the source of truth for what a
user may see and how it's displayed.

**Done when:** with the flag on, the library search returns semantically-ranked entity
cards (with your snippets); with the flag off, behavior is byte-identical to stock Uwazi.

---

## Step 12 — The global repository (design doc, for later)

**Goal:** turn one-instance code into the multi-instance product — on paper first.

When single-instance works end-to-end, write a short design doc covering: an instance
registry (URL + admin credentials per instance, like `uwazi_property_filler`'s per-instance
config), indexing many `instance_key` namespaces from one set of tables, per-instance
embedding/model configuration, quota + cost tracking, deployment (where does it live? who
pays for the GPUs?), and cross-instance search (query one instance's collection vs. all).
Everything built in Steps 0–11 (`instance_key` everywhere, config-driven models, disposable
indexes, per-instance sync cursors) was chosen so this step is a deployment problem, not a
rewrite.

---

## Cheat sheet — what to reuse and where things live

**From `python_uwazi_API` (install as `uwazi-API`):**

| Need | Reuse |
|---|---|
| Uwazi login/session/CSRF, retries, paging | `uwazi_api/client.py` (`UwaziClient`) |
| Fetch PDF segmentation (language matching included) | `uwazi_api/use_cases/file_service.py` (`FileService`) |
| Segmentation domain model | `uwazi_api/domain/segmentation.py` |
| Metadata flattening (thesaurus labels etc.) | `uwazi_agent/adapters/uwazi_api/entity_mapper.py`, `uwazi_property_filler/domain/metadata_text.py`, or `uwazi_api/use_cases/entity_to_dataframe.py` — pick one |
| Paragraph → reading-order text rendering | `uwazi_admin_agent/use_cases/segmentation_tools.py` (`format_segmentation`) |
| LLM provider port + Ollama adapter | `uwazi_agent/adapters/llm/` |
| Job API design for Step 8 | `uwazi_agent/drivers/rest/` |
| Adaptive throttled parallelism | `uwazi_admin_agent/use_cases/parallel_executor.py` |
| Postgres store pattern + schema bootstrap | `uwazi_property_filler/adapters/postgres_store.py` + `schema.sql` |
| Per-instance namespacing (`sha1(url)[:16]`) | `uwazi_property_filler/configuration.py` |
| ES freshness probing after writes | `uwazi_admin_agent/adapters/search_probe_adapter.py` |
| Uwazi API field behavior (stale but mostly right) | `python_uwazi_API/.notes/*.md` — verify surprises against `uwazi/` source |

**In `uwazi/` (integration seams, for Steps 9 and 11):**

| Seam | Path |
|---|---|
| AI assistant route pattern | `app/api/aiAssistant/infrastructure/express/AIAssistantRoutes.ts` |
| External job contract (what Uwazi calls) | `app/api/aiAssistant/infrastructure/ExternalAIAssistantService.ts` |
| Credentials-forwarding pattern | `app/api/aiAssistant/infrastructure/buildUwaziCredentials.ts` |
| Feature flags / settings schema | `app/shared/types/settingsSchema.ts`, `app/shared/types/settingsType.d.ts`, `app/api/config.ts` |
| Flag → frontend delivery | `app/react/entry-server.tsx`, `app/react/V2/shared/types.ts` |
| Search bar component | `app/react/Library/components/SearchBar.tsx` |
| Search request hook point | `app/react/Library/helpers/requestState.js` |
| Search route (v1, live) | `app/api/search/deprecatedRoutes.js` (misleading filename) |
| Snippet rendering (`{text, page}`) | `app/react/Layout/ItemSnippet.jsx` |
| Change feed (updatelogs) | `app/api/odm/logHelper.ts`, consumer example `app/api/sync/syncConfig.ts` |
| Old semantic-search remnant | `app/api/config/semanticSearch.ts` (`SEMANTIC_SEARCH_URL`) |

---

## Mini-glossary (plain language)

- **Embedding:** a list of numbers describing a text's meaning; similar meanings → similar
  numbers, even across languages.
- **Chunk:** a small piece of a document (here: merged segmentation paragraphs) — the unit
  you embed and retrieve.
- **Vector store:** a database that finds the closest vectors to a query vector — naive
  ones compare against everything, real ones use ANN indexes (fast, approximate).
- **Cosine similarity:** "how similar in meaning", measured as the angle between two
  vectors.
- **Hybrid search:** combine meaning search (vectors) with exact-word search (keywords);
  each covers the other's weaknesses.
- **RRF (reciprocal rank fusion):** a simple formula to merge two ranked lists into one.
- **RAG (retrieval-augmented generation):** first *find* relevant chunks, then have an LLM
  write an answer *using only those chunks*.
- **Grounding:** the discipline of making the model answer only from retrieved material.
- **Hallucination:** a confident answer with no basis in your data — grounded prompts +
  citation-only-from-sources are the firewall.
- **Recall@k / MRR:** retrieval quality metrics — "did the right document appear in the
  top k?" and "how high did it rank?", averaged over a question set.
- **Lost in the middle:** LLMs attend less to the middle of long inputs — put best chunks
  first.
- **Idempotency:** running the same job twice leaves the same result — the foundation for
  safe re-indexing and sync.