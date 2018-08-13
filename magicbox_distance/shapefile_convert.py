import functools

from magicbox_distance.distance import using_latitude_and_longitude
from magicbox_distance.networkx_roads import START_KEY, END_KEY, DISTANCE_KEY, ID_KEY, create_road_id_from_points, \
    START_ID_KEY, END_ID_KEY, create_node_id
from magicbox_distance.shapefile import PARTS_KEY, POINTS_KEY, RECORD_NUMBER_KEY


def to_networkx_roads(shapefile_records):
    for record in shapefile_records:
        # if record[RECORD_NUMBER_KEY] > 10000: break
        parts = record[PARTS_KEY]
        nested_points = [part[POINTS_KEY] for part in parts]
        for points in nested_points:
            yield to_networkx_road(points)


def to_networkx_road(points):
    start = points[0]
    end = points[-1]
    distance = functools.reduce(lambda x, y: x + y,
                                map(using_latitude_and_longitude, points[1:], points[:-1]),
                                0)
    return {ID_KEY: create_road_id_from_points(start, end),
            START_ID_KEY: create_node_id(start),
            START_KEY: start,
            END_ID_KEY: create_node_id(end),
            END_KEY: end,
            DISTANCE_KEY: distance,
            POINTS_KEY: points}
