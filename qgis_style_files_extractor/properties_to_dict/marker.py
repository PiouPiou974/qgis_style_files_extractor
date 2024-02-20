from ..dict_list_manipulations import get_from_k_v_list, no_empty_values
from .. import matplotlib_converters as mpl_conv


def properties_to_dict(properties: list) -> dict:
    markerfacecolor = get_from_k_v_list(k_v_list=properties, key='color')
    capstyle = get_from_k_v_list(k_v_list=properties, key='cap_style')
    joinstyle = get_from_k_v_list(k_v_list=properties, key='joinstyle')
    marker = get_from_k_v_list(k_v_list=properties, key='name')
    markeredgewidth = get_from_k_v_list(k_v_list=properties, key='outline_width')
    markeredgecolor = get_from_k_v_list(k_v_list=properties, key='outline_color')
    markersize = get_from_k_v_list(k_v_list=properties, key='size')

    return no_empty_values({
        'markerfacecolor': mpl_conv.rgba_to_hex(markerfacecolor),
        'capstyle': mpl_conv.cap_style(capstyle),
        'joinstyle': mpl_conv.join_style(joinstyle),
        'marker': mpl_conv.marker(marker),
        'markeredgewidth': mpl_conv.size(markeredgewidth),
        'markeredgecolor': mpl_conv.rgba_to_hex(markeredgecolor),
        'markersize': mpl_conv.size(markersize),
    })
