import unittest

from magicbox_distance import distance


class TestUsingLatitudeAndLongitude(unittest.TestCase):

    def test_zero_distance(self):
        calculated = distance.using_latitude_and_longitude((0, 0), (0, 0))
        self.assertEqual(calculated, 0)

    def test_christchurch_to_london_and_back(self):
        christchurch = (-43.5321, 172.6362)
        london = (51.5074, -0.1278)
        calculated = distance.using_latitude_and_longitude(christchurch, london)
        self.assertAlmostEqual(calculated, 18976, places=0)
        calculated = distance.using_latitude_and_longitude(london, christchurch)
        self.assertAlmostEqual(calculated, 18976, places=0)


if __name__ == '__main__':
    unittest.main()
