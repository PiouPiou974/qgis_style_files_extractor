import warnings
from typing import Literal


def geometry_type_from_wkb_enum(
        wkb_enum: str
) -> Literal['Point', 'LineString', 'Polygon', 'MultiPoint', 'MultiLineString', 'MultiPolygon', None]:
    # https://qgis.org/pyqgis/3.28/core/QgsWkbTypes.html#qgis.core.QgsWkbTypes
    # Wkb enum from QGis
    # curiously, QGis appears to be using the WKB standards minus 1 (1 is not a Point but a LineString)
    geometry_type = {
        '0': 'Point',
        '1': 'LineString',
        '2': 'Polygon',
        '3': 'MultiPoint',
        '4': 'MultiLineString',
        '5': 'MultiPolygon',
        '6': 'GeometryCollection',
    }.get(wkb_enum)

    if geometry_type is None:
        warnings.warn(f'Unknown geometry type from wkb enum {wkb_enum}')
    return geometry_type
