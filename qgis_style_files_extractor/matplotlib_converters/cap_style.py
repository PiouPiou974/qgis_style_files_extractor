def cap_style(s: str | None) -> str | None:
    # How to draw the end caps if the line is solid

    if s is None:
        return None

    matching_cap_style = {
        'square': 'projecting',
        'flat': 'butt',
        'round': 'round',
    }.get(s, None)

    if matching_cap_style is None:
        print(f'unexpected cap_style reference "{s}", to implement')

    return matching_cap_style
