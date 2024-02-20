def marker(s: str | None) -> str | None:
    # Marker style string

    if s is None:
        return None

    accepted_markers = {
        ' ': 'nothing',
        '': 'nothing',
        '*': 'star',
        '+': 'plus',
        ',': 'pixel',
        '.': 'point',
        '1': 'tri_down',
        '2': 'tri_up',
        '3': 'tri_left',
        '4': 'tri_right',
        '8': 'octagon',
        '<': 'triangle_left',
        '>': 'triangle_right',
        'D': 'diamond',
        'H': 'hexagon2',
        'None': 'nothing',
        'P': 'plus_filled',
        'X': 'x_filled',
        '^': 'triangle_up',
        '_': 'hline',
        'd': 'thin_diamond',
        'h': 'hexagon1',
        'none': 'nothing',
        'o': 'circle',
        'p': 'pentagon',
        's': 'square',
        'v': 'triangle_down',
        'x': 'x',
        '|': 'vline',
        0: 'tickleft',
        1: 'tickright',
        10: 'caretupbase',
        11: 'caretdownbase',
        2: 'tickup',
        3: 'tickdown',
        4: 'caretleft',
        5: 'caretright',
        6: 'caretup',
        7: 'caretdown',
        8: 'caretleftbase',
        9: 'caretrightbase'
    }

    if s in accepted_markers.keys():
        return s
    if s in accepted_markers.values():
        return s
    if s == 'cross2':
        return 'X'
    return None