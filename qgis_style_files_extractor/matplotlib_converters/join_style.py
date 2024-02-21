def join_style(s: str | None) -> str | None:
    # How to join segments if the line is solid

    if s is None:
        return None

    matching_join_style = {
        'miter': 'miter',
        'round': 'round',
        'bevel': 'bevel',
    }.get(s, None)

    if matching_join_style is None:
        print(f'unexpected join_style reference "{s}", to implement')

    return matching_join_style
