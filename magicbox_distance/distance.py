from functools import reduce
import networkx as nx
from geopy.distance import great_circle

import magicbox_distance.convert_shapefile_to_networkx_graph as convert
from . import ureg


def using_latitude_and_longitude(first, second):
    return great_circle(first, second).kilometers * ureg.kilometres


def using_route(G, first, second):
    if first == second: return 0 * ureg.kilometres

    first_node_id = convert.create_node_id(first)
    second_node_id = convert.create_node_id(second)

    path = nx.shortest_path(G, source=first_node_id, target=second_node_id, weight="weight")
    return _calculate_path_distance(G, path) * ureg.kilometres


def _calculate_path_distance(G, path):
    pairs = map(lambda x, y: (y, x), path[1:], path[:-1])
    return reduce(lambda aggregate, pair: aggregate + _find_road_distance(G, pair), pairs, 0)


def _find_road_distance(G, pair):
    weights = nx.get_edge_attributes(G, "weight")

    outward_pair = pair
    if outward_pair in weights:
        return weights[outward_pair]

    inward_pair = outward_pair[1], outward_pair[0]
    if (inward_pair) in weights:
        return weights[inward_pair]
