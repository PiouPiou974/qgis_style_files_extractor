import unittest
from qgis_style_files_extractor.main import QmlToStyles
import pprint


class MyTestCase(unittest.TestCase):
    def test_something(self):
        qml_path = 'qml_samples\\postes_de_transformation.qml'
        styles = QmlToStyles(qml_path)
        print(styles.dict)
        self.assertEqual(True, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
