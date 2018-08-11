# from https://www.esri.com/library/whitepapers/pdfs/shapefile.pdf
from functools import reduce

from struct import unpack, error
from enum import IntEnum
from numpy import array_split


class ShapeType(IntEnum):
    POLYLINE = 3


# file header attributes
FILE_CODE_EXPECTED = 9994
VERSION_EXPECTED = 1000

FILE_CODE_KEY = "file code"
FILE_LENGTH_KEY = "file length"
VERSION_KEY = "version"
SHAPE_TYPE_KEY = "shape type"

# record attributes
RECORD_NUMBER_KEY = "record number"
CONTENT_LENGTH_KEY = "content length"
PART_NUMBER_KEY = "part number"
PARTS_KEY = "parts"
POINTS_KEY = "points"

POINT_X_KEY = "x"
POINT_Y_KEY = "y"


def load(filePath):
    with open(filePath, "rb") as f:
        file_header = read_file_header(f)
        check_file_header(file_header)
        try:
            while True:
                yield (read_record(f))
        except EOFError:
            pass


def read_bytes_with_eof_check(f, size):
    buffer = f.read(size)
    if not buffer:
        raise EOFError
    return buffer


def read_file_header(f):
    header_raw = unpack(">IIIIIII", read_bytes_with_eof_check(f, 28)) + unpack("<IIdddddddd",
                                                                               read_bytes_with_eof_check(f, 72))
    file_code, \
    unused1, \
    unused2, \
    unused3, \
    unused4, \
    unused5, \
    file_length, \
    version, \
    shape_type, \
    bounding_box_x_min, \
    bounding_box_y_min, \
    bounding_box_x_max, \
    bounding_box_y_max, \
    bounding_box_z_min, \
    bounding_box_z_max, \
    bounding_box_m_min, \
    bounding_box_m_max \
        = header_raw
    header = {FILE_CODE_KEY: file_code, FILE_LENGTH_KEY: file_length, VERSION_KEY: version, SHAPE_TYPE_KEY: shape_type}
    return header


def check_file_header(header):
    assert header[FILE_CODE_KEY] == FILE_CODE_EXPECTED, "Expected '{field}'={expected} but was {actual}" \
        .format(field=FILE_CODE_KEY, expected=FILE_CODE_EXPECTED, actual=header[FILE_CODE_KEY])
    assert header[VERSION_KEY] == VERSION_EXPECTED, "Expected '{field}'={expected} but was {actual}" \
        .format(field=VERSION_KEY, expected=VERSION_EXPECTED, actual=header[VERSION_KEY])
    assert header[SHAPE_TYPE_KEY] == ShapeType.POLYLINE, "Expected '{field}'={expected} but was {actual}" \
        .format(field=SHAPE_TYPE_KEY, expected=ShapeType.POLYLINE, actual=header[SHAPE_TYPE_KEY])


def read_record(f):
    row_header = read_row_header(f)
    return read_poly_line(row_header, f)


def read_row_header(f):
    record_number, content_length = unpack(">II", read_bytes_with_eof_check(f, 8))
    return {RECORD_NUMBER_KEY: record_number, CONTENT_LENGTH_KEY: content_length}


def read_poly_line(row_header, f):
    polyline_prefix_raw = unpack("<IddddII", read_bytes_with_eof_check(f, 44))

    shape_type, \
    bounding_box_x_min, \
    bounding_box_y_min, \
    bounding_box_x_max, \
    bounding_box_y_max, \
    number_of_parts, \
    number_of_points \
        = polyline_prefix_raw

    part_indexes = list(map(lambda _: read_part_index(f), range(number_of_parts)))
    points = list(map(lambda _: read_point(f), range(number_of_points)))
    parts = make_parts(part_indexes, points)

    return {RECORD_NUMBER_KEY: row_header[RECORD_NUMBER_KEY],
            SHAPE_TYPE_KEY: shape_type,
            PARTS_KEY: parts}


def read_point(f):
    point_raw = unpack("<dd", read_bytes_with_eof_check(f, 16))
    point_x, point_y = point_raw
    return {POINT_X_KEY: point_x, POINT_Y_KEY: point_y}


def read_part_index(f):
    part_index = unpack("<I", read_bytes_with_eof_check(f, 4))
    return part_index[0]


def make_parts(part_indexes, points):
    _, *point_sets = array_split(points, part_indexes)
    result = list(map(lambda x: {PART_NUMBER_KEY: x[0] + 1, POINTS_KEY: x[1]}, enumerate(point_sets)))
    return result
