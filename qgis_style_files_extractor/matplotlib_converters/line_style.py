def line_style(s: str | None) -> str | None:
    # How to join segments if the line is solid

    if s is None:
        return None

    if s in ['-', '--', '-.', ':', '']:
        return s

    if s == 'no':
        return None

    linestyle = {
        'solid': '-',
        'dot': ':',
        'dash': '--',
        'dash dot': '-.',
        'dash dot dot': (0, (3, 5, 1, 5, 1, 5)),
    }.get(s, None)

    if linestyle is None:
        print(f'unexpected line_style reference "{s}", to implement')

    return linestyle

