import unittest

import magicbox_distance.geojson as geojson


class TestLoadSchoolsExampleGeoJson(unittest.TestCase):

    def test_load(self):
        # schoolsUrl = "https://raw.githubusercontent.com/unicef/magicbox-maps-prototype/master/public/data/schools.json"
        schoolsUrl = "file:///Users/joachim/Downloads/schools.json"
        schools = geojson.load(schoolsUrl)
        self.assertEqual(len(schools["features"]), 67708)

if __name__ == '__main__':
    unittest.main()
