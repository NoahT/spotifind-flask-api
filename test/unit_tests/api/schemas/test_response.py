import unittest
import src.api.schemas.response as response
from http import HTTPStatus

class ResponseFactoryTestSuite(unittest.TestCase):
    def setUp(self) -> None:
        self._bad_request_response_builder = response.BadRequestResponseBuilder()
        self._not_found_response_builder = response.NotFoundResponseBuilder()
        self._ok_response_builder = response.OkResponseBuilder()
        self._response_builder_factory = response.ResponseBuilderFactory(
            self._bad_request_response_builder,
            self._not_found_response_builder,
            self._ok_response_builder
        )
    
    def test_should_return_bad_request_response_builder_on_400(self):
        response_builder = self._response_builder_factory.get_builder(HTTPStatus.BAD_REQUEST.value)

        self.assertIs(response_builder, self._bad_request_response_builder)
    
    def test_should_return_not_found_response_builder_on_404(self):
        response_builder = self._response_builder_factory.get_builder(HTTPStatus.NOT_FOUND.value)

        self.assertIs(response_builder, self._not_found_response_builder)
    
    def test_should_return_ok_response_builder_on_200(self):
        response_builder = self._response_builder_factory.get_builder(HTTPStatus.OK.value)

        self.assertIs(response_builder, self._ok_response_builder)
    
    def test_should_raise_error_when_unsupported_status_used(self):
        self.assertRaises(ValueError, self._response_builder_factory.get_builder, HTTPStatus.BAD_GATEWAY.value)

class ResponseBuilder4xxTestSuite(unittest.TestCase):
    def test_should_properly_build_400_response(self):
        bad_request_response = response.BadRequestResponseBuilder().build_response()
        response_400 = {
            "message": "Bad request.",
            "status": 400
        }

        self.assertEqual(bad_request_response, response_400)
    
    def test_should_properly_build_404_response(self):
        not_found_response = response.NotFoundResponseBuilder().build_response()
        response_404 = {
            "message": "Invalid track id.",
            "status": 404
        }

        self.assertEqual(not_found_response, response_404)
    
    def test_should_properly_build_200_response(self):
        ok_response = response.OkResponseBuilder().build_response()
        response_200 = {} # TODO

        self.assertEqual(ok_response, response_200)

        

if __name__ == '__main__':
    unittest.main()
