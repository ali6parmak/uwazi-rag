# Agent Instructions

Guidelines for coding agents working in this repository. Read `PLAN.md` before doing any
work — it is the step-by-step build plan and the source of truth for scope and order.

## Project Overview

`uwazi-rag` is a standalone semantic search + RAG service for Uwazi instances (human rights
and legal document collections). It reads documents and metadata from a Uwazi instance via
its HTTP API, chunks and embeds them with Ollama models, stores vectors in Postgres
(pgvector), and serves:

1. hybrid (meaning + keyword) semantic search returning Uwazi entity `sharedId`s, and
2. RAG answers with citations that link back into Uwazi (`/{language}/entity/{sharedId}`).

It integrates with Uwazi through (a) the AI-assistant job contract (`POST /api/v1/jobs` /
`GET /api/v1/jobs/{id}` — the exact contract `uwazi/app/api/aiAssistant/infrastructure/ExternalAIAssistantService.ts`
implements) and (b) a small, feature-flagged search-bar patch maintained as an
upstream-shaped diff. Long-term this becomes a **global repository** serving many instances;
today it targets one local instance — so never hardcode a single instance into core logic.

The Uwazi HTTP client comes from the sibling package `uwazi-API` (installed as an editable
path dependency). Reuse it; do not re-implement Uwazi auth, paging, file fetching, or
metadata flattening. Field-level Uwazi API behavior is documented in
`../python_uwazi_API/.notes/*.md` — mostly correct but stale; verify surprising claims
against the Uwazi source.

## Tech Stack

- Python 3.12+, `uv`, hatchling, src layout (mirrors the sibling project)
- Pydantic v2 domain models; hexagonal layout: `domain/`, `adapters/`, `use_cases/`, `drivers/`
- FastAPI + uvicorn (REST driver), argparse CLI
- Ollama for embeddings (`POST /api/embed`, default model `bge-m3`, 1024 dims) and LLMs —
  always behind ports (`EmbeddingPort`, `LlmPort`); models/dims come from config, never code
- Postgres + pgvector (`VectorStore` port; a naive in-memory implementation exists for tests)

## Conventions

- Ports for everything external (Ollama, Postgres, Uwazi HTTP, clock). All logic — chunking,
  prompt building, citation formatting, rank fusion, chunk identity — is pure and testable
  offline.
- Chunk identity is `(instance_key, shared_id, language, file_id, chunk_index)`, where
  `instance_key = sha1(instance_url)[:16]`. Indexes are disposable and must be rebuildable
  from Uwazi alone; the pipeline is the product.
- v1 permission rule: index **published entities only**. Answers must cite only retrieved
  chunks; no relevant retrieval → "not found in this collection", never a generic LLM answer.
- Any change to chunking, embedding model, retrieval, or prompts must run the eval harness
  (`uwazi-rag eval` against `data/eval/golden.jsonl`) before it is considered done, with
  results appended to `data/eval/results.md`.

## Testing Policy

When asked to create or modify tests, follow these rules strictly:

1. **No real-instance tests.** Unit tests must not require a running Uwazi instance, Ollama,
   Postgres, network calls, or environment credentials.
2. **No mocks or stubs.** No `unittest.mock`, `MagicMock`, `AsyncMock`, `monkeypatch`, fake
   repositories/adapters, or monkey-patching. The naive in-memory `VectorStore` is a real
   implementation and is the approved way to test logic that needs a store.
3. **Isolated unit tests only.** Test pure functions, domain models, and deterministic
   transformations with real captured data (fixtures under `tests/fixtures/`, produced by
   `uwazi-rag fetch`) and plain assertions.
4. **Run only the test you create.** After creating a test, execute just that file:
   ```bash
   python -m pytest src/uwazi_rag/tests/test_<module>.py -v
   ```
   Do not run the full suite unless explicitly requested.
5. **The eval harness is not a unit test.** It needs the real services and runs via
   `uwazi-rag eval` on demand — never inside pytest.

## Commands

```bash
uv run uwazi-rag hello              # embedding smoke test
uv run uwazi-rag fetch <sharedId>   # capture one entity's text as fixture
uv run uwazi-rag index --template X # index a template's published entities
uv run uwazi-rag search "query"     # hybrid semantic search CLI
uv run uwazi-rag ask "question"     # RAG answer with citations
uv run uwazi-rag eval               # golden-set scorecard (needs real services)
uv run uwazi-rag serve              # HTTP API on $SERVICE_PORT (default 5060)
uv run uwazi-rag sync               # incremental update from updatelogs/editDate
```

Ollama must be running for anything that embeds or answers (`ollama serve`).