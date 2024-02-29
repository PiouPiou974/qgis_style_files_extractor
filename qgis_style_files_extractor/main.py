from math import gcd
from typing import Literal

from .matplotlib_converters.color import rgba_to_one_letter_color_and_alpha, rgb_hex_and_alpha_to_rgba
from .qml_reader import qml_extract_name_settings
from .dict_list_manipulations import as_list
from .qgis_converter import wkb_types
from .qgis_converter.options_and_properties import get_prop
from .properties_to_dict import marker__simple_marker, fill__simple_fill, fill__point_pattern_fill, fill__marker_line


class QmlToStyles:
    layer_name: str
    geometry_type: Literal[
        'Point', 'LineString', 'Polygon', 'MultiPoint', 'MultiLineString', 'MultiPolygon', 'Raster', None,
    ]
    style_type: Literal['singleSymbol', 'categorizedSymbol', 'RuleRenderer', 'singlebandpseudocolor']
    symbols: dict[str, list[dict]] = dict()
    rules: list[dict] = list()
    labeling: dict = dict()

    def __init__(self, filepath: str) -> None:
        self.layer_name, layer_setting = qml_extract_name_settings(filepath=filepath)

        assert 'qgis' in layer_setting.keys()
        layer_setting = layer_setting['qgis']

        # detect if raster or vector or invalid
        type_geometry = None
        if 'renderer-v2' in layer_setting.keys():
            type_geometry = 'vector'
        elif 'pipe' in layer_setting.keys():
            if 'rasterrenderer' in layer_setting['pipe'].keys():
                type_geometry = 'raster'

        assert type_geometry, ('This package cannot operate outside renderer-v2 for vector and rasterrenderer for '
                               'rasters. Please check QGis version and generate qml file with the newest version '
                               'possible.')

        if type_geometry == 'vector':
            self.extract_vector_styles(layer_setting)

        if type_geometry == 'raster':
            self.extract_raster_styles(layer_setting)

    def extract_raster_styles(self, layer_setting: dict) -> None:
        raster_renderer = layer_setting['pipe']['rasterrenderer']
        self.geometry_type = 'Raster'
        self.style_type = raster_renderer.get('@type')
        assert self.style_type in ['singlebandpseudocolor']

        def extract_single_band_pseudo_color() -> None:
            assert 'rastershader' in raster_renderer.keys()
            assert 'colorrampshader' in raster_renderer['rastershader'].keys()
            assert 'item' in raster_renderer['rastershader']['colorrampshader'].keys()

            v_min = int(raster_renderer['@classificationMin'])
            v_max = int(raster_renderer['@classificationMax'])

            color_sequence: list = raster_renderer['rastershader']['colorrampshader']['item']

            colors_values = {
                color['@value']: rgb_hex_and_alpha_to_rgba(color['@color'], int(color['@alpha']))
                for color in color_sequence
            }

            if not all([type(value) is int for value in colors_values.keys()]):
                # cas ou l'échelle comporte des paliers non entier. On simplifie
                listed_color_map = list(colors_values.values())
            else:
                values_gcd: int = gcd(*list(colors_values.keys()))
                values: list[int] = [int(value/values_gcd) for value in colors_values.keys()]
                colors = list(colors_values.values())

                listed_color_map = []
                step = 0
                for val in range(min(values), max(values) + 1):
                    if step < len(values) - 1:
                        if val >= values[step + 1]:
                            step += 1
                    listed_color_map.append(colors[step])

            self.symbols = {
                'v_min': v_min,
                'v_max': v_max,
                'listed_color_map_kwargs': {
                    'colors': listed_color_map,
                },
            }
            print(self.symbols)


        if self.style_type == 'singlebandpseudocolor':
            extract_single_band_pseudo_color()
        else:
            raise ValueError


    def extract_vector_styles(self, layer_setting: dict) -> None:
        self.geometry_type = wkb_types.geometry_type_from_wkb_enum(layer_setting.get('layerGeometryType'))

        self.style_type = layer_setting['renderer-v2'].get('@type')

        assert self.style_type in ['RuleRenderer', 'singleSymbol'], \
            f'Style renderer type not planned : {self.style_type}'
        # todo : categorizedSymbol

        self.symbols_from_renderer(layer_setting)

        if 'labeling' in layer_setting.keys():
            self.add_labeling(layer_setting)

        if self.style_type == 'RuleRenderer':
            self.rules_from_renderer(layer_setting)

    def add_labeling(self, layer_setting: dict) -> None:
        labeling = dict()

        try:
            labeling_settings = layer_setting['labeling']
            assert labeling_settings['@type'] == 'simple'
            text_style = labeling_settings['settings']['text-style']

            color, alpha = rgba_to_one_letter_color_and_alpha(text_style['@textColor'])
            # background_color, background_alpha = rgba_to_hex_and_alpha(text_style['@previewBkgrdColor'])

            labeling['field'] = text_style['@fieldName']
            labeling['annotate_kwargs'] = {
                'color': color,
                'alpha': alpha,
                'fontsize': int(text_style['@fontSize']),
                'fontstyle': 'italic' if text_style['@fontItalic'] == '1' else 'normal',
                'fontweight': int(text_style['@fontWeight']),
                'fontfamily': text_style['@fontFamily'],
                # 'backgroundcolor': background_color,
            }

        except Exception as e:
            print(e)
            labeling = {}

        self.labeling = labeling

    def rules_from_renderer(self, layer_setting: dict) -> None:
        renderer = layer_setting['renderer-v2']
        assert 'rules' in renderer.keys()
        assert 'rule' in renderer['rules']
        rules = as_list(renderer['rules']['rule'])

        for rule in rules:
            rule_properties = {
                'label': rule.get('@label', 'NO LABEL'),
                'filter': rule['@filter'],
                'symbol': self.symbols.get(rule['@symbol']),
            }
            self.rules.append(rule_properties)

    def symbols_from_renderer(self, layer_setting: dict) -> None:
        renderer = layer_setting['renderer-v2']
        assert 'symbols' in renderer.keys()
        assert 'symbol' in renderer['symbols']
        symbols = as_list(renderer['symbols']['symbol'])

        for symbol in symbols:
            symbol_key = symbol.get('@name')
            symbol_type = symbol.get('@type')
            assert symbol_type in ['marker', 'fill'], \
                f'unexpected symbol type {symbol_type}'

            # does not seem to be relevant, alpha is coded inside each rgba values
            # alpha = float(symbol.get('@alpha'))

            self.symbols[symbol_key] = list()

            assert 'layer' in symbol.keys()
            for layer in as_list(symbol['layer']):
                if symbol_type == 'marker':
                    layer_class = layer.get('@class')

                    if layer_class == 'SimpleMarker':
                        prop = get_prop(layer)
                        layer_properties_list = marker__simple_marker.properties_to_dicts(prop)

                    else:
                        raise ValueError(f'unexpected layer type {layer_class}')

                elif symbol_type == 'fill':
                    layer_class = layer.get('@class')

                    if layer_class == 'SimpleFill':
                        prop = get_prop(layer)
                        layer_properties_list = fill__simple_fill.properties_to_dicts(prop)
                    elif layer_class == 'PointPatternFill':
                        prop = get_prop(layer)
                        layer_properties_list = fill__point_pattern_fill.properties_and_symbol_to_dicts(
                            properties=prop,
                            symbols=layer['symbol'],
                        )
                    elif layer_class == 'MarkerLine':
                        prop = get_prop(layer)
                        layer_properties_list = fill__marker_line.properties_and_symbol_to_dicts(
                            properties=prop,
                            symbols=layer['symbol'],
                        )

                    else:
                        print(layer)
                        raise ValueError(f'unexpected layer type {layer_class}')
                else:
                    raise ValueError(f'unexpected symbol type {symbol_type}')

                self.symbols[symbol_key].extend(layer_properties_list)

    @property
    def dict(self) -> dict:
        return {
            'name': self.layer_name,
            'geometry_type': self.geometry_type,
            'style_type': self.style_type,
            'symbols': self.symbols,
            'rules': self.rules,
            'labeling': self.labeling,
        }
