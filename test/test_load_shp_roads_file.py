import unittest

from magicbox_distance import roads


class TestLoadColumbiaRoads(unittest.TestCase):

    def test_load(self):
        # https://data.humdata.org/dataset/d8f6feda-6755-4e84-bd14-5c719bc5f37a (hotosm_col_roads_lines_shp.zip)
        roads_file = "/Users/joachim/Downloads/hotosm_col_roads_lines_shp/hotosm_col_roads_lines.shp"
        map = roads.load(roads_file)

        self.assertEqual(len(list(map)), 478321)
        self.fail("not implmented - check each entry has a valid looking structure")


if __name__ == '__main__':
    unittest.main()
