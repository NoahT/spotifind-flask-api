import unittest
from src.api.app import flask_app

class RecosAPITestSuite(unittest.TestCase):
    def setUp(self) -> None:
        self.spotifind_client = flask_app.test_client()
    
    def test_should_return_200_response_for_valid_id(self) -> None:
        recos_response = self.spotifind_client.get('/v1/reco/3L4KeuZsCf5PHkXPvvvCQG')
        recos_response_json = recos_response.json

        self.assertIsNotNone(recos_response_json)
        
        recos = recos_response_json['recos']
        self.assertIsNotNone(recos)
        self.assertEqual(len(recos), 5)

        request = recos_response_json['request']
        self.assertIsNotNone(request)
        self.assertEqual(request,
        {
            'size': 5,
            'track': {
                'id': '3L4KeuZsCf5PHkXPvvvCQG'
            }
        })
        
    def test_should_return_200_response_for_valid_id_with_size(self) -> None:
        recos_response = self.spotifind_client.get('/v1/reco/3L4KeuZsCf5PHkXPvvvCQG?size=50')
        recos_response_json = recos_response.json

        self.assertIsNotNone(recos_response_json)

        recos = recos_response_json['recos']
        self.assertIsNotNone(recos)
        self.assertEqual(len(recos), 50)
        
        request = recos_response_json['request']
        self.assertIsNotNone(request)
        self.assertEqual(request,
        {
            'size': 50,
            'track': {
                'id': '3L4KeuZsCf5PHkXPvvvCQG'
            }
        })

    def test_should_return_400_response_for_invalid_size(self) -> None:
        recos_response = self.spotifind_client.get('/v1/reco/3L4KeuZsCf5PHkXPvvvCQG?size=-1')
        recos_response_json = recos_response.json

        self.assertIsNotNone(recos_response_json)
        self.assertEqual(recos_response_json,
        {
            "message": "Bad request.",
            "status": 400
        })

    def test_should_return_400_response_for_invalid_track(self) -> None:
        recos_response = self.spotifind_client.get('/v1/reco/invalid_resource')
        recos_response_json = recos_response.json

        self.assertIsNotNone(recos_response_json)
        self.assertEqual(recos_response_json,
        {
            "message": "Bad request.",
            "status": 400
        })
