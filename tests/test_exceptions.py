import pytest
import json
from unittest.mock import Mock

from api.exceptions import (
    PaystackError,
    APIError,
    AuthenticationError,
    ValidationError,
    NotFoundError,
    RateLimitError,
    ServerError,
    NetworkError,
    InvalidResponseError,
    TransactionFailureError,
    create_error_from_response,
)


class TestPaystackError:
    def test_initialization(self):
        error = PaystackError("Test message", 400, {"status": "error"}, "req_123")
        assert error.message == "Test message"
        assert error.status_code == 400
        assert error.response == {"status": "error"}
        assert error.request_id == "req_123"

    def test_str_representation(self):
        error = PaystackError("Test message", 400, request_id="req_123")
        assert str(error) == "PaystackError - HTTP 400 - Request ID: req_123 - Test message"

        error_no_id = PaystackError("Test message")
        assert str(error_no_id) == "PaystackError - Test message"

    def test_repr_representation(self):
        error = PaystackError("Test message", 400, request_id="req_123")
        assert repr(error) == "PaystackError(message='Test message', status_code=400, request_id='req_123')"


class TestSpecificExceptions:
    def test_api_error_inheritance(self):
        assert issubclass(APIError, PaystackError)
        err = APIError("API issue")
        assert err.message == "API issue"

    def test_authentication_error_inheritance(self):
        assert issubclass(AuthenticationError, PaystackError)
        err = AuthenticationError("Auth failed")
        assert err.message == "Auth failed"

    def test_not_found_error_inheritance(self):
        assert issubclass(NotFoundError, PaystackError)
        err = NotFoundError("Resource not found")
        assert err.message == "Resource not found"

    def test_server_error_inheritance(self):
        assert issubclass(ServerError, PaystackError)
        err = ServerError("Server down")
        assert err.message == "Server down"

    def test_network_error_inheritance(self):
        assert issubclass(NetworkError, PaystackError)
        err = NetworkError("No internet")
        assert err.message == "No internet"

    def test_invalid_response_error_inheritance(self):
        assert issubclass(InvalidResponseError, PaystackError)
        err = InvalidResponseError("Bad JSON")
        assert err.message == "Bad JSON"


class TestValidationError:
    def test_initialization(self):
        field_errors = {"email": "Invalid format", "amount": "Too low"}
        error = ValidationError("Validation failed", field_errors=field_errors)
        assert error.message == "Validation failed"
        assert error.field_errors == field_errors

    def test_str_representation_with_field_errors(self):
        field_errors = {"email": "Invalid format"}
        error = ValidationError("Validation failed", field_errors=field_errors)
        assert (
            str(error)
            == "PaystackError - Validation failed | Field errors: email: Invalid format"
        )

    def test_str_representation_without_field_errors(self):
        error = ValidationError("Validation failed")
        assert str(error) == "PaystackError - Validation failed"


class TestRateLimitError:
    def test_initialization(self):
        error = RateLimitError("Rate limit exceeded", retry_after=60)
        assert error.message == "Rate limit exceeded"
        assert error.retry_after == 60

    def test_str_representation_with_retry_after(self):
        error = RateLimitError("Rate limit exceeded", retry_after=60)
        assert (
            str(error)
            == "PaystackError - Rate limit exceeded | Retry after: 60 seconds"
        )

    def test_str_representation_without_retry_after(self):
        error = RateLimitError("Rate limit exceeded")
        assert str(error) == "PaystackError - Rate limit exceeded"


class TestTransactionFailureError:
    def test_initialization(self):
        error = TransactionFailureError("Transaction failed", gateway_response="Declined")
        assert error.message == "Transaction failed"
        assert error.gateway_response == "Declined"

    def test_str_representation_with_gateway_response(self):
        error = TransactionFailureError("Transaction failed", gateway_response="Declined")
        assert (
            str(error)
            == "PaystackError - Transaction failed | Gateway response: Declined"
        )

    def test_str_representation_without_gateway_response(self):
        error = TransactionFailureError("Transaction failed")
        assert str(error) == "PaystackError - Transaction failed"


class TestCreateErrorFromResponse:
    def test_400_validation_error(self):
        response_data = {"status": False, "message": "Invalid data", "errors": {"name": "required"}}
        error = create_error_from_response(response_data, 400)
        assert isinstance(error, ValidationError)
        assert error.message == "Invalid data"
        assert error.field_errors == {"name": "required"}

    def test_401_authentication_error(self):
        response_data = {"status": False, "message": "Invalid API key"}
        error = create_error_from_response(response_data, 401)
        assert isinstance(error, AuthenticationError)
        assert error.message == "Invalid API key"

    def test_404_not_found_error(self):
        response_data = {"status": False, "message": "Resource not found"}
        error = create_error_from_response(response_data, 404)
        assert isinstance(error, NotFoundError)
        assert error.message == "Resource not found"

    def test_429_rate_limit_error(self):
        mock_response = Mock()
        mock_response.json.return_value = {"status": False, "message": "Too many requests"}
        mock_response.headers = {"Retry-After": "120"}
        error = create_error_from_response(mock_response, 429)
        assert isinstance(error, RateLimitError)
        assert error.message == "Too many requests"
        assert error.retry_after == 120

    def test_500_server_error(self):
        response_data = {"status": False, "message": "Internal server error"}
        error = create_error_from_response(response_data, 500)
        assert isinstance(error, ServerError)
        assert error.message == "Internal server error"

    def test_other_api_error(self):
        response_data = {"status": False, "message": "Unknown error"}
        error = create_error_from_response(response_data, 403)
        assert isinstance(error, APIError)
        assert error.message == "Unknown error"

    def test_transaction_failure_error_200_false_status(self):
        # This scenario is handled by the client, not create_error_from_response directly
        # create_error_from_response will return an APIError for 200 status
        # The client code then checks the 'status' field in the response data
        response_data = {"status": False, "message": "Transaction failed", "data": {"gateway_response": "Declined"}}
        error = create_error_from_response(response_data, 200)
        assert isinstance(error, APIError) # It's an APIError from this function's perspective
        assert error.message == "Transaction failed"

    def test_response_without_json_method(self):
        response_data = {"message": "Plain dict response"}
        error = create_error_from_response(response_data, 400)
        assert isinstance(error, ValidationError)
        assert error.message == "Plain dict response"

    def test_invalid_json_response(self):
        mock_response = Mock()
        mock_response.json.side_effect = json.JSONDecodeError("Expecting value", "doc", 0)
        mock_response.headers = {}
        error = create_error_from_response(mock_response, 400)
        assert isinstance(error, ValidationError)
        assert "HTTP 400 error" in error.message

    def test_rate_limit_error_no_retry_after_header(self):
        mock_response = Mock()
        mock_response.json.return_value = {"status": False, "message": "Too many requests"}
        mock_response.headers = {} # No Retry-After header
        error = create_error_from_response(mock_response, 429)
        assert isinstance(error, RateLimitError)
        assert error.message == "Too many requests"
        assert error.retry_after is None

    def test_rate_limit_error_invalid_retry_after_header(self):
        mock_response = Mock()
        mock_response.json.return_value = {"status": False, "message": "Too many requests"}
        mock_response.headers = {"Retry-After": "abc"} # Invalid Retry-After header
        error = create_error_from_response(mock_response, 429)
        assert isinstance(error, RateLimitError)
        assert error.message == "Too many requests"
        assert error.retry_after is None
