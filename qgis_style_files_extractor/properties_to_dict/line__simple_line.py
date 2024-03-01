from ..dict_list_manipulations import get_from_k_v_list
from .. import matplotlib_converters as mpl_conv


def properties_to_dicts(properties: list, general_alpha: float) -> list[dict]:
    line_style = mpl_conv.line_style(get_from_k_v_list(k_v_list=properties, key='line_style'))
    line_color_rgba = get_from_k_v_list(k_v_list=properties, key='line_color')
    line_color, alpha_line = mpl_conv.rgba_to_hex_and_alpha(line_color_rgba)
    line_width = mpl_conv.size(get_from_k_v_list(k_v_list=properties, key='line_width'))
    cap_style = mpl_conv.cap_style(get_from_k_v_list(k_v_list=properties, key='capstyle'))
    join_style = mpl_conv.join_style(get_from_k_v_list(k_v_list=properties, key='joinstyle'))

    # todo : markers
    # render fill, hatch and line in different dict
    properties_list = [
        {
            'linestyle': line_style,
            'linewidth': line_width,
            'color': line_color,
            'alpha': alpha_line * general_alpha,
            'capstyle': cap_style,
            'joinstyle': join_style,
        }
    ]

    return properties_list
