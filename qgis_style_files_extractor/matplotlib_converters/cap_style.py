def cap_style(s: str | None) -> str | None:
    # How to draw the end caps if the line is solid

    if s is None:
        return None

    if s in ['butt', 'projecting', 'round']:
        return s
    if s == 'square':
        return 'butt'
    return None
