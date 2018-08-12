import unittest

from magicbox_distance import ureg
import magicbox_distance.distance as distance


class TestUsingLatitudeAndLongitude(unittest.TestCase):

    def test_zero_distance(self):
        calculated = distance.using_latitude_and_longitude((0, 0), (0, 0))
        self.assertEqual(calculated, 0 * ureg.kilometres)

    def test_christchurch_to_london_and_back(self):
        christchurch = (-43.5321, 172.6362)
        london = (51.5074, -0.1278)
        expected = 18976 * ureg.kilometres

        to_london = distance.using_latitude_and_longitude(christchurch, london)

        self.assertTrue(abs(to_london - expected) < 1 * ureg.kilometres)

        to_christchurch = distance.using_latitude_and_longitude(london, christchurch)
        self.assertTrue(abs(to_christchurch - expected) < 1 * ureg.kilometres)


if __name__ == '__main__':
    unittest.main()
