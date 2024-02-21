from ..dict_list_manipulations import get_from_k_v_list, no_empty_values
from .. import matplotlib_converters as mpl_conv


def properties_to_dicts(properties: list) -> list[dict]:
    marker = mpl_conv.marker(get_from_k_v_list(k_v_list=properties, key='name'))
    marker_size = mpl_conv.size(get_from_k_v_list(k_v_list=properties, key='size'))

    marker_face_color_rgba = get_from_k_v_list(k_v_list=properties, key='color')
    marker_face_color, alpha_marker_face = mpl_conv.rgba_to_hex_and_alpha(marker_face_color_rgba)

    cap_style = mpl_conv.cap_style(get_from_k_v_list(k_v_list=properties, key='cap_style'))
    join_style = mpl_conv.join_style(get_from_k_v_list(k_v_list=properties, key='joinstyle'))

    marker_edge_width = mpl_conv.size(get_from_k_v_list(k_v_list=properties, key='outline_width'))
    marker_edge_color_rgba = get_from_k_v_list(k_v_list=properties, key='outline_color')
    marker_edge_color, alpha_marker_edge = mpl_conv.rgba_to_hex_and_alpha(marker_edge_color_rgba)

    return [
        {
            'marker': marker,
            'markersize': marker_size,
            'markerfacecolor': marker_face_color,
            'markeredgewidth': marker_edge_width,
            'markeredgecolor': marker_edge_color,
            'capstyle': cap_style,
            'joinstyle': join_style,
        }
    ]
