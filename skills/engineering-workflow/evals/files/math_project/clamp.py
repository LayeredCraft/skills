def clamp(value: int, lower: int, upper: int) -> int:
    """Constrain value to inclusive lower and upper bounds."""
    return max(lower, min(value, upper))
