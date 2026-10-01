"""Configuration for uwazi-rag (stdlib + dotenv only).

Env vars (see ``.env.example``):

- ``UWAZI_URL``, ``UWAZI_USER``, ``UWAZI_PASSWORD`` — admin credentials for the
  local Uwazi instance (admin because PDF segmentation needs it).
- ``OLLAMA_BASE_URL`` — Ollama HTTP endpoint, default ``http://localhost:11434``.
- ``EMBEDDING_MODEL`` — embedding model name, default ``bge-m3``.
- ``EMBEDDING_DIMENSIONS`` — expected vector size, a property of the model
  (bge-m3: 1024). Verified with a probe embed, never assumed in logic.
- ``SERVICE_PORT`` — REST API port, default 5060.

Import-time safe: nothing here requires services to be reachable, so unit
tests can import this module offline. Uwazi credentials are validated lazily
by :func:`uwazi_credentials` when a use case actually needs them.
"""

from __future__ import annotations

import hashlib
import os
from pathlib import Path

from dotenv import load_dotenv

# Repo root: src/uwazi_rag/configuration.py -> up three levels.
ROOT_PATH: Path = Path(__file__).parent.parent.parent.resolve()
DATA_DIR: Path = ROOT_PATH / "data"
# Uwazi captures (Step 1) — disposable, rebuildable from Uwazi alone.
RAW_DIR: Path = DATA_DIR / "raw"
# Step 3 naive index — one JSON file of (chunk, vector) pairs; disposable
# (rebuildable from data/raw captures) and never committed.
NAIVE_STORE_PATH: Path = DATA_DIR / "naive_store.json"
# Step 3.5 eval artifacts. golden.jsonl / manual.jsonl / about.md are committed
# (the "data is disposable" exception); passages.jsonl is derived and gitignored.
EVAL_DIR: Path = DATA_DIR / "eval"
# Real captured data for offline unit tests (AGENTS.md testing policy). Committed.
FIXTURES_DIR: Path = Path(__file__).parent / "tests" / "fixtures"

# ``override=True`` makes the ``.env`` file authoritative so a stale
# ``UWAZI_URL`` inherited from a parent process cannot redirect the app
# (same convention as the sibling packages).
load_dotenv(ROOT_PATH / ".env", override=True)


def instance_key(url: str) -> str:
    """Stable per-instance namespace key from a Uwazi base URL.

    Trailing slashes are stripped so ``https://x.io`` and ``https://x.io/``
    map to the same key. Chunk identity is namespaced by this key so one
    store can later serve many instances (PLAN.md golden rule 8, Step 12).
    """
    return hashlib.sha1(url.rstrip("/").encode("utf-8")).hexdigest()[:16]


def uwazi_credentials() -> tuple[str, str, str]:
    """``(url, user, password)`` for the local Uwazi instance, checked lazily.

    Raises a clear error instead of failing at import time so ``hello`` and
    the unit tests work without an instance configured.
    """
    url = os.environ.get("UWAZI_URL", "")
    user = os.environ.get("UWAZI_USER", "")
    password = os.environ.get("UWAZI_PASSWORD", "")
    missing = [name for name, value in (("UWAZI_URL", url), ("UWAZI_USER", user), ("UWAZI_PASSWORD", password)) if not value]
    if missing:
        raise RuntimeError(
            "Missing environment variables: " + ", ".join(missing) + ". Copy .env.example to .env and fill it in."
        )
    return url, user, password


# Base URL of the configured Uwazi instance, read like OLLAMA_BASE_URL above
# (credentials stay lazy in :func:`uwazi_credentials`). ``build-index`` uses
# it to namespace the captures dir, ``search`` to print entity links.
UWAZI_URL: str = (os.environ.get("UWAZI_URL") or "").rstrip("/")

OLLAMA_BASE_URL: str = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
# Instruct model behind question drafts (Step 3.5 golden set) and answers (Step 6).
# May be a cloud-served model the local daemon proxies. Required for anything that
# chats: empty here → the adapter raises with setup instructions.
LLM_MODEL: str = os.environ.get("LLM_MODEL", "")
EMBEDDING_MODEL: str = os.environ.get("EMBEDDING_MODEL", "bge-m3")
# Dimensions come from config, never code (PLAN.md golden rule 7). The real
# size is verified at startup by embedding one probe text (see `hello`).
EMBEDDING_DIMENSIONS: int = int(os.environ.get("EMBEDDING_DIMENSIONS", "1024"))
SERVICE_PORT: int = int(os.environ.get("SERVICE_PORT", "5057"))
# Languages golden questions are written in; a capture in one of these languages may
# have its questions generated in the other one (cross-language recall rows). Comma
# separated in .env, e.g. EVAL_LANGUAGES=en,es.
EVAL_LANGUAGES: tuple[str, ...] = tuple(
    code.strip() for code in os.environ.get("EVAL_LANGUAGES", "en,es").split(",") if code.strip()
)


def uwazi_url() -> str:
    """The configured Uwazi base URL, checked lazily.

    Like :func:`uwazi_credentials` but without login: capture-only jobs
    (``build-golden``) need the URL for the ``instance_key`` namespace, not
    credentials.
    """
    url = os.environ.get("UWAZI_URL", "")
    if not url:
        raise RuntimeError("UWAZI_URL is not set. Copy .env.example to .env and fill it in.")
    return url
