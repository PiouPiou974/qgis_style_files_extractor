import xmltodict


def qml_extract_name_settings(filepath: str) -> tuple[str, dict]:
    assert filepath.find('.qml') != -1, f'not a qml file: {filepath}'

    layer_name = filepath.split('\\')[-1].replace('.qml', '')

    with open(filepath, 'r') as f:
        encoding = f.encoding
        xml_content = f.read().encode(encoding)
    layer_settings = xmltodict.parse(xml_content)
    print(layer_settings)
    return layer_name, layer_settings
