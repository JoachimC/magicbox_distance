from functools import reduce
import networkx as nx
from geopy.distance import great_circle

from magicbox_distance.networkx_roads import create_node_id, START_KEY, END_KEY, DISTANCE_KEY, END_ID_KEY, START_ID_KEY
from . import ureg


def using_latitude_and_longitude(first, second):
    return great_circle(first, second).kilometers * ureg.kilometres


def using_roads(roads, first, second):
    if first == second: return 0 * ureg.kilometres

    MG = nx.MultiGraph()
    weighted_edges = map(lambda road: (road[START_ID_KEY], road[END_ID_KEY], road[DISTANCE_KEY]), roads)
    MG.add_weighted_edges_from(weighted_edges)

    first_node_id = create_node_id(first)
    second_node_id = create_node_id(second)
    path = nx.shortest_path(MG, first_node_id, second_node_id)
    distance = calculate_path_distance(roads, path)
    return distance


def calculate_path_distance(roads, path):
    pairs = map(lambda x, y: (x, y), path[1:], path[:-1])
    return reduce(lambda aggregate, pair: aggregate + find_road(roads, pair)[DISTANCE_KEY], pairs, 0)


def find_road(roads, pair):
    return next(road for road in roads if is_match(road, pair))


def is_match(road, pair):
    pair_start_id = pair[0]
    pair_end_id = pair[1]
    road_end_id = create_node_id(road[END_KEY])
    road_start_id = create_node_id(road[START_KEY])

    outward_match = road_start_id == pair_start_id and road_end_id == pair_end_id
    inward_match = road_end_id == pair_start_id and road_start_id == pair_end_id

    return outward_match or inward_match
