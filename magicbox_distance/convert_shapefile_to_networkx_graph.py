# from https://www.esri.com/library/whitepapers/pdfs/shapefile.pdf
import functools

import networkx as nx

from magicbox_distance import ureg
from magicbox_distance.distance import using_latitude_and_longitude
from magicbox_distance.shapefile import PARTS_KEY, POINTS_KEY

ID_KEY = "id"
START_ID_KEY = "start_id"
END_ID_KEY = "end_id"
START_KEY = "start"
END_KEY = "end"
DISTANCE_KEY = "distance"


def create_node_id(node):
    return "{latitude:+f},{longitude:+f}".format(latitude=node.latitude, longitude=node.longitude)


def _create_edge_id_from_node_ids(start_node_id, end_node_id):
    return "{start} to {end}".format(start=start_node_id, end=end_node_id)


def _create_road_id_from_points(start, end):
    return _create_edge_id_from_node_ids(create_node_id(start), create_node_id(end))


def load_graph_from_shapefile_records(shapefile_record):
    G = nx.Graph()
    for shape in shapefile_record:
        G.add_edge(shape[START_ID_KEY], shape[END_ID_KEY], weight=shape[DISTANCE_KEY].to(ureg.kilometres).magnitude)
    return G


def _to_networkx_graph(shapefile_records):
    for record in shapefile_records:
        # if record[RECORD_NUMBER_KEY] > 10000: break
        parts = record[PARTS_KEY]
        nested_points = [part[POINTS_KEY] for part in parts]
        for points in nested_points:
            yield _to_networkx_edge(points)


def _to_networkx_edge(points):
    start = points[0]
    end = points[-1]
    distance = functools.reduce(lambda x, y: x + y,
                                map(using_latitude_and_longitude, points[1:], points[:-1]),
                                0)
    return {ID_KEY: _create_road_id_from_points(start, end),
            START_ID_KEY: create_node_id(start),
            START_KEY: start,
            END_ID_KEY: create_node_id(end),
            END_KEY: end,
            DISTANCE_KEY: distance,
            POINTS_KEY: points}