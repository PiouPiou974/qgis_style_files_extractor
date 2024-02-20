import copy
from .properties_to_dict import marker, fill
from .qml_reader import qml_to_dict
from .dict_list_manipulations import as_list, get_from_k_v_list


class QmlToStyles:
    layer_setting: dict
    geometry_type: str
    qml_style_categories: list[str]
    symbols: dict[str, list[dict]] = dict()
    rules: list[dict] = list()

    def __init__(self, filepath: str) -> None:
        layer_setting = qml_to_dict(filepath=filepath)
        assert 'qgis' in layer_setting.keys()
        self.layer_setting = layer_setting['qgis']

        assert 'renderer-v2' in self.layer_setting.keys()

        self.geometry_type = self.layer_setting.get('layerGeometryType')
        self.qml_style_categories = self.layer_setting.get('styleCategories', '').split('|')

        self.style_type = self.layer_setting['renderer-v2'].get('@type')
        assert self.style_type in ['RuleRenderer', 'singleSymbol'], \
            f'Style renderer type not planned : {self.style_type}'
        # todo : categorizedSymbol

        self.symbols_from_renderer()

        if self.style_type == 'RuleRenderer':
            self.rules_from_renderer()

        print(self.symbols)

    def rules_from_renderer(self) -> None:
        renderer = self.layer_setting['renderer-v2']
        assert 'rules' in renderer.keys()
        assert 'rule' in renderer['rules']
        rules = as_list(renderer['rules']['rule'])

        for rule in rules:
            rule_properties = {
                'label': rule['@label'],
                'filter': rule['@filter'],
                'symbol': rule['@symbol'],
            }
            self.rules.append(rule_properties)


    def symbols_from_renderer(self) -> None:
        renderer = self.layer_setting['renderer-v2']
        assert 'symbols' in renderer.keys()
        assert 'symbol' in renderer['symbols']
        symbols = as_list(renderer['symbols']['symbol'])

        for symbol in symbols:
            symbol_key = symbol.get('@name')
            symbol_type = symbol.get('@type')
            assert symbol_type in ['marker', 'fill'], \
                f'unexpected symbol type {symbol_type}'
            alpha = float(symbol.get('@alpha'))

            self.symbols[symbol_key] = list()

            assert 'layer' in symbol.keys()
            for layer in as_list(symbol['layer']):
                if symbol_type == 'marker':
                    layer_properties = marker.properties_to_dict(layer['prop'])
                if symbol_type == 'fill':
                    layer_properties = fill.properties_to_dict(layer['prop'])

                else:
                    raise ValueError

                layer_properties['alpha'] = alpha
                self.symbols[symbol_key].append(copy.deepcopy(layer_properties))
