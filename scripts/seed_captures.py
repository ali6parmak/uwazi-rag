"""One-off bulk capture: seed ``data/raw/`` with published entities + segmentations.

Dev tooling, deliberately NOT a ``uwazi-rag`` CLI subcommand — bulk capture is
data provisioning, not the product. It reuses the exact Step 1 capture logic
(``capture_entity`` + ``write_raw_capture``) and the same ``.env`` credentials.

Read-only against the Uwazi instance (published entities only); writes only
into this repo's ``data/raw/`` directory. Fixtures are NOT touched by bulk
runs — they stay curated (promote one by hand when one deserves test status).

Example:

    python scripts/seed_captures.py --list
    python scripts/seed_captures.py --group "HRC: NGO Written Statement" \\
        --group "Inter-American Court: Judgments" --per-group 8
"""

from __future__ import annotations

import argparse
import sys

from uwazi_api.client import UwaziClient
from uwazi_api.domain.exceptions import SegmentationNotFoundError
from uwazi_api.domain.search_filters import SearchFilters, SelectFilter

from uwazi_rag.configuration import RAW_DIR, instance_key, uwazi_credentials
from uwazi_rag.use_cases.fetch_document import capture_entity, write_raw_capture

DEFAULT_TEMPLATE = "DOCUMENT"
DEFAULT_PROP = "Document Type"


def _build_client() -> tuple[UwaziClient, str]:
    url, user, password = uwazi_credentials()
    return UwaziClient(url=url, user=user, password=password), url


def _list_groups(client: UwaziClient, template: str, prop_name: str, language: str) -> None:
    prop = client.templates.find_property(template, prop_name)
    if prop is None:
        template_obj = client.templates.get_by_name(template) or next(
            (t for t in client.templates.get() if t.name == template), None
        )
        prop_names = [p.name for p in (template_obj.properties if template_obj else [])]
        raise RuntimeError(f"property '{prop_name}' not found in template '{template}' — available: {prop_names}")
    thesaurus = next((t for t in client.thesauris.get(language) if t.id == prop.content), None)
    if thesaurus is None:
        raise RuntimeError(f"thesaurus '{prop.content}' for property '{prop_name}' not found")
    print(f"document_type families under '{prop_name}' ({template}, labels in '{language}'):")
    for family in thesaurus.values:
        print(f"- {family.label}")
        for sub in family.values or []:
            print(f"    - {sub.label}")


def _all_subgroups(client: UwaziClient, template: str, prop_name: str, language: str) -> list[str]:
    """Every subgroup label (level below the family), sorted for stable output."""
    prop = client.templates.find_property(template, prop_name)
    thesaurus = next((t for t in client.thesauris.get(language) if t.id == prop.content), None)
    labels: list[str] = []
    for family in thesaurus.values:
        if family.values:
            labels.extend(sub.label for sub in family.values)
        else:
            labels.append(family.label)
    return labels


def _count_group(
    client: UwaziClient, template: str, prop_name: str, group: str, language: str, published: bool | None = None
) -> int:
    """Published-entity count for one subgroup by paging the search API.

    Bounded by the ES 10k window like every /api/search consumer; for this
    instance's group sizes it is a fair estimate. ``published=None`` counts
    what the admin account can see (the remote Global Repository keeps its
    entities unpublished until release day).
    """
    total = 0
    start_from = 0
    batch = 100
    while True:
        filters = SearchFilters()
        filters.add(prop_name, SelectFilter(values=[group]))
        rows = client.search.search_by_filter(
            filters,
            template_name=template,
            start_from=start_from,
            batch_size=batch,
            published=published,
            language=language,
        )
        total += len(rows)
        if len(rows) < batch or start_from + batch >= 10000:
            return total
        start_from += batch


def _sample_and_capture(
    client: UwaziClient,
    url: str,
    *,
    template: str,
    prop_name: str,
    group: str,
    per_group: int,
    languages: list[str],
    published: bool | None = None,
) -> tuple[int, int]:
    """Capture up to ``per_group`` entities of one subgroup. Returns (ok, skipped)."""
    filters = SearchFilters()
    filters.add(prop_name, SelectFilter(values=[group]))
    entities = client.search.search_by_filter(
        filters,
        template_name=template,
        batch_size=per_group,
        published=published,
        language="en",
        sort="creationDate",
        order="desc",
    )
    print(f"\n[{group}] sampling {min(per_group, len(entities))}/{len(entities)} candidates")
    ok = skipped = 0
    for entity in entities:
        for language in languages:
            try:
                capture = capture_entity(client, shared_id=entity.shared_id or "", language=language, url=url)
            except SegmentationNotFoundError as error:
                print(f"  skip {entity.shared_id} [{language}]: {error}")
                skipped += 1
                continue
            except Exception as error:
                print(f"  ERROR {entity.shared_id} [{language}]: {error}", file=sys.stderr)
                skipped += 1
                continue
            raw_path, _, _ = write_raw_capture(
                capture,
                instance_key=instance_key(url),
                raw_dir=RAW_DIR,
                update_fixtures=False,
            )
            print(f"  {capture['shared_id']} [{language}] {len(capture['paragraphs'])} paras -> {raw_path.name}")
            ok += 1
    print(f"[{group}] captured: {ok}, skipped/failed: {skipped}")
    return ok, skipped


def main() -> int:
    parser = argparse.ArgumentParser(description="Bulk-capture published entities into data/raw (dev tool)")
    parser.add_argument("--template", default=DEFAULT_TEMPLATE)
    parser.add_argument("--prop", default=DEFAULT_PROP, help="select property holding the document groups")
    parser.add_argument("--language", action="append", dest="languages", help="entity language, repeatable")
    parser.add_argument("--group", action="append", dest="groups", help="subgroup label to sample from, repeatable")
    parser.add_argument("--per-group", type=int, default=8)
    parser.add_argument("--list", action="store_true", help="print the group tree of the document_type property")
    parser.add_argument(
        "--publishing",
        choices=("any", "published"),
        default="any",
        help="any = everything the admin account sees (default; the Global Repository keeps entities unpublished),"
        " published = strict published-only",
    )
    parser.add_argument(
        "--count",
        action="store_true",
        help="count entities per document_type subgroup (all subgroups, or only --group ones)",
    )
    args = parser.parse_args()

    client, url = _build_client()
    languages = args.languages or ["en", "es"]

    if args.list:
        _list_groups(client, args.template, args.prop, languages[0])
        return 0

    if args.count:
        groups = args.groups or _all_subgroups(client, args.template, args.prop, languages[0])
        published_flag = True if args.publishing == "published" else None
        counts = {
            g: _count_group(client, args.template, args.prop, g, languages[0], published=published_flag) for g in groups
        }
        for label, count in sorted(counts.items(), key=lambda item: item[1], reverse=True):
            print(f"{count:6d}  {label}")
        return 0

    if not args.groups:
        parser.error("provide --group (repeatable) or use --list to see the groups")

    total_ok = total_skipped = 0
    for group in args.groups or []:
        ok, skipped = _sample_and_capture(
            client,
            url,
            template=args.template,
            prop_name=args.prop,
            group=group,
            per_group=args.per_group,
            languages=languages,
            published=True if args.publishing == "published" else None,
        )
        total_ok += ok
        total_skipped += skipped

    print(f"\nDONE — captured {total_ok} captures, skipped/failed {total_skipped}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
