"""Step 4c wave 3.0 — the offline heading scan over every capture home (no embeddings).

PLAN.md Step 4c pre-states the measurement and its go/no-go: across all ``data/raw`` homes
report heading coverage (typed for the Uwazi homes, regex for the typeless line-partitioned
dataset homes), the share of docs whose section partition differs from the incumbent merge
partition, section-length median/p95 at each home's recorded leader geometry, section vs
merge chunk counts, and sampled headings — feeding ONE pre-stated gate: < 30% of contract
documents (contractnli/cuad/maud) with any heading cuts the SectionChunker arm before any
embeddings; the SegmentChunker proceeds regardless. Everything here is offline math over
captures — no Ollama, no stores. The results.md record is hand-written after the report is
reviewed, never emitted by this code.
"""

from __future__ import annotations

import statistics
from dataclasses import dataclass
from math import ceil
from pathlib import Path
from typing import Any

from uwazi_rag.configuration import UWAZI_URL, instance_key
from uwazi_rag.use_cases.chunking import build_chunks, keepable
from uwazi_rag.use_cases.headings import (
    ALL_CAPS_MAX_CHARS,
    is_heading,
    pack_sections,
    partition_sections,
    section_chars,
)
from uwazi_rag.use_cases.index_captures import load_captures

# Recorded leader geometry per instrument (PLAN.md Step 4c wave 3.1; Stage-2 verdict): the
# merge competitor's char budget the section method packs at, and the geometry every
# wave-3.0 chunk/partition lens is measured at. vic-chargebook's passthrough budget is
# listed for the record only — the pre-chunked instrument is OUT OF SCOPE for chunking
# methods (its chunk config does not change).
RECORDED_LEADER_GEOMETRY: dict[str, int] = {
    "legalbenchrag-privacyqa": 2400,
    "legalbenchrag-contractnli": 1200,
    "legalbenchrag-cuad": 2400,
    "legalbenchrag-maud": 2400,
    "vic-chargebook": 4096,
}
DEFAULT_LEADER_GEOMETRY = 1200  # the Uwazi home's recorded leader (Stage-2 chunk leaders all @1200)
MERGE_OVERLAP_RATIO = 0.15  # every recorded merge store is -0.15-; the lens mirrors the incumbent
SAMPLED_HEADINGS = 5  # per instrument, first in deterministic (file name, paragraph position) order
CONTRACT_DATASET_IDS = frozenset({"legalbenchrag-contractnli", "legalbenchrag-cuad", "legalbenchrag-maud"})
CONTRACT_HEADING_GATE_PCT = 30.0  # pre-stated: fewer contract heading-docs than this cuts the SectionChunker arm


@dataclass(frozen=True)
class HeadingSample:
    """One sampled heading: which document, how the detector knew, what the line says."""

    doc: str
    source: str  # "type: <lowercased Uwazi type>" or "regex"
    text: str


@dataclass(frozen=True)
class HomeScan:
    """All wave-3.0 numbers for one capture home (deterministic — same data, same scan)."""

    instance_key: str
    dataset_id: str | None
    template_names: dict[str, int]
    budget: int
    out_of_scope: bool
    captures: int
    captures_ready: int
    captures_skipped_not_ready: int
    docs: int  # ready captures with keepable text — every denominator below, like the index path
    docs_with_headings: int
    headings: int
    heading_sources: dict[str, int]
    docs_partition_differs: int
    sections: int
    section_chars_median: float | None
    section_chars_p95: float | None
    sections_over_budget: int
    section_chunks: int
    merge_chunks: int
    sections_still_over_budget: int
    paragraph_types: dict[str, int]
    samples: list[HeadingSample]


def _sample_text(text: str) -> str:
    """The heading's first line, whitespace-collapsed, truncated to 100 chars."""
    line = text.splitlines()[0] if text.strip() else text
    collapsed = " ".join(line.split())
    return collapsed[:100] + ("…" if len(collapsed) > 100 else "")


