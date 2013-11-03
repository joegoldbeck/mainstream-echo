import unittest
import index
from tornado.escape import json_decode

class TestExtractProfileId(unittest.TestCase):
    def runTest(self):
        test_body = '{"response": {"status": {"version": "4.2", "code": 0, "message": "Success"}, "type": "artist", "name": "test_artist_catalog", "id": "CATIYPU1421AC496FC"}}'
        self.assertEqual(index.extract_profile_id(test_body), 'CATIYPU1421AC496FC')


if __name__ == '__main__':
    unittest.main()
