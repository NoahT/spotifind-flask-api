import unittest
import src.api.schemas.response as response
from http import HTTPStatus

class ResponseFactoryTestSuite(unittest.TestCase):
    def setUp(self) -> None:
        self._bad_request_response_builder = response.BadRequestResponseBuilder()
        self._not_found_response_builder = response.NotFoundResponseBuilder()
        self._internal_server_error_builder = response.InternalServerErrorResponseBuilder()
        self._ok_response_builder = response.OkResponseBuilder()
        self._response_builder_factory = response.ResponseBuilderFactory(
            self._bad_request_response_builder,
            self._not_found_response_builder,
            self._internal_server_error_builder,
            self._ok_response_builder
        )
    
    def test_should_return_bad_request_response_builder_on_400(self):
        response_builder = self._response_builder_factory.get_builder(HTTPStatus.BAD_REQUEST.value)

        self.assertIs(response_builder, self._bad_request_response_builder)
    
    def test_should_return_not_found_response_builder_on_404(self):
        response_builder = self._response_builder_factory.get_builder(HTTPStatus.NOT_FOUND.value)

        self.assertIs(response_builder, self._not_found_response_builder)
    
    def test_should_return_not_found_response_builder_on_500(self):
        response_builder = self._response_builder_factory.get_builder(HTTPStatus.INTERNAL_SERVER_ERROR.value)

        self.assertIs(response_builder, self._internal_server_error_builder)
    
    def test_should_return_ok_response_builder_on_200(self):
        response_builder = self._response_builder_factory.get_builder(HTTPStatus.OK.value)

        self.assertIs(response_builder, self._ok_response_builder)
    
    def test_should_raise_error_when_unsupported_status_used(self):
        self.assertRaises(ValueError, self._response_builder_factory.get_builder, HTTPStatus.BAD_GATEWAY.value)

class ResponseBuilderTestSuite(unittest.TestCase):
    def test_should_properly_build_400_response(self):
        bad_request_response = response.BadRequestResponseBuilder().build_response(recos_response={}, id='123', size=5)
        response_400 = {
            "message": "Bad request.",
            "status": 400
        }

        self.assertEqual(response_400, bad_request_response.response)
        self.assertEqual(400, bad_request_response.response_code)
    
    def test_should_properly_build_404_response(self):
        not_found_response = response.NotFoundResponseBuilder().build_response(recos_response={}, id='123', size=5)
        response_404 = {
            "message": "Invalid track id: 123",
            "status": 404
        }

        self.assertEqual(response_404, not_found_response.response)
        self.assertEqual(404, not_found_response.response_code)
    
    def test_should_properly_build_500_response(self):
        internal_server_error_response = response.InternalServerErrorResponseBuilder().build_response(recos_response={}, id='123', size=5)
        response_500 = {
            'message': 'An unexpected error occurred. Please contact a contributor for assistance.',
            'status': 500
        }

        self.assertEqual(response_500, internal_server_error_response.response)
        self.assertEqual(500, internal_server_error_response.response_code)
    
    def test_should_properly_build_200_response(self):
        recos_dict = {
            "neighbor": [
                {
                    "id": "7C48cUjCGx14K5b41e9vTD",
                    "distance": 1.0
                },
                {
                    "id": "3x7gMvCsL1SS6THGwB55Pm",
                    "distance": 2.0
                },
                {
                    "id": "7sLQGgXFs4LaGAaDErPwOl",
                    "distance": 5.0
                }
            ]
        }
        expected_response = {
            "recos": [
                {
                    "id": "7C48cUjCGx14K5b41e9vTD"
                },
                {
                    "id": "3x7gMvCsL1SS6THGwB55Pm"
                }
            ],
            "request": {
                "size": 2,
                "track": {
                    "id": "123"
                }
            }
        }
        ok_response = response.OkResponseBuilder().build_response(recos_response=recos_dict, id='123', size=2)

        self.assertEqual(expected_response, ok_response.response)
        self.assertEqual(200, ok_response.response_code)
    
    def test_should_properly_build_200_response_with_input_as_neighbor(self):
        recos_dict = {
            "neighbor": [
                {
                    "id": "123",
                    "distance": 0.0
                },
                {
                    "id": "3x7gMvCsL1SS6THGwB55Pm",
                    "distance": 2.0
                },
                {
                    "id": "7sLQGgXFs4LaGAaDErPwOl",
                    "distance": 5.0
                }
            ]
        }
        expected_response = {
            "recos": [
                {
                    "id": "3x7gMvCsL1SS6THGwB55Pm"
                },
                {
                    "id": "7sLQGgXFs4LaGAaDErPwOl"
                }
            ],
            "request": {
                "size": 2,
                "track": {
                    "id": "123"
                }
            }
        }
        ok_response = response.OkResponseBuilder().build_response(recos_response=recos_dict, id='123', size=2)

        self.assertEqual(expected_response, ok_response.response)
        self.assertEqual(200, ok_response.response_code)

if __name__ == '__main__':
    unittest.main()
