def join_style(s: str | None) -> str | None:
    # How to join segments if the line is solid

    if s is None:
        return None

    if s in ['miter', 'round', 'bevel']:
        return s
    return None
