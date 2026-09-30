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

from uwazi_api.client import UwaziClient
from uwazi_api.domain.segmentation import Segmentation

from uwazi_rag.configuration import FIXTURES_DIR, instance_key


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


def capture_entity(client: UwaziClient, *, shared_id: str, language: str, url: str) -> dict:
    """Network part of Step 1 for one entity-language: entity -> segmentation -> capture dict.

    Shared by the CLI driver and the bulk seed script so both capture with the
    exact same logic. Raises ``SegmentationNotFoundError`` when the entity has
    no (file-)segmentation for that language.
    """
    entity = client.entities.get_one(shared_id, language)
    segmentation = client.files.get_segmentation(shared_id, language)
    template = client.templates.get_by_id(entity.template) if entity.template else None
    document = next((d for d in entity.documents if d.id == segmentation.file_id), None)
    return raw_capture_json(
        shared_id=entity.shared_id or shared_id,
        language=language,
        instance_key=instance_key(url),
        title=entity.title or "",
        template_id=entity.template,
        template_name=template.name if template else "",
        file_id=segmentation.file_id,
        file_name=getattr(document, "originalname", None),
        segmentation_status=segmentation.status,
        paragraphs=segmentation_paragraphs(segmentation),
    )


def fixture_is_up_to_date(existing: dict | None, capture: dict) -> bool:
    """True when the committed fixture already holds this content.

    Compares everything except ``fetched_at_utc`` so a re-fetch of an unchanged
    document does not dirty-diff the committed fixture with a new timestamp.
    """
    if existing is None:
        return False

    def stable(capture: dict) -> dict:
        return {key: value for key, value in capture.items() if key != "fetched_at_utc"}

    return stable(existing) == stable(capture)


def write_raw_capture(
    capture: dict, *, instance_key: str, raw_dir: Path, update_fixtures: bool = True
) -> tuple[Path, Path, bool]:
    """Write the capture to the ``data/raw`` cache and the tests fixtures dir.

    The raw copy is always rewritten (disposable cache); the fixture is only
    rewritten when its content effectively changed. Returns
    ``(raw_path, fixture_path, fixture_updated)``.
    """
    filename = f"{capture['shared_id']}_{capture['language']}.json"
    json_text = json.dumps(capture, ensure_ascii=False, indent=2) + "\n"

    raw_path = raw_dir / instance_key / filename
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    raw_path.write_text(json_text, encoding="utf-8")

    fixture_path = FIXTURES_DIR / filename
    existing = json.loads(fixture_path.read_text(encoding="utf-8")) if fixture_path.exists() else None
    if update_fixtures and not fixture_is_up_to_date(existing, capture):
        fixture_path.parent.mkdir(parents=True, exist_ok=True)
        fixture_path.write_text(json_text, encoding="utf-8")
        return raw_path, fixture_path, True
    return raw_path, fixture_path, False


def pages_covered(paragraphs: list[dict]) -> tuple[int, int] | None:
    """The page range the paragraphs span, or None for an empty capture."""
    numbers = [int(p["pageNumber"]) for p in paragraphs if p.get("pageNumber") is not None]
    if not numbers:
        return None
    return min(numbers), max(numbers)