def scan_home(home_dir: Path) -> HomeScan:
    """One capture home → its wave-3.0 numbers (offline; same loaders as indexing)."""
    captures = load_captures(home_dir)
    template_names: dict[str, int] = {}
    paragraph_types: dict[str, int] = {}
    dataset_id: str | None = None
    for capture in captures:
        template = capture["template"]
        name = str(template["name"])
        template_names[name] = template_names.get(name, 0) + 1
        if template.get("id") == "dataset":
            if dataset_id is not None and dataset_id != name:
                raise ValueError(f"{home_dir}: one home holds two dataset ids ({dataset_id!r}, {name!r})")
            dataset_id = name
    budget = RECORDED_LEADER_GEOMETRY.get(dataset_id or "", DEFAULT_LEADER_GEOMETRY)
    out_of_scope = dataset_id == "vic-chargebook"

    headings = 0
    sections_total = 0
    sections_over_budget = 0
    section_chunks = 0
    merge_chunks = 0
    sections_still_over_budget = 0
    docs = 0
    docs_with_headings = 0
    docs_partition_differs = 0
    heading_sources = {"type": 0, "regex": 0}
    section_lengths: list[int] = []
    samples: list[HeadingSample] = []
    captures_ready = 0
    captures_skipped_not_ready = 0

    for capture in captures:
        if capture["segmentation_status"] != "ready":
            captures_skipped_not_ready += 1
            continue
        captures_ready += 1
        paragraphs: list[dict[str, Any]] = capture["paragraphs"]
        for paragraph in paragraphs:
            kind = (paragraph.get("type") or "").strip().lower()
            paragraph_types[kind] = paragraph_types.get(kind, 0) + 1

        doc_headings: list[int] = []
        for paragraph_id, paragraph in enumerate(paragraphs):
            if not keepable(paragraph) or not is_heading(paragraph):
                continue
            doc_headings.append(paragraph_id)
            paragraph_type = (paragraph.get("type") or "").strip().lower()
            if paragraph_type:
                heading_sources["type"] += 1
                source = f"type: {paragraph_type}"
            else:
                heading_sources["regex"] += 1
                source = "regex"
            if len(samples) < SAMPLED_HEADINGS:
                samples.append(
                    HeadingSample(doc=str(capture["shared_id"]), source=source, text=_sample_text(str(paragraph["text"])))
                )

        doc_merge = build_chunks(
            paragraphs,
            instance_key=str(capture["instance_key"]),
            shared_id=str(capture["shared_id"]),
            language=str(capture["language"]),
            file_id=str(capture["file"]["id"]),
            entity_title=str(capture["title"]),
            template_name=str(capture["template"]["name"]),
            target_max_chars=budget,
            overlap_ratio=MERGE_OVERLAP_RATIO,
            prepend_header=False,
        )
        if not doc_merge:
            continue  # no keepable text — outside every denominator, exactly like indexing
        docs += 1
        headings += len(doc_headings)
        docs_with_headings += 1 if doc_headings else 0
        merge_chunks += len(doc_merge)

        doc_sections = partition_sections(paragraphs)
        sections_total += len(doc_sections)
        for section in doc_sections:
            chars = section_chars(paragraphs, section)
            section_lengths.append(chars)
            sections_over_budget += 1 if chars > budget else 0
        doc_pack = pack_sections(doc_sections, paragraphs, budget)
        section_chunks += len(doc_pack)
        sections_still_over_budget += sum(1 for group in doc_pack if section_chars(paragraphs, group) > budget)
        if [list(group) for group in doc_pack] != [chunk.paragraph_ids for chunk in doc_merge]:
            docs_partition_differs += 1

    return HomeScan(
        instance_key=str(captures[0]["instance_key"]),
        dataset_id=dataset_id,
        template_names=template_names,
        budget=budget,
        out_of_scope=out_of_scope,
        captures=len(captures),
        captures_ready=captures_ready,
        captures_skipped_not_ready=captures_skipped_not_ready,
        docs=docs,
        docs_with_headings=docs_with_headings,
        headings=headings,
        heading_sources=heading_sources,
        docs_partition_differs=docs_partition_differs,
        sections=sections_total,
        section_chars_median=float(statistics.median(section_lengths)) if section_lengths else None,
        section_chars_p95=_percentile95(section_lengths),
        sections_over_budget=sections_over_budget,
        section_chunks=section_chunks,
        merge_chunks=merge_chunks,
        sections_still_over_budget=sections_still_over_budget,
        paragraph_types=paragraph_types,
        samples=samples,
    )


