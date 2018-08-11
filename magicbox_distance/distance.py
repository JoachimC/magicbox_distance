from geopy.distance import great_circle

import networkx as nx


def using_latitude_and_longitude_in_km(first, second):
    return great_circle(first, second).kilometers


def using_roads_in_km(roads, first, second):
    MG = nx.MultiGraph()
    weighted_edges = list(map(lambda x: (create_node_name(x[0]), create_node_name(x[1]), x[2]), roads))
    MG.add_weighted_edges_from(weighted_edges)

    GG = nx.Graph()
    for n, nbrs in MG.adjacency():
        for nbr, edict in nbrs.items():
            minvalue = min([d['weight'] for d in edict.values()])
            GG.add_edge(n, nbr, weight=minvalue)

    length = nx.shortest_path_length(GG, create_node_name(first), create_node_name(second))
    return length


def create_node_name(node):
    return "{x:+f}{y:+f}".format(x=node[0], y=node[1])
