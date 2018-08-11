import functools
from magicbox_distance.shapefile import PARTS_KEY, POINTS_KEY, POINT_X_KEY, POINT_Y_KEY
import magicbox_distance.distance as distance


def to_networkx_roads(shapefile_records):
    parts = functools.reduce(lambda accumulated, this: extract_parts(accumulated, this), shapefile_records, [])
    points = list(map(lambda part: part[POINTS_KEY], parts))
    return functools.reduce(to_networkx_road, points, [])


def extract_parts(accumulated, this):
    return accumulated + this[PARTS_KEY]


def to_networkx_road(accumulated, points):
    start = to_tuple(points[0])
    end = to_tuple(points[-1])
    points_as_tuples = list(map(to_tuple, points))
    distance_km = functools.reduce(lambda x, y: x + y,
                                   map(distance.using_latitude_and_longitude_in_km, points_as_tuples[1:], points_as_tuples[:-1]),
                                   0)
    return accumulated + [(start, end, distance_km)]


def to_tuple(point):
    return (point[POINT_Y_KEY], point[POINT_Y_KEY])