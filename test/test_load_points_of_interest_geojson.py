import unittest

from magicbox_distance import geojson

class TestLoadSchoolsExampleGeoJson(unittest.TestCase):

    def test_load(self):
        schoolsUrl = "https://raw.githubusercontent.com/unicef/magicbox-maps-prototype/master/public/data/schools.json"
        schools = geojson.load(schoolsUrl)
        self.assertEqual(len(schools["features"]), 67708)

if __name__ == '__main__':
    unittest.main()
