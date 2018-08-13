import unittest

from geopy import Point

from magicbox_distance import ureg

import test.unit.data_factory as data_factory
import magicbox_distance.distance as distance
import magicbox_distance.shapefile_convert as shapefile_convert


class TestUsingRoads(unittest.TestCase):

    def test_zero_distance(self):
        actual_distance = distance.using_roads([], data_factory.right_angle_start, data_factory.right_angle_start)
        self.assertEqual(actual_distance, 0 * ureg.kilometre)

    def test_simple_triangle(self):
        right_angled_road = data_factory.create_part(data_factory.right_angle_start,
                                                     data_factory.right_angle_middle,
                                                     data_factory.right_angle_end)
        shapefile = data_factory.create_shapefile([right_angled_road])

        networkx = shapefile_convert.to_networkx_roads(shapefile)
        actual_distance = distance.using_roads(networkx, data_factory.right_angle_start, data_factory.right_angle_end)

        self.assertEqual(actual_distance, data_factory.right_angle_distance)

    def test_two_edge_path(self):
        first_start = data_factory.right_angle_start
        first_middle = data_factory.right_angle_middle
        first_end = data_factory.right_angle_end
        first_right_angled_road = data_factory.create_part(first_start, first_middle, first_end)

        second_start = first_end
        second_middle = Point('%.1f' % (first_end.latitude + 0.1), first_end.longitude)
        second_end = Point('%.1f' % (first_end.latitude + 0.1), '%.1f' % (first_end.longitude + 0.1))
        second_right_angled_road = data_factory.create_part(second_start, second_middle, second_end)

        shapefile = data_factory.create_shapefile([first_right_angled_road] + [second_right_angled_road])

        networkx = shapefile_convert.to_networkx_roads(shapefile)
        actual_distance = distance.using_roads(networkx, first_start, second_end)

        self.assertTrue(abs(actual_distance - (data_factory.right_angle_distance * 2)) < 1 * ureg.metre)

    def test_two_path_options(self):
        start = data_factory.right_angle_start
        end = data_factory.right_angle_end
        expected_distance = distance.using_latitude_and_longitude(start, end)

        roads = self.create_three_edge_short_road(start, end) + self.create_two_edge_long_road(start, end)
        shapefile = data_factory.create_shapefile(roads)

        networkx = shapefile_convert.to_networkx_roads(shapefile)
        actual_distance = distance.using_roads(networkx, start, end)

        self.assertTrue(abs(actual_distance - expected_distance) < 1 * ureg.metre)

    def create_three_edge_short_road(self, start, end):
        first_start = start
        first_end = Point('%.3f' % (((end.latitude - start.latitude) * 0.2) + start.latitude),
                          '%.3f' % (((end.longitude - start.longitude) * 0.2) + start.longitude))
        first_road = data_factory.create_part(first_start, first_end)

        second_start = first_end
        second_end = Point('%.3f' % (((end.latitude - start.latitude) * 0.8) + start.latitude),
                           '%.3f' % (((end.longitude - start.longitude) * 0.8) + start.longitude))
        second_road = data_factory.create_part(second_start, second_end)

        third_start = second_end
        third_end = end
        third_road = data_factory.create_part(third_start, third_end)

        return [first_road, second_road, third_road]

    def create_two_edge_long_road(self, start, end):
        first_start = start
        first_end = Point('%.1f' % (first_start.latitude + 45), '%.1f' % (first_start.longitude + 45))
        first_road = data_factory.create_part(first_start, first_end)

        second_start = first_end
        second_end = end
        second_road = data_factory.create_part(second_start, second_end)

        return [first_road, second_road]

    def test_there_and_back(self):
        self.assertTrue(False, "not implemented")

if __name__ == '__main__':
    unittest.main()
