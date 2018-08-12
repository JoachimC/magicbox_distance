import functools

from magicbox_distance.distance import using_latitude_and_longitude
from magicbox_distance.networkx_roads import START_KEY, END_KEY, DISTANCE_KEY, ID_KEY, create_road_id_from_points, \
    START_ID_KEY, END_ID_KEY, create_node_id
from magicbox_distance.shapefile import PARTS_KEY, POINTS_KEY


def to_networkx_roads(shapefile_records):
    parts = functools.reduce(lambda accumulated, record: extract_parts(accumulated, record), shapefile_records, [])
    points = [part[POINTS_KEY] for part in parts]
    return functools.reduce(to_networkx_road, points, [])


def extract_parts(accumulated, record):
    return accumulated + record[PARTS_KEY]


def to_networkx_road(accumulated, points):
    start = points[0]
    end = points[-1]
    distance = functools.reduce(lambda x, y: x + y,
                                map(using_latitude_and_longitude, points[1:], points[:-1]),
                                0)
    return accumulated + [
        {ID_KEY: create_road_id_from_points(start, end),
         START_ID_KEY: create_node_id(start),
         START_KEY: start,
         END_ID_KEY: create_node_id(end),
         END_KEY: end,
         DISTANCE_KEY: distance,
         POINTS_KEY: points}]
