import xmltodict


def qml_to_dict(filepath: str) -> dict:
    assert filepath.find('.qml') != -1, f'not a qml file: {filepath}'

    with open(filepath, 'r') as f:
        xml_content = f.read()

    return xmltodict.parse(xml_content)
