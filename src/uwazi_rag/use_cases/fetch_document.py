"""Step 1: capture one entity's segmentation from Uwazi.

The driver (CLI) does the network part through ``uwazi_api``; the pure part
below assembles the capture JSON and writes it. The exact same JSON lands in
``data/raw/{instance_key}/`` (the working cache) and under
``src/uwazi_rag/tests/fixtures/`` (committed) — the fixture powers the offline
unit tests from Step 2 onward, per the AGENTS.md testing policy.

Immutability notes (from the sibling repo's field notes): a file's storage
filename never changes content (uploads mint new names) and a ``ready``
segmentation for a given ``file_id`` never changes — so both are safe to cache
forever. Captures missing a segmentation record that fact instead of failing.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from uwazi_api.domain.segmentation import Segmentation

from uwazi_rag.configuration import FIXTURES_DIR


def raw_capture_json(
    *,
    shared_id: str,
    language: str,
    instance_key: str,
    title: str,
    template_id: str | None,
    template_name: str,
    file_id: str | None,
    file_name: str | None,
    segmentation_status: str,
    paragraphs: list[dict],
    fetched_at_utc: str | None = None,
) -> dict:
    """Assemble the capture JSON for one ``sharedId`` + entity-language.

    ``paragraphs`` already use Uwazi's raw field names (``text``, ``pageNumber``,
    position fields) so the fixture mirrors the API payload.
    """
    return {
        "instance_key": instance_key,
        "shared_id": shared_id,
        "language": language,
        "title": title,
        "template": {"id": template_id, "name": template_name},
        "file": {"id": file_id, "name": file_name},
        "segmentation_status": segmentation_status,
        "fetched_at_utc": fetched_at_utc or datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "paragraphs": paragraphs,
    }


def segmentation_paragraphs(segmentation: Segmentation) -> list[dict]:
    """Dump a ``Segmentation`` into raw-Uwazi-name dicts (aliased)."""
    return [p.model_dump(mode="json", by_alias=True) for p in segmentation.paragraphs]


def write_raw_capture(capture: dict, *, instance_key: str, raw_dir: Path) -> list[Path]:
    """Write the capture to the ``data/raw`` cache and the tests fixtures dir."""
    filename = f"{capture['shared_id']}_{capture['language']}.json"
    data_dir = raw_dir / instance_key
    data_dir.mkdir(parents=True, exist_ok=True)
    targets = [data_dir / filename, FIXTURES_DIR / filename]
    for path in targets:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(capture, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return targets


def pages_covered(paragraphs: list[dict]) -> tuple[int, int] | None:
    """The page range the paragraphs span, or None for an empty capture."""
    numbers = [int(p["pageNumber"]) for p in paragraphs if p.get("pageNumber") is not None]
    if not numbers:
        return None
    return min(numbers), max(numbers)
