"""Step 4a — the legalbenchrag adapter (sources: privacy_qa, contractnli, cuad).

ZeroEntropy's LegalBench-RAG parked upstream (verified 2026-10-06, see
``data/datasets/legalbenchrag/about.md`` — that file is this adapter's
contract). One dataset per SOURCE (each gets its own instance-key namespace
and sweep); the upstream package stays shared on disk, never duplicated.
MAUD is deliberately ABSENT — it is license-gated until its terms are checked
with its authors.

The mapping (from the home's about.md contract):

- corpus reads are Python text-mode ``utf-8`` (``Path.read_text``), never
  ``utf-8-sig`` — the gold spans are text-mode offsets;
- filenames normalize on BOTH sides (reference × disk) through NFC — one CUAD
  file is referenced NFD while it sits on disk NFC (``LECLANCHÉ…``);
  normalization is how the adapter finds it;
- paragraphs synthesize as an offset-preserving line partition of the raw
  text (``core.synthesize_paragraphs``) — the corpus carries no blank lines;
- every snippet passes the dataset's own self-check
  (``text[start:end] == answer``) — the adapter's acceptance gate;
- char-spans → ``paragraph_ids`` anchors by strict interval intersection.

Queries keep their upstream shape verbatim (``Consider "Doc title"; question``
— the doc-title context is part of the benchmark, and instrument fidelity
beats cosmetic query cleanup).
"""

from __future__ import annotations

import json
import unicodedata
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from uwazi_rag.adapters.datasets.base import DatasetBuildResult
from uwazi_rag.adapters.datasets.core import (
    UPSTREAM_ORIGIN,
    capture_paragraphs,
    content_anchor_ids,
    make_dataset_capture,
    make_expected_block,
    make_golden_row,
    span_text,
    synthesize_paragraphs,
)
from uwazi_rag.adapters.datasets.pins import PinCheck, verify_pins
from uwazi_rag.configuration import DATA_DIR, dataset_instance_key

# dataset id → upstream benchmark/corpus source directory. MAUD omitted on
# purpose (license-gated — see the home's about.md GATE note).
SOURCES: dict[str, str] = {
    "legalbenchrag-privacyqa": "privacy_qa",
    "legalbenchrag-contractnli": "contractnli",
    "legalbenchrag-cuad": "cuad",
}

HOME_DIR_NAME = "legalbenchrag"


class LegalBenchRagSource:
    """One LegalBench-RAG source as a dataset instrument.

    Built once per dataset id at registry time; ``build`` maps the upstream
    tree deterministically — same tree, same bytes out (pinned by tests).
    """

    def __init__(self, dataset_id: str, *, home_dir: Path | None = None) -> None:
        if dataset_id not in SOURCES:
            raise ValueError(
                f"legalbenchrag source ids are {', '.join(sorted(SOURCES))} "
                "(MAUD is gated — see data/datasets/legalbenchrag/about.md)"
            )
        self._dataset_id = dataset_id
        self.source = SOURCES[dataset_id]
        # Optional override for the offline tests (fixture slices carry the same
        # home layout: about contract + checksums pins + upstream/); None = real paths.
        self._home_dir = home_dir

    @property
    def dataset_id(self) -> str:
        return self._dataset_id

    def home_dir(self) -> Path:
        return self._home_dir if self._home_dir is not None else DATA_DIR / "datasets" / HOME_DIR_NAME

    def upstream_dir(self) -> Path:
        return self.home_dir() / "upstream"

    def pin_labels(self) -> set[str]:
        """What this source's build consumes: the benchmark file + the source's corpus digest."""
        return {f"file:benchmarks/{self.source}.json", f"corpus:corpus/{self.source}"}

    def verify(self, upstream_dir: Path) -> list[PinCheck]:
        """Checksum-verify exactly what this source consumes (raises on drift)."""
        return verify_pins(self.home_dir() / "checksums.txt", upstream_dir, labels=self.pin_labels())

    def build(self, upstream_dir: Path) -> DatasetBuildResult:
        """Map the whole source upstream: captures for every corpus doc + golden rows.

        Deterministic on three axes the tests pin: question order is the
        benchmark file's order grouped by first-appearance document; captures
        cover EVERY corpus file of the source (the corpus is the instrument's
        whole search space, as upstream ships it) in file-name order; and
        capture bytes contain no clock (``fetched_at_utc`` is ``None``).
        """
        pin_checks = self.verify(upstream_dir)
        corpus_dir = upstream_dir / "corpus" / self.source
        disk_index = _disk_name_index(corpus_dir)

        docs_cache: dict[str, str] = {}  # NFC file_path → text
        remapped_paths: set[str] = set()
        rows_per_doc: dict[str, list[dict[str, Any]]] = {}  # first-appearance document order
        checks = 0
        for test in _tests(upstream_dir / "benchmarks" / f"{self.source}.json"):
            snippets = test["snippets"]
            raw_paths = {str(snippet["file_path"]) for snippet in snippets}
            paths = {_nfc(raw) for raw in raw_paths}
            if len(paths) != 1:
                raise ValueError(
                    f"query {str(test['query'])[:80]!r}: its snippets span {sorted(paths)} — the benchmark "
                    "anchors every question to exactly ONE document (about.md); refusing to guess"
                )
            file_path = next(iter(paths))
            if any(raw != _nfc(raw) for raw in raw_paths):
                remapped_paths.add(file_path)
            text, _ = _document_text(corpus_dir, file_path, disk_index, docs_cache)
            spans = synthesize_paragraphs(text)
            answers: list[str] = []
            anchor_set: set[int] = set()
            for snippet in snippets:
                span = (int(snippet["span"][0]), int(snippet["span"][1]))
                if span_text(text, span) != str(snippet["answer"]):
                    raise ValueError(
                        f"{file_path} span [{span[0]}, {span[1]}) fails the dataset's own self-check "
                        "(text[start:end] == answer) — the upstream offsets do not hold; aborting the build"
                    )
                checks += 1
                answers.append(str(snippet["answer"]))
                anchor_set.update(content_anchor_ids(text, spans, span))
            shared_id = _shared_id(file_path)
            rows_per_doc.setdefault(file_path, []).append(
                make_golden_row(
                    row_id=f"{shared_id}:q{len(rows_per_doc[file_path]) + 1:03d}",
                    question=str(test["query"]),
                    origin=UPSTREAM_ORIGIN,
                    query_language="en",
                    source_group_id=shared_id,
                    expected=make_expected_block(
                        instance_key=dataset_instance_key(self._dataset_id),
                        shared_id=shared_id,
                        title=shared_id,
                        language="en",
                        file_id=file_path,
                        paragraph_ids=sorted(anchor_set),  # ascending, like the house rows
                        text="\n\n".join(answers),
                    ),
                )
            )

        captures: dict[str, dict[str, Any]] = {}
        for normalized_name in sorted(disk_index):
            file_path = f"{self.source}/{normalized_name}"
            text, _ = _document_text(corpus_dir, file_path, disk_index, docs_cache)
            shared_id = _shared_id(file_path)
            name = f"{shared_id}_en.json"
            if name in captures:
                raise ValueError(f"two corpus files would capture as {name!r} — stems must be unique per source")
            capture = make_dataset_capture(
                dataset_id=self._dataset_id,
                shared_id=shared_id,
                title=shared_id,
                file_id=file_path,
                file_name=normalized_name,
                paragraphs=capture_paragraphs(text, synthesize_paragraphs(text)),
            )
            captures[name] = capture

        golden_rows = [row for file_rows in rows_per_doc.values() for row in file_rows]
        return DatasetBuildResult(
            captures=captures,
            golden_rows=golden_rows,
            pin_checks=pin_checks,
            checks=checks,
            note=(f"{len(remapped_paths)} filename(s) resolved through NFC normalization" if remapped_paths else ""),
        )


