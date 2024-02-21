import unittest
from qgis_style_files_extractor.main import QmlToStyles


class MyTestCase(unittest.TestCase):
    def test_something(self):
        qml_path = 'qml_samples\\servitudes_d_utilité_publique_s.qml'
        styles = QmlToStyles(qml_path)
        print(styles.rules)
        self.assertEqual(True, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
