from ..dict_list_manipulations import get_from_k_v_list, no_empty_values
from .. import matplotlib_converters as mpl_conv


def properties_to_dict(properties: list) -> dict:
    facecolor = get_from_k_v_list(k_v_list=properties, key='color')
    hatch = get_from_k_v_list(k_v_list=properties, key='style')
    fill = get_from_k_v_list(k_v_list=properties, key='style')
    capstyle = get_from_k_v_list(k_v_list=properties, key='cap_style')
    joinstyle = get_from_k_v_list(k_v_list=properties, key='joinstyle')
    linestyle = get_from_k_v_list(k_v_list=properties, key='outline_style')
    linewidth = get_from_k_v_list(k_v_list=properties, key='outline_width')
    edgecolor = get_from_k_v_list(k_v_list=properties, key='outline_color')

    return no_empty_values({
        'facecolor': mpl_conv.rgba_to_hex(facecolor),
        'hatch': mpl_conv.hatch_from_fill_style(hatch),  # todo : if hatch is not None, set edgecolor to facecolor
        'fill': fill == 'solid',
        'capstyle': mpl_conv.cap_style(capstyle),
        'joinstyle': mpl_conv.join_style(joinstyle),
        'linewidth': mpl_conv.size(linewidth),
        'linestyle': mpl_conv.line_style(linestyle),
        'edgecolor': mpl_conv.rgba_to_hex(edgecolor),
    })


