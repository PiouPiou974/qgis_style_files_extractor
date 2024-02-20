def line_style(s: str | None) -> str | None:
    # How to join segments if the line is solid

    if s is None:
        return None

    if s in ['-', '--', '-.', ':', '']:
        return s

    linestyle = {
        'solid': '-',
        'dot': ':',
        'dash': '--',
        'no': '',
        'dash dot': '-.',
        'dash dot dot': (0, (3, 5, 1, 5, 1, 5)),
    }.get(s, None)

    if linestyle is None:
        print(f'line_style reference "{s}" not found, to implement')

    return linestyle

