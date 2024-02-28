from typing import Literal

from .matplotlib_converters.color import rgba_to_one_letter_color_and_alpha
from .qml_reader import qml_extract_name_settings
from .dict_list_manipulations import as_list
from .qgis_converter import wkb_types
from .qgis_converter.options_and_properties import get_prop
from .properties_to_dict import marker__simple_marker, fill__simple_fill, fill__point_pattern_fill, fill__marker_line


class QmlToStyles:
    layer_name: str
    geometry_type: Literal['Point', 'LineString', 'Polygon', 'MultiPoint', 'MultiLineString', 'MultiPolygon', None]
    style_type: Literal['singleSymbol', 'categorizedSymbol', 'RuleRenderer']
    symbols: dict[str, list[dict]] = dict()
    rules: list[dict] = list()
    labeling: dict = dict()

    def __init__(self, filepath: str) -> None:
        self.layer_name, layer_setting = qml_extract_name_settings(filepath=filepath)

        assert 'qgis' in layer_setting.keys()
        layer_setting = layer_setting['qgis']

        assert 'renderer-v2' in layer_setting.keys(), ('This package cannot operate outside renderer-v2. '
                                                       'Please check QGis version and generate qml file with'
                                                       'the newest version possible.')

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

        self.labeling = labeling

    def rules_from_renderer(self, layer_setting: dict) -> None:
        renderer = layer_setting['renderer-v2']
        assert 'rules' in renderer.keys()
        assert 'rule' in renderer['rules']
        rules = as_list(renderer['rules']['rule'])

        for rule in rules:
            rule_properties = {
                'label': rule['@label'],
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
