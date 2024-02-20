import matplotlib.colors


def rgba_to_hex(s: str | None) -> str | None:

    if s is None:
        return None

    rgba = tuple(int(v)/255 for v in s.split(','))
    return matplotlib.colors.to_hex(rgba, keep_alpha=True)