def _percentile95(values: list[int]) -> float | None:
    """The nearest-rank 95th percentile (deterministic; empty → ``None``, rendered as —)."""
    if not values:
        return None
    ordered = sorted(values)
    return float(ordered[max(0, ceil(0.95 * len(ordered)) - 1)])


def scan_report(raw_dir: Path, *, single_home: Path | None = None) -> str:
    """Every capture home under ``raw_dir`` (or exactly ``single_home``) → the full report."""
    if single_home is not None:
        scans = [scan_home(single_home)]
    else:
        home_dirs = sorted(path for path in raw_dir.iterdir() if path.is_dir() and any(path.glob("*.json")))
        if not home_dirs:
            raise FileNotFoundError(
                f"no capture homes with captures under {raw_dir} — run `uwazi-rag fetch`/`dataset` first"
            )
        scans = [scan_home(home) for home in home_dirs]
    return render_report(scans, live_instance_key=instance_key(UWAZI_URL) if UWAZI_URL else "")


_SUMMARY_HEADER = (
    "| home | budget | docs | +heading | %docs | sect≠merge | %docs | %of +heading"
    " | sections | median/p95 | sect chunks | merge chunks | Δ |"
)


def render_report(scans: list[HomeScan], *, live_instance_key: str = "") -> str:
    """The deterministic markdown report: one summary table + per-home detail + the gate."""
    lines = [
        f"# Wave 3.0 heading scan — {len(scans)} capture home(s), offline (no embeddings, no services, no stores)",
        "",
        "detector (frozen, PLAN.md Step 4c): Uwazi `section header`/`title` types take precedence; typeless first lines",
        " match `ARTICLE|SECTION|EXHIBIT|SCHEDULE|ANNEX|APPENDIX|PART|RECITALS` (uppercase, word-bounded) | `§` |",
        f" ordinal `^\\d+(\\.\\d+)*\\b` | all-caps ≤ {ALL_CAPS_MAX_CHARS} chars, no terminal `. , ; :`",
        "geometry: each home at its recorded leader merge budget (`merge-<budget>/0.15/on`, Stage-2 verdict); header text",
        " never changes counts or partitions, so the header setting is not part of this lens",
        "",
        _SUMMARY_HEADER,
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    lines.extend(_summary_row(scan, live_instance_key) for scan in scans)
    for scan in scans:
        lines.append("")
        lines.extend(_detail(scan, live_instance_key))
    lines.append(_gate(scans))
    return "\n".join(lines) + "\n"


def _summary_row(scan: HomeScan, live_instance_key: str) -> str:
    label = _label(scan, live_instance_key)
    pct_heading = _pct(scan.docs_with_headings, scan.docs)
    pct_differs = _pct(scan.docs_partition_differs, scan.docs)
    pct_differs_of_heading = _pct(scan.docs_partition_differs, scan.docs_with_headings)
    return (
        f"| {label} | {scan.budget} | {scan.docs} | {scan.docs_with_headings} | {pct_heading}"
        f" | {scan.docs_partition_differs} | {pct_differs} | {pct_differs_of_heading} | {scan.sections}"
        f" | {_range(scan.section_chars_median, scan.section_chars_p95)}"
        f" | {scan.section_chunks} | {scan.merge_chunks} | {scan.section_chunks - scan.merge_chunks:+d} |"
    )


def _detail(scan: HomeScan, live_instance_key: str) -> list[str]:
    label = _label(scan, live_instance_key)
    pct_heading = _pct(scan.docs_with_headings, scan.docs)
    lines = [
        f"## {label} — instance `{scan.instance_key}` ({_templates(scan)})",
        "",
        f"- captures: {scan.captures} (ready {scan.captures_ready}, not-ready skipped {scan.captures_skipped_not_ready})"
        f" → text docs {scan.docs}",
        f"- headings: {scan.headings} paragraph(s) in {scan.docs_with_headings} doc(s) ({pct_heading})"
        f" — sources: type {scan.heading_sources['type']} / regex {scan.heading_sources['regex']}",
        f"- sections: {scan.sections} — chars median {_num(scan.section_chars_median)}, p95 {_num(scan.section_chars_p95)};"
        f" over the {scan.budget}-char budget: {scan.sections_over_budget}"
        f" ({_pct(scan.sections_over_budget, scan.sections)})",
        f"- chunks at the recorded geometry: section-packed {scan.section_chunks} vs merge {scan.merge_chunks}"
        f" ({scan.section_chunks - scan.merge_chunks:+d});"
        f" section chunks still over budget: {scan.sections_still_over_budget}",
        f"- section partition differs from the merge partition on {scan.docs_partition_differs} doc(s)"
        f" ({_pct(scan.docs_partition_differs, scan.docs)} of docs;"
        f" {_pct(scan.docs_partition_differs, scan.docs_with_headings)} of heading docs)",
    ]
    if scan.out_of_scope:
        lines.append(
            "- OUT OF SCOPE for chunking methods: pre-chunked passthrough passages;"
            " its chunk config does not change (for the record only)"
        )
    if scan.samples:
        lines.append("- sampled headings (first 5 in file + position order):")
        lines.extend(
            f'  {number}. `{sample.doc}` — {sample.source} — "{sample.text}"'
            for number, sample in enumerate(scan.samples, start=1)
        )
    typed = {name: count for name, count in scan.paragraph_types.items() if name}
    if typed:
        census = ", ".join(f"{name} ×{count}" for name, count in sorted(typed.items(), key=lambda item: -item[1]))
        lines.append(f"- paragraph-type census: {census}")
    return lines


def _gate(scans: list[HomeScan]) -> str:
    """The pre-stated go/no-go block — the record is hand-written after review, not here."""
    heading_docs = sum(scan.docs_with_headings for scan in scans if scan.dataset_id in CONTRACT_DATASET_IDS)
    contract_docs = sum(scan.docs for scan in scans if scan.dataset_id in CONTRACT_DATASET_IDS)
    lines = ["## Go/no-go gate (pre-stated in PLAN.md Step 4c)", ""]
    if contract_docs == 0:
        lines.append("no contract dataset docs in this run — the gate does not apply here")
        return "\n".join(lines)
    gate_pct = 100.0 * heading_docs / contract_docs
    verdict = "KEPT (at/above the 30% bar)" if gate_pct >= CONTRACT_HEADING_GATE_PCT else "CUT (below the 30% bar)"
    lines.append(
        f"contract docs with ≥1 heading (contractnli + cuad + maud): {heading_docs} / {contract_docs} = {gate_pct:.1f}%"
        f" → SectionChunker arm {verdict}; the SegmentChunker proceeds regardless"
    )
    return "\n".join(lines)


def _label(scan: HomeScan, live_instance_key: str) -> str:
    if scan.dataset_id:
        return scan.dataset_id
    if scan.instance_key == live_instance_key:
        return "uwazi (live)"
    return "uwazi (other)"


def _templates(scan: HomeScan) -> str:
    return ", ".join(f"{name} ×{count}" for name, count in sorted(scan.template_names.items(), key=lambda item: -item[1]))


def _pct(numerator: int, denominator: int) -> str:
    return "—" if denominator <= 0 else f"{100.0 * numerator / denominator:.1f}%"


def _num(value: float | None) -> str:
    return "—" if value is None else f"{value:.0f}"


def _range(median: float | None, p95: float | None) -> str:
    return f"{_num(median)}/{_num(p95)}"
