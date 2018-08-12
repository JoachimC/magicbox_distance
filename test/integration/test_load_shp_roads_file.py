import unittest

import magicbox_distance.shapefile as shapefile
import magicbox_distance.shapefile_parse as shapefile_parse


class TestLoadColumbiaRoads(unittest.TestCase):

    def test_load(self):
        # https://data.humdata.org/dataset/d8f6feda-6755-4e84-bd14-5c719bc5f37a (hotosm_col_roads_lines_shp.zip)
        roads_file = "/Users/joachim/Downloads/hotosm_col_roads_lines_shp/hotosm_col_roads_lines.shp"
        shapes = shapefile_parse.load(roads_file)

        for index, shape in enumerate(shapes):
            last_index = index
            self.assertEqual(shape[shapefile.SHAPE_TYPE_KEY], shapefile.ShapeType.POLYLINE)

        self.assertEqual(last_index + 1, 478321)


if __name__ == '__main__':
    unittest.main()
