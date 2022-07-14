import unittest

class SpotifyClientTestSuite(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()
    
    def test_should_return_200_response_for_valid_track_id(self) -> None:
        pass

    def test_should_return_200_response_for_valid_track_id_and_marketplace(self) -> None:
        pass

    def test_should_return_200_response_for_valid_track_id_and_missing_marketplace(self) -> None:
        pass

    def test_should_return_400_response_for_invalid_track_id(self) -> None:
        pass

    def test_should_return_401_response_for_invalid_bearer_token(self) -> None:
        pass
