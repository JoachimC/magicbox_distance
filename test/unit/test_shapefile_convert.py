import unittest

from magicbox_distance import ureg
import magicbox_distance.shapefile_convert as shapefile_convert
import test.unit.data_factory as data_factory

from magicbox_distance.networkx_roads import START_KEY, END_KEY, DISTANCE_KEY


class TestShapeFileConvert(unittest.TestCase):
    start = data_factory.right_angle_start
    middle = data_factory.right_angle_middle
    end = data_factory.right_angle_end

    def test_simple_triangle(self):
        road = data_factory.create_part(self.start, self.middle, self.end)
        shapefile = data_factory.create_shapefile([road])
        networkx = shapefile_convert.to_networkx_roads(shapefile)

        self.assertEqual(len(networkx), 1)
        self.assertEqual(networkx[0][START_KEY], self.start)
        self.assertEqual(networkx[0][END_KEY], self.end)
        self.assertTrue(abs(networkx[0][DISTANCE_KEY] - data_factory.right_angle_distance) < 1 * ureg.millimetre)


if __name__ == '__main__':
    unittest.main()
