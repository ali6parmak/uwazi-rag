"""Step 4a — committed checksum pins for the dataset instruments.

Upstream material is gitignored (disposable, re-fetchable), so the build's
integrity guarantee cannot live in the upstream tree: each home carries a
committed ``checksums.txt`` that pins exactly what the adapter consumes.
Measured from the parked, verified upstream (2026-10-06, per each home's
``about.md``); any drift makes the build fail loudly BEFORE anything is
written — a rebuilt dataset is only as trustworthy as its pins.

File format (one check per line, ``#`` comments allowed):

- ``file <relative-path> <sha256>``        — one exact upstream file
- ``corpus <relative-dir> <sha256>``       — the corpus digest: sha256 over
  every ``*.txt`` under the dir, sorted, fed as
  ``relative-name + "\\0" + bytes`` (name- and content-sensitive)

Pure-but-impure hybrid: the digest rules are pure; reading pins and upstream
files is real file IO (offline — no network, per the testing policy).
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PinCheck:
    """One verified pin fact — for the build summary."""

    label: str
    digest: str
    source_count: int


def file_digest(path: Path) -> str:
    """sha256 of one file's bytes."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def corpus_digest(upstream_dir: Path, relative_dir: str) -> str:
    """The ``corpus`` pin digest: sha256 over sorted ``*.txt`` names + bytes.

    Same convention as the sweep runner's capture digest (name + ``\\0`` +
    bytes): sensitive to additions, removals, renames and content alike.
    """
    directory = upstream_dir / relative_dir
    if not directory.is_dir():
        raise FileNotFoundError(f"corpus dir {directory} does not exist — the upstream tree is incomplete")
    files = sorted(directory.glob("*.txt"))
    if not files:
        raise FileNotFoundError(f"no .txt corpus files under {directory} — the upstream tree is incomplete")
    digest = hashlib.sha256()
    for path in files:
        digest.update(path.name.encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
    return digest.hexdigest()


def parse_pins(pins_path: Path) -> dict[str, str]:
    """Parse a committed ``checksums.txt`` into ``label → expected sha256``."""
    pins: dict[str, str] = {}
    for number, raw_line in enumerate(pins_path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) != 3 or parts[0] not in ("file", "corpus"):
            raise ValueError(
                f"{pins_path.name} line {number}: expected 'file <rel-path> <sha256>' "
                f"or 'corpus <rel-dir> <sha256>', got {line!r}"
            )
        kind, name, digest = parts
        if len(digest) != 64 or any(char not in "0123456789abcdef" for char in digest):
            raise ValueError(f"{pins_path.name} line {number}: {digest!r} is not a sha256 hex digest")
        label = f"{kind}:{name}"
        if label in pins:
            raise ValueError(f"{pins_path.name} line {number}: label {label!r} appears twice")
        pins[label] = digest
    if not pins:
        raise ValueError(f"{pins_path}: no pins recorded — refuse to build an unpinned dataset")
    return pins


def verify_pins(pins_path: Path, upstream_dir: Path, *, labels: set[str]) -> list[PinCheck]:
    """Verify the named pins against the upstream tree; raise on any mismatch.

    ``labels`` is what the adapter consumes — unrelated pins in the file are
    ignored (a home may pin more than one adapter consumes at a time, e.g.
    MAUD stays pinned-but-gated). Every mismatch names the expected and
    actual digest in one stderr-ready message.
    """
    pins = parse_pins(pins_path)
    missing = sorted(labels - set(pins))
    if missing:
        raise ValueError(
            f"pins file {pins_path} lacks entries for {', '.join(missing)} — pin them from the verified upstream first"
        )
    checks: list[PinCheck] = []
    for label in sorted(labels):
        kind, name = label.split(":", 1)
        digest = file_digest(upstream_dir / name) if kind == "file" else corpus_digest(upstream_dir, name)
        expected_digest = pins[label]
        if digest != expected_digest:
            raise ValueError(
                f"upstream drift at {label}: pinned {expected_digest[:16]}…, measured {digest[:16]}… "
                f"— re-fetch/verify the upstream against {pins_path} before building"
            )
        checks.append(
            PinCheck(
                label=label,
                digest=digest,
                source_count=len(list((upstream_dir / name).glob("*.txt"))) if kind == "corpus" else 1,
            )
        )
    return checks
