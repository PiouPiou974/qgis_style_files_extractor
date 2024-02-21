import warnings

from ..dict_list_manipulations import get_from_k_v_list, as_list
from .. import matplotlib_converters as mpl_conv


def properties_and_symbol_to_dicts(properties: list, symbols: list) -> list[dict]:
    warnings.warn('Custom point pattern fill is currently not well supported in matplotlib, using hatching. '
                  'Differences may arise in symbology.')

    distance_x = mpl_conv.size(get_from_k_v_list(k_v_list=properties, key='distance_x'))
    distance_y = mpl_conv.size(get_from_k_v_list(k_v_list=properties, key='distance_y'))
    distance_between_points = min(distance_x, distance_y)
    # calculate density, based on distance, between 1 (10 millimeters apart) and 7 (1 millimeters apart).
    density = 10 / distance_between_points
    if density > 7:
        density = 7
    if density < 1:
        density = 1
    density = int(density)

    properties_list = list()

    symbols = as_list(symbols)
    for symbol in symbols:
        # get the first layer of the symbol to retrieve data :
        symbol_properties = symbol['layer']['prop']

        original_marker_symbol = get_from_k_v_list(k_v_list=symbol_properties, key='name')
        matplotlib_marker_symbol = mpl_conv.marker(original_marker_symbol)
        if matplotlib_marker_symbol is None:
            # if no symbol : no hatching
            continue

        accepted_hatching_symbol = {
            '/': '/',
            '\\': '\\',
            '|': '|',
            '-': '-',
            '+': '+',
            'x': 'x',
            'o': 'o',
            'O': 'O',
            '.': '.',
            '*': '*'
        }.get(matplotlib_marker_symbol)

        if accepted_hatching_symbol is None:
            warnings.warn(f'Unexpected marker symbol "{matplotlib_marker_symbol}" '
                          f'for original symbol"{original_marker_symbol}", set to "."')
            accepted_hatching_symbol = '.'

        color, alpha = mpl_conv.rgba_to_hex_and_alpha(get_from_k_v_list(k_v_list=symbol_properties, key='color'))
        size = get_from_k_v_list(k_v_list=symbol_properties, key='size')

        properties_list.append({
            'fill': None,
            'hatch': ''.join([accepted_hatching_symbol for _ in range(density)]),
            'edgecolor': color,  # in QGis, hatch color is face color. In matplotlib, edge color.
            'alpha': alpha,
        })


    return properties_list
