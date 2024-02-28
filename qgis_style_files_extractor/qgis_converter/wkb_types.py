import warnings
from typing import Literal


def geometry_type_from_wkb_enum(
        wkb_enum: str
) -> Literal['Point', 'LineString', 'Polygon', 'MultiPoint', 'MultiLineString', 'MultiPolygon', None]:
    # https://qgis.org/pyqgis/3.28/core/QgsWkbTypes.html#qgis.core.QgsWkbTypes
    # Wkb enum from QGis
    geometry_type = {
        '1': 'Point',
        '2': 'LineString',
        '3': 'Polygon',
        '4': 'MultiPoint',
        '5': 'MultiLineString',
        '6': 'MultiPolygon',
    }.get(wkb_enum)

    if geometry_type is None:
        warnings.warn(f'Unknown geometry type from wkb enum {wkb_enum}')
    return geometry_type
