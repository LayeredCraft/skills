from parser import parse_fields


def test_parse_fields_trims_values() -> None:
    assert parse_fields("alpha, beta") == ["alpha", "beta"]
