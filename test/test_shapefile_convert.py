import unittest

import magicbox_distance.shapefile_convert as shapefile_convert
import data_factory

kms_to_millimetre_accuracy_decimal_places = 6


class TestShapeFileConvert(unittest.TestCase):
    start = data_factory.right_isosceles_triangle_start
    middle = data_factory.right_isosceles_triangle_middle
    end = data_factory.right_isosceles_triangle_end

    start_tuple = shapefile_convert.to_tuple(start)
    middle_tuple = shapefile_convert.to_tuple(middle)
    end_tuple = shapefile_convert.to_tuple(end)

    def test_simple_triangle(self):
        shapefile = data_factory.create_right_isosceles_triangle(self.start, self.middle, self.end)
        networkx = shapefile_convert.to_networkx_roads(shapefile)

        self.assertEqual(len(networkx), 1)
        self.assertEqual(networkx[0][0], self.start_tuple)
        self.assertEqual(networkx[0][1], self.end_tuple)
        self.assertAlmostEqual(networkx[0][2], data_factory.right_isosceles_triangle_distance,
                               kms_to_millimetre_accuracy_decimal_places)


if __name__ == '__main__':
    unittest.main()
