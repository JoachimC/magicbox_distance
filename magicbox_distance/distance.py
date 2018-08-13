import time
from functools import reduce
import networkx as nx
from geopy.distance import great_circle

from magicbox_distance.networkx_roads import create_node_id, START_KEY, END_KEY, DISTANCE_KEY, END_ID_KEY, START_ID_KEY
from . import ureg


def using_latitude_and_longitude(first, second):
    return great_circle(first, second).kilometers * ureg.kilometres


def using_roads(roads, first, second):
    if first == second: return 0 * ureg.kilometres

    t = time.time()
    G = nx.DiGraph()
    for road in roads:
        G.add_edge(road[START_ID_KEY], road[END_ID_KEY], weight=road[DISTANCE_KEY])

    print("loaded in {interval}".format(interval=time.time() - t))
    t = time.time()

    first_node_id = create_node_id(first)
    second_node_id = create_node_id(second)
    path = nx.shortest_path(G, source=first_node_id, target=second_node_id, weight="weight")
    distance = calculate_path_distance(G, path)
    print("routed in {interval}".format(interval=time.time() - t))

    return distance


def calculate_path_distance(G, path):
    pairs = map(lambda x, y: (y, x), path[1:], path[:-1])
    return reduce(lambda aggregate, pair: aggregate + find_road_distance(G, pair), pairs, 0)


def find_road_distance(G, pair):
    weights = nx.get_edge_attributes(G, "weight")

    outward_pair = pair
    if outward_pair in weights:
        return weights[outward_pair]

    inward_pair = outward_pair[1], outward_pair[0]
    if (inward_pair) in weights:
        return weights[inward_pair]
