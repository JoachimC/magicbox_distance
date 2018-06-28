import unittest
from magicbox_distance import distance


class TestUsingLatitudeAndLongitude(unittest.TestCase):

    def test_zero_distance(self):
        calculated = distance.using_latitude_and_longitude(0, 0)
        self.assertEqual(calculated, 0)

if __name__ == '__main__':
    unittest.main()
