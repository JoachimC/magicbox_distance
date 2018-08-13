import unittest

import networkx as nx


class TestLoadColumbiaRoadsNetworkXNative(unittest.TestCase):

    def test_load(self):
        # https://data.humdata.org/dataset/d8f6feda-6755-4e84-bd14-5c719bc5f37a (hotosm_col_roads_lines_shp.zip)
        roads_file = "/Users/joachim/Downloads/hotosm_col_roads_lines_shp/hotosm_col_roads_lines.shp"
        # todo : ImportError: read_shp requires OGR: http://www.gdal.org/
        G = nx.read_shp(roads_file)


if __name__ == '__main__':
    unittest.main()
