import unittest

from magicbox_distance import ureg

from geopy import Point
import networkx as nx

import magicbox_distance.shapefile_parse as shapefile_parse
from magicbox_distance import shapefile_convert, distance
from magicbox_distance.distance import load_graph


class TestLoadColumbiaRoads(unittest.TestCase):

    def test_pickle_graph(self):
        roads_file = "/Users/joachim/Downloads/hotosm_col_roads_lines_shp/hotosm_col_roads_lines.shp"
        shapes = shapefile_parse.load(roads_file)
        networkx = shapefile_convert.to_networkx_roads(shapes)
        G = load_graph(networkx)
        nx.write_gpickle(G, "/tmp/columbia.roads.pickle")

    def test_unpickle_graph(self):
        G = nx.read_gpickle("/tmp/columbia.roads.pickle")

        expected_distance = 0.17716759526992643 * ureg.kilometres
        start = Point(-75.490017, +10.478256)
        end = Point(-75.488535, +10.480564)
        actual_distance = distance.route(G, start, end)
        self.assertEqual(actual_distance, expected_distance)


if __name__ == '__main__':
    unittest.main()
