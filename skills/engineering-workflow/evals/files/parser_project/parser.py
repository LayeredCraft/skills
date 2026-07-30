def parse_fields(text: str) -> list[str]:
    """Split comma-separated fields, trimming surrounding whitespace."""
    return [part.strip() for part in text.split(",")]
