# from https://www.esri.com/library/whitepapers/pdfs/shapefile.pdf
from struct import unpack, error

# file header attributes
POLYLINE = 3

FILE_CODE_EXPECTED = 9994
VERSION_EXPECTED = 1000
SHAPE_TYPE_EXPECTED = POLYLINE

FILE_CODE_KEY = "file code"
FILE_LENGTH_KEY = "file length"
VERSION_KEY = "version"
SHAPE_TYPE_KEY = "shape type"

# record attributes
RECORD_NUMBER_KEY = "record number"
CONTENT_LENGTH_KEY = "content length"


def load(filePath):
    with open(filePath, "rb") as f:
        file_header = read_file_header(f)
        check_file_header(file_header)
        try:
            while True:
                yield read_record(f)
        except EOFError:
            pass
        except error:
            pass


def read_file_header(f):
    header_raw = unpack(">IIIIIII", f.read(28)) + unpack("<IIdddddddd", f.read(72))
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
    assert header[SHAPE_TYPE_KEY] == SHAPE_TYPE_EXPECTED, "Expected '{field}'={expected} but was {actual}" \
        .format(field=SHAPE_TYPE_KEY, expected=SHAPE_TYPE_EXPECTED, actual=header[SHAPE_TYPE_KEY])


def read_record(f):
    row_header = read_row_header(f)
    return read_poly_line(row_header, f)


def read_row_header(f):
    record_number, content_length = unpack(">II", f.read(8))
    return {RECORD_NUMBER_KEY: record_number, CONTENT_LENGTH_KEY: content_length}


def read_poly_line(row_header, f):
    contentLength = row_header[CONTENT_LENGTH_KEY]
    f.read(contentLength * 2)
    return {RECORD_NUMBER_KEY: row_header[RECORD_NUMBER_KEY]}
