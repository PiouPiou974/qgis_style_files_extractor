def as_list(o: dict | list) -> list:
    if type(o) is list:
        return o
    return [o]


def get_from_k_v_list(k_v_list: list[dict[str: str]], key: str) -> str | None:
    return next((_dict['@v'] for _dict in k_v_list if _dict['@k'] == key), None)


def no_empty_values(d: dict) -> dict:
    return_dict = dict()
    for k, v in d.items():
        if v is not None:
            return_dict[k] = v
    return return_dict
