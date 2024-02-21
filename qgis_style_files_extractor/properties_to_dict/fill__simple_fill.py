from ..dict_list_manipulations import get_from_k_v_list
from .. import matplotlib_converters as mpl_conv


def properties_to_dicts(properties: list) -> list[dict]:
    face_color_rgba = get_from_k_v_list(k_v_list=properties, key='color')
    face_color, alpha_face = mpl_conv.rgba_to_hex_and_alpha(face_color_rgba)

    fill_or_hatch = get_from_k_v_list(k_v_list=properties, key='style')
    fill = fill_or_hatch == 'solid'
    hatch = mpl_conv.hatch_from_fill_style(fill_or_hatch)

    line_style = mpl_conv.line_style(get_from_k_v_list(k_v_list=properties, key='outline_style'))
    edge_color_rgba = get_from_k_v_list(k_v_list=properties, key='outline_color')
    edge_color, alpha_edge = mpl_conv.rgba_to_hex_and_alpha(edge_color_rgba)
    line_width = mpl_conv.size(get_from_k_v_list(k_v_list=properties, key='outline_width'))
    cap_style = mpl_conv.cap_style(get_from_k_v_list(k_v_list=properties, key='cap_style'))
    join_style = mpl_conv.join_style(get_from_k_v_list(k_v_list=properties, key='joinstyle'))

    # render fill, hatch and line in different dict
    properties_list = list()

    if fill:
        # fill dict
        properties_list.append({
            'fill': fill,
            'facecolor': face_color,
            'alpha': alpha_face,
        })

    if hatch:
        # hatch dict
        properties_list.append({
            'fill': None,
            'hatch': hatch,
            'edgecolor': face_color,  # in QGis, hatch color is face color. In matplotlib, edge color.
            'alpha': alpha_face,
        })

    if line_style:
        # line dict
        properties_list.append({
            'fill': None,
            'linestyle': line_style,
            'edgecolor': edge_color,
            'alpha': alpha_face,
            'capstyle': cap_style,
            'joinstyle': join_style,
            'linewidth': line_width,
        })

    return properties_list
