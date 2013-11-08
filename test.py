import unittest
import main

class TestHowMainstream(unittest.TestCase):
    def test_emptyList(self):
        self.assertIsInstance(main.how_mainstream([]), str)
    def test_validArtist(self):
        singleProfile = [{'familiarity': 0.908821, 'hotttnesss': 0.804396, 'name': 'The Beatles', 'id': 'AR6XZ861187FB4CECD'}]
        self.assertIsInstance(main.how_mainstream(singleProfile), str)
    def test_validArtists(self):
        multipleProfiles = [{'familiarity': 0.908821, 'hotttnesss': 0.804396, 'name': 'The Beatles', 'id': 'AR6XZ861187FB4CECD'}, {'familiarity': 0.858889, 'hotttnesss': 0.797314, 'name': 'Pink Floyd', 'id': 'ARD4C1I1187FB4B0C3'}]
        self.assertIsInstance(main.how_mainstream(multipleProfiles), str)

if __name__ == '__main__':
    unittest.main()
