import unittest

from magicbox_distance import ureg

import data_factory
import magicbox_distance.distance as distance
import magicbox_distance.shapefile_convert as shapefile_convert


class TestUsingRoads(unittest.TestCase):

    def test_zero_distance(self):
        actual_distance = distance.using_roads([],
                                               data_factory.right_isosceles_triangle_start,
                                               data_factory.right_isosceles_triangle_start)
        self.assertEqual(actual_distance, 0 * ureg.kilometre)

    def test_simple_triangle(self):
        shapefile = data_factory.create_right_isosceles_triangle(data_factory.right_isosceles_triangle_start,
                                                                 data_factory.right_isosceles_triangle_middle,
                                                                 data_factory.right_isosceles_triangle_end)
        networkx = shapefile_convert.to_networkx_roads(shapefile)
        actual_distance = distance.using_roads(networkx, data_factory.right_isosceles_triangle_start,
                                               data_factory.right_isosceles_triangle_end)

        self.assertEqual(actual_distance, data_factory.right_isosceles_triangle_distance)


if __name__ == '__main__':
    unittest.main()
