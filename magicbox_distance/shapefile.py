# from https://www.esri.com/library/whitepapers/pdfs/shapefile.pdf
from enum import IntEnum


class ShapeType(IntEnum):
    POLYLINE = 3


# record attributes
RECORD_NUMBER_KEY = "record number"
PART_NUMBER_KEY = "part number"
PARTS_KEY = "parts"
POINTS_KEY = "points"
SHAPE_TYPE_KEY = "shape type"

# point attributes
POINT_X_KEY = "x"
POINT_Y_KEY = "y"


def create_record(record_number, shape_type, parts):
    return {RECORD_NUMBER_KEY: record_number,
            SHAPE_TYPE_KEY: shape_type,
            PARTS_KEY: parts}


def create_part(index, points):
    return {PART_NUMBER_KEY: index, POINTS_KEY: points}


def create_point(point_x, point_y):
    return {POINT_X_KEY: point_x, POINT_Y_KEY: point_y}
