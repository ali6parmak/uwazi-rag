from uwazi_rag.use_cases.fetch_document import pages_covered, raw_capture_json

SAMPLE_PARAGRAPH = {
    "left": 0.0,
    "top": 0.0,
    "width": 1.0,
    "height": 1.0,
    "pageNumber": 3,
    "text": "Witnesses reported that armed men took the prisoners away at night.",
    "type": "paragraph",
}


def _capture(paragraphs: list[dict] | None = None) -> dict:
    return raw_capture_json(
        shared_id="64hnagcpvk",
        language="en",
        instance_key="2bf0fa1d7db9ecd6",
        title="Global Repository document 192",
        template_id="6a85a0c6131bc6535a55de7f",
        template_name="Report",
        file_id="6abb75f8f1a0fa406043ae6a",
        file_name="Report No. 7016.pdf",
        segmentation_status="ready",
        paragraphs=paragraphs or [SAMPLE_PARAGRAPH],
        fetched_at_utc="2026-09-29T00:00:00+00:00",
    )


def test_capture_keeps_uwazi_raw_field_names_in_paragraphs() -> None:
    capture = _capture()
    assert capture["paragraphs"][0]["pageNumber"] == 3
    assert "text" in capture["paragraphs"][0]


def test_capture_records_identity_and_provenance() -> None:
    capture = _capture()
    assert capture["instance_key"] == "2bf0fa1d7db9ecd6"
    assert capture["shared_id"] == "64hnagcpvk"
    assert capture["language"] == "en"
    assert capture["template"]["name"] == "Report"
    assert capture["file"]["name"] == "Report No. 7016.pdf"
    assert capture["segmentation_status"] == "ready"
    assert capture["fetched_at_utc"] == "2026-09-29T00:00:00+00:00"


def test_pages_covered_reports_min_and_max_ignoring_missing_pages() -> None:
    assert pages_covered([{"pageNumber": 3}] * 2 + [{"pageNumber": 1}]) == (1, 3)
    assert pages_covered([{"pageNumber": 5}, {"pageNumber": None}]) == (5, 5)


def test_pages_covered_is_none_without_paragraphs() -> None:
    assert pages_covered([]) is None
