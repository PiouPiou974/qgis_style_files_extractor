# sometimes, in layers, "prop" is not defined. We can reconstruct it from "Option"


def get_prop(layer: dict) -> list:
    # nested symbol :
    if 'symbol' in layer.keys():
        print('nested symbol')
        assert type(layer['symbol']['layer']) is dict
        return get_prop(layer['symbol']['layer'])

    if 'prop' in layer.keys():
        return layer['prop']

    options: dict = layer['Option']
    assert options.get('@type') == 'Map'
    options: list = options['Option']
    prop = [{"@k": _dict["@name"], "@v": _dict["@value"]} for _dict in options]
    return prop
