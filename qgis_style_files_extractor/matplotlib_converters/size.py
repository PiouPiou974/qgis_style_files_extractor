def size(s: str | None) -> float | None:
    # size in typographic point from size in QGis (millimeters)

    if s is None:
        return None

    if float(s) == 0:  # case hair-line
        return 0.5

    return float(s) * 2.83465
