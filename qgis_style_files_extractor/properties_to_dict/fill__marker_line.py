import warnings

from ..dict_list_manipulations import get_from_k_v_list, as_list
from .. import matplotlib_converters as mpl_conv


def properties_and_symbol_to_dicts(properties: list, symbols: list, general_alpha: float) -> list[dict]:
    warnings.warn('MarkerLine fill is currently not well supported in matplotlib. Transformed into dots.')
    # FutureDev
    interval = mpl_conv.size(get_from_k_v_list(k_v_list=properties, key='interval'))

    properties_list = list()

    symbols = as_list(symbols)
    for symbol in symbols:
        # get the first layer of the symbol to retrieve data :
        symbol_properties = symbol['layer']['prop']

        # FutureDev
        original_marker_symbol = get_from_k_v_list(k_v_list=symbol_properties, key='name')

        selected_line_style = ':'

        size = mpl_conv.size(get_from_k_v_list(k_v_list=symbol_properties, key='size'))
        color, alpha = mpl_conv.rgba_to_hex_and_alpha(get_from_k_v_list(k_v_list=symbol_properties, key='color'))

        properties_list.append({
            'fill': None,
            'linestyle': selected_line_style,
            'linewidth': size,
            'edgecolor': color,  # in QGis, hatch color is face color. In matplotlib, edge color.
            'alpha': alpha * general_alpha,
        })

    return properties_list
