import unittest

from magicbox_distance import ureg
import magicbox_distance.shapefile_convert as shapefile_convert
import data_factory

from magicbox_distance.networkx_roads import START_KEY, END_KEY, DISTANCE_KEY


class TestShapeFileConvert(unittest.TestCase):
    start = data_factory.right_isosceles_triangle_start
    middle = data_factory.right_isosceles_triangle_middle
    end = data_factory.right_isosceles_triangle_end

    def test_simple_triangle(self):
        shapefile = data_factory.create_right_isosceles_triangle(self.start, self.middle, self.end)
        networkx = shapefile_convert.to_networkx_roads(shapefile)

        self.assertEqual(len(networkx), 1)
        self.assertEqual(networkx[0][START_KEY], self.start)
        self.assertEqual(networkx[0][END_KEY], self.end)
        self.assertTrue(abs(networkx[0][DISTANCE_KEY] - data_factory.right_isosceles_triangle_distance) < 1 * ureg.millimetre)


if __name__ == '__main__':
    unittest.main()
