import unittest

from magicbox_distance import shapefile
from magicbox_distance.shapefile import ShapeType


class TestLoadColumbiaRoads(unittest.TestCase):

    def test_load(self):
        # https://data.humdata.org/dataset/d8f6feda-6755-4e84-bd14-5c719bc5f37a (hotosm_col_roads_lines_shp.zip)
        roads_file = "/Users/joachim/Downloads/hotosm_col_roads_lines_shp/hotosm_col_roads_lines.shp"
        roads_generator = shapefile.load(roads_file)

        roads = list(roads_generator)
        self.assertEqual(len(roads), 478321)
        for road in roads_generator:
            self.assertEqual(road[shapefile.SHAPE_TYPE_KEY], ShapeType.POLYLINE)


if __name__ == '__main__':
    unittest.main()
