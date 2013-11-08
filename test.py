import unittest
import main

class TestFormatArtistProfiles(unittest.TestCase):
    def test_no_artists(self):
        self.assertEqual(main.format_artist_profiles([]), [])
    def test_valid_artist(self):
        valid_artist_response = [{'response': {'status': {'code': 0, 'message': 'Success', 'version': '4.2'}, 'artist': {'familiarity': 0.908821, 'hotttnesss': 0.804396, 'name': 'The Beatles', 'id': 'AR6XZ861187FB4CECD'}}}]
        self.assertEqual(main.format_artist_profiles(valid_artist_response), [{'familiarity': 0.908821, 'hotttnesss': 0.804396, 'name': 'The Beatles', 'id': 'AR6XZ861187FB4CECD'}])

class TestHowMainstream(unittest.TestCase):
    def test_empty_list(self):
        self.assertIsInstance(main.how_mainstream([]), str)
    def test_valid_artist(self):
        singleProfile = [{'familiarity': 0.908821, 'hotttnesss': 0.804396, 'name': 'The Beatles', 'id': 'AR6XZ861187FB4CECD'}]
        self.assertIsInstance(main.how_mainstream(singleProfile), str)
    def test_valid_artists(self):
        multipleProfiles = [{'familiarity': 0.908821, 'hotttnesss': 0.804396, 'name': 'The Beatles', 'id': 'AR6XZ861187FB4CECD'}, {'familiarity': 0.858889, 'hotttnesss': 0.797314, 'name': 'Pink Floyd', 'id': 'ARD4C1I1187FB4B0C3'}]
        self.assertIsInstance(main.how_mainstream(multipleProfiles), str)

if __name__ == '__main__':
    unittest.main()
