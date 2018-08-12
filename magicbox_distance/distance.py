from geopy.distance import great_circle
from . import ureg

from magicbox_distance.networkx_roads import create_node_id
import networkx as nx


def using_latitude_and_longitude(first, second):
    return great_circle(first, second).kilometers * ureg.kilometres


def using_roads(roads, first, second):
    MG = nx.MultiGraph()
    weighted_edges = list(map(lambda x: (create_node_id(x[0]), create_node_id(x[1]), x[2]), roads))
    MG.add_weighted_edges_from(weighted_edges)

    GG = nx.Graph()
    for n, nbrs in MG.adjacency():
        for nbr, edict in nbrs.items():
            minvalue = min([d['weight'] for d in edict.values()])
            GG.add_edge(n, nbr, weight=minvalue)

    length = nx.shortest_path(GG, create_node_id(first), create_node_id(second))
    return length