def _nfc(name: str) -> str:
    """NFC-normalize one filename — the disk side is read through NFC as well."""
    return unicodedata.normalize("NFC", name)


def _shared_id(file_path: str) -> str:
    """The document's entity id: its (NFC) basename without the ``.txt``."""
    return file_path.rsplit("/", 1)[-1].removesuffix(".txt")


def _disk_name_index(corpus_dir: Path) -> dict[str, str]:
    """NFC-normalized ``*.txt`` basenames → actual on-disk names (ambiguity is fatal)."""
    if not corpus_dir.is_dir():
        raise FileNotFoundError(f"no corpus dir at {corpus_dir} — the upstream tree is incomplete")
    index: dict[str, str] = {}
    for path in sorted(corpus_dir.glob("*.txt")):
        normalized = _nfc(path.name)
        if normalized in index and index[normalized] != path.name:
            raise ValueError(f"two corpus files normalize to the same name ({normalized!r}) — ambiguity, refusing")
        index[normalized] = path.name
    return index


def _document_text(
    corpus_dir: Path,
    file_path: str,
    disk_index: Mapping[str, str],
    cache: dict[str, str],
) -> tuple[str, int]:
    """The document's text as Python text-mode utf-8 (the offsets' frame), NFC-resolved.

    Returns ``(text, remap_count)`` — remap is 1 when the reference needed NFC
    normalization to find its on-disk name, 0 otherwise (the quirk counter).
    """
    if file_path in cache:
        return cache[file_path], 0
    name = file_path.rsplit("/", 1)[-1]
    actual = disk_index.get(name)
    if actual is None:
        raise FileNotFoundError(
            f"benchmark references {file_path!r} but no corpus file normalizes to {name!r} — "
            "the benchmark and corpus trees disagree; refusing to build"
        )
    remapped = 0 if actual == name else 1
    text = (corpus_dir / actual).read_text(encoding="utf-8")
    cache[file_path] = text
    return text, remapped


def _tests(benchmarks_path: Path) -> Sequence[Mapping[str, Any]]:
    """The benchmark JSON's ``tests`` list (deterministic: pinned revision)."""
    parsed: dict[str, Any] = json.loads(benchmarks_path.read_text(encoding="utf-8"))
    tests: list[dict[str, Any]] = parsed["tests"]
    if not tests:
        raise ValueError(f"{benchmarks_path}: empty tests list — refusing to build an empty dataset")
    return tests
