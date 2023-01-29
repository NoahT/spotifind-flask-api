import unittest
from unittest.mock import patch, Mock
from http import HTTPStatus
from requests import HTTPError as ClientHTTPError
import src.api.schemas.response as response
import src.api.util.reco.reco_controller as reco_controller

class V1RecoControllerTestSuite(unittest.TestCase):
    @patch('src.api.schemas.response.ResponseBuilderFactory')
    @patch('src.api.util.reco.reco_adapter.V1RecoAdapter')
    def setUp(self, reco_adapter, response_builder_factory) -> None:
        bad_request_response_builder = Mock(response.BadRequestResponseBuilder)
        bad_request_response_builder.build_response.return_value = response.Response(None, 400)
        not_found_response_builder = Mock(response.NotFoundResponseBuilder)
        not_found_response_builder.build_response.return_value = response.Response(None, 404)
        self.bad_request_response_builder = bad_request_response_builder
        self.not_found_response_builder = not_found_response_builder
        def response_builder_factory_side_effect(**kwargs):
            response_builder = None
            status_code = kwargs['status_code']
            if status_code == HTTPStatus.NOT_FOUND.value:
                response_builder = not_found_response_builder
            else:
                response_builder = bad_request_response_builder
            
            return response_builder
        
        response_builder_factory.get_builder.side_effect = response_builder_factory_side_effect
        self._v1_reco_controller = reco_controller.V1RecoController(reco_adapter, response_builder_factory)
    
    def test_should_return_400_response_on_invalid_client_request(self) -> None:
        def side_effect(id, size):
            mock_response = Mock()
            mock_response.status_code = 400
            raise ClientHTTPError(response=mock_response)
        
        self._v1_reco_controller._reco_adapter.get_recos.side_effect = side_effect
        reco_response = self._v1_reco_controller.get_recos('invalid', '5')
        self.assertEqual(400, reco_response.response_code)
    
    def test_should_return_200_response_on_valid_client_request(self) -> None:
        mock_response = response.Response(
            {
                'request': {
                    'track': {
                        'id': 'track_id'
                    },
                    'size': 5
                },
                'recos': [
                    {
                        'id': 'reco1'
                    },
                    {
                        'id': 'reco2'
                    },
                    {
                        'id': 'reco3'
                    },
                ]
            },
            200
        )
        self._v1_reco_controller._reco_adapter.get_recos.return_value = mock_response
        
        reco_response = self._v1_reco_controller.get_recos('track_id', '5')

        self.assertEqual(mock_response.response_code, reco_response.response_code)
        self.assertEqual(mock_response.response, reco_response.response)

