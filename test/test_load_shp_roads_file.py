import unittest

import magicbox_distance.shapefile as shapefile
import magicbox_distance.shapefile_parse as shapefile_parse


class TestLoadColumbiaRoads(unittest.TestCase):

    def test_load(self):
        # https://data.humdata.org/dataset/d8f6feda-6755-4e84-bd14-5c719bc5f37a (hotosm_col_roads_lines_shp.zip)
        roads_file = "/Users/joachim/Downloads/hotosm_col_roads_lines_shp/hotosm_col_roads_lines.shp"
        roads = list(shapefile_parse.load(roads_file))
        self.assertEqual(len(roads), 478321)
        for road in roads:
            self.assertEqual(road[shapefile.SHAPE_TYPE_KEY], shapefile.ShapeType.POLYLINE)

if __name__ == '__main__':
    unittest.main()
