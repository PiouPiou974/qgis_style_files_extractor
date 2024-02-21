def hatch_from_fill_style(s: str | None) -> str | None:
    # How to join segments if the line is solid

    if s is None:
        return None

    if s in ['/', '\\', '|', '-', '+', 'x', 'o', 'O', '.', '*']:
        return s

    if s in ['solid', 'no']:
        return None

    hatch = {
        'vertical': '|',
        'horizontal': '-',
        'b_diagonal': '/',
        'f_diagonal': '\\',
        'diagonal_x': 'x',
        'cross': '+',
        'dense1': '.......',
        'dense2': '......',
        'dense3': '.....',
        'dense4': '....',
        'dense5': '...',
        'dense6': '..',
        'dense7': '.',
    }.get(s, None)

    if hatch is None:
        print(f'unexpected hatch reference "{s}", to implement')

    return hatch

