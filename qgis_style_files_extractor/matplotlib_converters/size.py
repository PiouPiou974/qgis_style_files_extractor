def size(s: str | None) -> float | None:
    # size in typographic point from size in QGis (millimeters)

    if s is None:
        return None

    return float(s) * 2.83465
