# sometimes, in layers, "prop" is not defined. We can reconstruct it from "Option"


def get_prop(layer: dict) -> list:
    if 'prop' in layer.keys():
        return layer['prop']

    options: dict = layer['Option']
    assert options.get('@type') == 'Map'
    options: list = options['Option']
    prop = [{"@k": _dict["@name"], "@v": _dict["@value"]} for _dict in options]
    return prop
