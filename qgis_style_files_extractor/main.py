from typing import Literal

from .qml_reader import qml_to_dict
from .dict_list_manipulations import as_list
from .properties_to_dict import marker__simple_marker, fill__simple_fill, fill__point_pattern_fill, fill__marker_line


class QmlToStyles:
    geometry_type: str
    style_type: Literal['RuleRenderer', 'singleSymbol']
    qml_style_categories: list[str]
    symbols: dict[str, list[dict]] = dict()
    rules: list[dict] = list()

    def __init__(self, filepath: str) -> None:
        layer_setting = qml_to_dict(filepath=filepath)

        assert 'qgis' in layer_setting.keys()
        layer_setting = layer_setting['qgis']

        assert 'renderer-v2' in layer_setting.keys()
        self.geometry_type = layer_setting.get('layerGeometryType')
        self.qml_style_categories = layer_setting.get('styleCategories', '').split('|')

        self.style_type = layer_setting['renderer-v2'].get('@type')

        assert self.style_type in ['RuleRenderer', 'singleSymbol'], \
            f'Style renderer type not planned : {self.style_type}'
        # todo : categorizedSymbol

        self.symbols_from_renderer(layer_setting)

        if self.style_type == 'RuleRenderer':
            self.rules_from_renderer(layer_setting)

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
            alpha = float(symbol.get('@alpha'))  # does not seem to be relevant, alpha is coded inside each rgba values

            self.symbols[symbol_key] = list()

            assert 'layer' in symbol.keys()
            for layer in as_list(symbol['layer']):
                if symbol_type == 'marker':
                    layer_class = layer.get('@class')

                    if layer_class == 'SimpleMarker':
                        layer_properties_list = marker__simple_marker.properties_to_dicts(layer['prop'])

                    else:
                        raise ValueError(f'unexpected layer type {layer_class}')

                elif symbol_type == 'fill':
                    layer_class = layer.get('@class')

                    if layer_class == 'SimpleFill':
                        layer_properties_list = fill__simple_fill.properties_to_dicts(layer['prop'])
                    elif layer_class == 'PointPatternFill':
                        layer_properties_list = fill__point_pattern_fill.properties_and_symbol_to_dicts(
                            properties=layer['prop'],
                            symbols=layer['symbol'],
                        )
                    elif layer_class == 'MarkerLine':
                        layer_properties_list = fill__marker_line.properties_and_symbol_to_dicts(
                            properties=layer['prop'],
                            symbols=layer['symbol'],
                        )

                    else:
                        print(layer)
                        raise ValueError(f'unexpected layer type {layer_class}')
                else:
                    raise ValueError(f'unexpected symbol type {symbol_type}')

                self.symbols[symbol_key].extend(layer_properties_list)
