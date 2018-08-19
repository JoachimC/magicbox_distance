import unittest

import magicbox_distance.networkx_roads
import magicbox_distance.shapefile
from magicbox_distance import ureg

from geopy import Point
import networkx as nx

from magicbox_distance import distance
from magicbox_distance.convert_shapefile_to_networkx_graph import load_graph_from_shapefile_records


class TestLoadColumbiaRoads(unittest.TestCase):

    def test_pickle_graph(self):
        roads_file = "/Users/joachim/Downloads/hotosm_col_roads_lines_shp/hotosm_col_roads_lines.shp"
        shapes = magicbox_distance.shapefile.load_from_file(roads_file)
        networkx = magicbox_distance.networkx_roads.to_networkx_roads(shapes)
        G = load_graph_from_shapefile_records(networkx)
        nx.write_gpickle(G, "/tmp/columbia.roads.pickle")

    def test_unpickle_graph(self):
        G = nx.read_gpickle("/tmp/columbia.roads.pickle")

        expected_distance = 0.17716759526992643 * ureg.kilometres
        start = Point(-75.490017, +10.478256)
        end = Point(-75.488535, +10.480564)
        actual_distance = distance.using_route(G, start, end)
        self.assertEqual(actual_distance, expected_distance)


if __name__ == '__main__':
    unittest.main()
