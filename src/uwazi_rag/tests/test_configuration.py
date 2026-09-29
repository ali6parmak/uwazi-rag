from uwazi_rag.configuration import instance_key


def test_instance_key_matches_the_known_sha1_prefix() -> None:
    # sha1("http://localhost:3000")[:16] — locks the convention used everywhere
    # (chunk identity, cache paths) so it can never silently change.
    assert instance_key("http://localhost:3000") == "2bf0fa1d7db9ecd6"


def test_instance_key_is_a_16_char_hex_string() -> None:
    key = instance_key("https://huridocs.example.org")
    assert len(key) == 16
    int(key, 16)  # must parse as hexadecimal


def test_instance_key_strips_trailing_slash() -> None:
    assert instance_key("https://x.io/") == instance_key("https://x.io")


def test_instance_key_differs_across_hosts() -> None:
    assert instance_key("https://a.io") != instance_key("https://b.io")


def test_instance_key_is_deterministic() -> None:
    assert instance_key("https://x.io") == instance_key("https://x.io")
