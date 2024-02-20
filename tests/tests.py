import unittest
from qgis_style_files_extractor.main import QmlToStyles


class MyTestCase(unittest.TestCase):
    def test_something(self):
        qml_path = 'qml_samples\\test.qml'
        styles = QmlToStyles(qml_path)
        self.assertEqual(True, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
