async def format_numeric(numeric: int | float) -> str:
    suffixes = [
        (1_000_000_000_000_000, "Q"),
        (1_000_000_000_000, "T"),
        (1_000_000_000, "B"),
        (1_000_000, "M"),
        (1_000, "K"),
    ]
    abs_value = abs(numeric)

    for threshold, suffix in suffixes:
        if abs_value >= threshold:
            value = numeric / threshold
            return f"{value:.0f}{suffix}" if value.is_integer() else f"{value:.1f}{suffix}"
    return str(numeric)