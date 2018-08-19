# from https://www.esri.com/library/whitepapers/pdfs/shapefile.pdf
from enum import IntEnum
from struct import unpack

from geopy import Point
from numpy import array_split


class ShapeType(IntEnum):
    POLYLINE = 3


# record attributes
RECORD_NUMBER_KEY = "record number"
PART_NUMBER_KEY = "part number"
PARTS_KEY = "parts"
POINTS_KEY = "points"
SHAPE_TYPE_KEY = "shape type"


def create_record(record_number, shape_type, parts):
    return {RECORD_NUMBER_KEY: record_number,
            SHAPE_TYPE_KEY: shape_type,
            PARTS_KEY: parts}


def create_part(index, points):
    return {PART_NUMBER_KEY: index, POINTS_KEY: points}


FILE_CODE_EXPECTED = 9994
VERSION_EXPECTED = 1000
CONTENT_LENGTH_KEY = "content length"
FILE_CODE_KEY = "file code"
FILE_LENGTH_KEY = "file length"
VERSION_KEY = "version"


def load_from_file(filePath):
    with open(filePath, "rb") as f:
        file_header = _read_file_header(f)
        _check_file_header(file_header)
        try:
            while True:
                yield _read_record(f)
        except EOFError:
            pass


def _read_bytes_with_eof_check(f, size):
    buffer = f.read(size)
    if not buffer:
        raise EOFError
    return buffer


def _read_file_header(f):
    header_raw = unpack(">IIIIIII", _read_bytes_with_eof_check(f, 28)) + unpack("<IIdddddddd",
                                                                                _read_bytes_with_eof_check(f, 72))
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
    header = {FILE_CODE_KEY: file_code, FILE_LENGTH_KEY: file_length, VERSION_KEY: version,
              SHAPE_TYPE_KEY: shape_type}
    return header


def _check_file_header(header):
    assert header[FILE_CODE_KEY] == FILE_CODE_EXPECTED, "Expected '{field}'={expected} but was {actual}" \
        .format(field=FILE_CODE_KEY, expected=FILE_CODE_EXPECTED, actual=header[FILE_CODE_KEY])
    assert header[VERSION_KEY] == VERSION_EXPECTED, "Expected '{field}'={expected} but was {actual}" \
        .format(field=VERSION_KEY, expected=VERSION_EXPECTED, actual=header[VERSION_KEY])
    assert header[
               SHAPE_TYPE_KEY] == ShapeType.POLYLINE, "Expected '{field}'={expected} but was {actual}" \
        .format(field=SHAPE_TYPE_KEY, expected=ShapeType.POLYLINE,
                actual=header[SHAPE_TYPE_KEY])


def _read_record(f):
    row_header = _read_row_header(f)
    return _read_poly_line(row_header, f)


def _read_row_header(f):
    record_number, content_length = unpack(">II", _read_bytes_with_eof_check(f, 8))
    return {RECORD_NUMBER_KEY: record_number, CONTENT_LENGTH_KEY: content_length}


def _read_poly_line(row_header, f):
    polyline_prefix_raw = unpack("<IddddII", _read_bytes_with_eof_check(f, 44))

    shape_type, \
    bounding_box_x_min, \
    bounding_box_y_min, \
    bounding_box_x_max, \
    bounding_box_y_max, \
    number_of_parts, \
    number_of_points \
        = polyline_prefix_raw

    part_indexes = [_read_part_index(f) for _ in range(number_of_parts)]
    points = [_read_point(f) for _ in range(number_of_points)]
    parts = _make_parts(part_indexes, points)

    return create_record(row_header[RECORD_NUMBER_KEY], shape_type, parts)


def _read_point(f):
    point_raw = unpack("<dd", _read_bytes_with_eof_check(f, 16))
    point_x, point_y = point_raw
    return Point(point_x, point_y)


def _read_part_index(f):
    part_index = unpack("<I", _read_bytes_with_eof_check(f, 4))
    return part_index[0]


def _make_parts(part_indexes, points):
    _, *point_sets = array_split(points, part_indexes)
    result = [create_part(x[0] + 1, x[1]) for x in enumerate(point_sets)]
    return result