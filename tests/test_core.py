import pytest
import responses
from requests.exceptions import Timeout, ConnectTimeout, ReadTimeout

from paystack_client import (
    APIError,
    NetworkError,
    InvalidResponseError,
    ValidationError,
    AuthenticationError,
    TransactionFailureError,
)


@responses.activate
def test_baseclient_sets_authorization_header(base_client, secret_key):

    responses.add(
        responses.GET,
        f"{base_client.base_url}/test",
        json={"status": True, "message": "ok", "data": {"x": 1}},
        status=200,
    )
    data, meta = base_client.request("GET", "test")
    assert responses.calls[0].request.headers["Authorization"] == f"Bearer {secret_key}"
    assert data == {"x": 1}


def test_baseclient_removes_authorization_header_for_private_false(base_client, mocker):
    mock_request = mocker.patch.object(base_client.session, 'request')
    mock_request.return_value = mocker.Mock(
        status_code=200,
        json=lambda: {"status": True, "message": "ok", "data": {"x": 1}},
        headers={"x-amzn-requestid": "test-request-id"}
    )

    data, meta = base_client.request("GET", "test", private=False)

    # Assert that the 'Authorization' header was removed before the request was sent
    called_headers = mock_request.call_args[1]['headers']
    assert "Authorization" not in called_headers
    assert data == {"x": 1}

def test_baseclient_repr_with_empty_secret_key():
    from paystack_client.core import BaseClient
    client = BaseClient(secret_key="sk_test_12345") # Initialize with a valid key
    client.secret_key = "" # Then set it to empty for repr test
    assert repr(client) == "BaseClient(secret_key=None, base_url='https://api.paystack.co/')"

def test_baseclient_repr_with_none_secret_key():
    from paystack_client.core import BaseClient
    client = BaseClient(secret_key="sk_test_12345") # Initialize with a valid key
    client.secret_key = None # Then set it to None for repr test
    assert repr(client) == "BaseClient(secret_key=None, base_url='https://api.paystack.co/')"



@responses.activate
def test_baseclient_sets_idempotency_key(base_client):
    idempotency_key = "test_idempotency_key"
    responses.add(
        responses.POST,
        f"{base_client.base_url}/test",
        json={"status": True, "message": "ok", "data": {"x": 1}},
        status=200,
    )
    data, meta = base_client.request("POST", "test", idempotency_key=idempotency_key)
    assert responses.calls[0].request.headers["Idempotency-Key"] == idempotency_key
    assert data == {"x": 1}


@responses.activate
def test_request_connect_timeout(base_client):

    def request_callback(request):
        raise ConnectTimeout("Connection timed out")

    responses.add_callback(
        responses.GET,
        f"{base_client.base_url}/test",
        callback=request_callback,
        content_type="application/json",
    )

    with pytest.raises(NetworkError, match="Connection timed out"):
        base_client.request("GET", "test")


@responses.activate
def test_request_read_timeout(base_client):

    def request_callback(request):
        raise ReadTimeout("Request timed out")

    responses.add_callback(
        responses.GET,
        f"{base_client.base_url}/test",
        callback=request_callback,
        content_type="application/json",
    )

    with pytest.raises(NetworkError, match=f"Request timed out after {base_client.timeout} seconds"):
        base_client.request("GET", "test")


@responses.activate
def test_false_status_response(base_client):

    responses.add(
        responses.POST,
        f"{base_client.base_url}/initiate_payment",
        json={
            "status": False,
            "message": "API error",
        },
        status=200,
    )
    with pytest.raises(APIError) as excinfo:
        base_client.request("POST", "initiate_payment")
    assert "API request failed: API error" in str(excinfo.value)


@responses.activate
def test_invalid_response_structure(base_client):

    responses.add(
        responses.POST,
        f"{base_client.base_url}/initiate_payment",
        json={
            "detail": "Invalid JSON response",
        },
        status=200,
    )
    with pytest.raises(InvalidResponseError) as excinfo:
        base_client.request("POST", "initiate_payment")
    assert "Invalid Paystack response structure: missing 'status' or 'message'" in str(
        excinfo.value
    )


@responses.activate
def test_invalid_response_not_dict(base_client):
    responses.add(
        responses.GET,
        f"{base_client.base_url}/test",
        json=["not", "a", "dict"],
        status=200,
    )
    with pytest.raises(InvalidResponseError, match="Expected JSON object, got <class 'list'>"):
        base_client.request("GET", "test")


@responses.activate
def test_error_status_code(base_client):

    responses.add(
        responses.POST,
        f"{base_client.base_url}/initiate_payment",
        json={
            "status": False,
            "message": "API error",
        },
        status=400,
    )
    with pytest.raises(ValidationError) as excinfo:
        base_client.request("POST", "initiate_payment")
    assert "API error" in str(excinfo.value)


@responses.activate
def test_invalid_json(base_client):

    responses.add(
        responses.GET,
        f"{base_client.base_url}/test",
        body="not json",
        status=200,
        content_type="application/json",
        headers={
            "x-amzn-requestid": "test-request-id"
        }
    )
    with pytest.raises(InvalidResponseError) as excinfo:
        base_client.request("GET", "test")
    assert "Invalid JSON response" in str(excinfo.value)
    assert excinfo.value.request_id == "test-request-id"


def test_baseclient_invalid_secret_key_format():
    from paystack_client.core import BaseClient
    with pytest.raises(AuthenticationError, match="Invalid paystack secret key format. Key should start with 'sk_test_' or 'sk_live_'"):
        BaseClient(secret_key="invalid_key")


@responses.activate
def test_handle_success_response_transaction_failed(base_client):
    responses.add(
        responses.GET,
        f"{base_client.base_url}/test",
        json={
            "status": True,
            "message": "Transaction status",
            "data": {"status": "failed", "gateway_response": "Insufficient funds"},
        },
        status=200,
    )
    with pytest.raises(TransactionFailureError, match="Transaction failed: failed"):
        base_client.request("GET", "test")


@responses.activate
def test_handle_success_response_transaction_abandoned(base_client):
    responses.add(
        responses.GET,
        f"{base_client.base_url}/test",
        json={
            "status": True,
            "message": "Transaction status",
            "data": {"status": "abandoned", "gateway_response": "User closed page"},
        },
        status=200,
    )
    with pytest.raises(TransactionFailureError, match="Transaction failed: abandoned"):
        base_client.request("GET", "test")


@responses.activate
def test_handle_success_response_transaction_cancelled(base_client):
    responses.add(
        responses.GET,
        f"{base_client.base_url}/test",
        json={
            "status": True,
            "message": "Transaction status",
            "data": {"status": "cancelled", "gateway_response": "User cancelled"},
        },
        status=200,
    )
    with pytest.raises(TransactionFailureError, match="Transaction failed: cancelled"):
        base_client.request("GET", "test")


@responses.activate
def test_handle_success_response_missing_status_or_message(base_client):
    responses.add(
        responses.GET,
        f"{base_client.base_url}/test",
        json={
            "data": {"status": "success"},
        },
        status=200,
    )
    with pytest.raises(InvalidResponseError, match="Invalid Paystack response structure: missing 'status' or 'message'"):
        base_client.request("GET", "test")


@responses.activate
def test_validate_required_params_positional_arguments(base_client):
    with pytest.raises(TypeError, match="Positional arguments are not allowed for this method."):
        base_client._validate_required_params("arg1", param="value")


@responses.activate
def test_validate_amount_invalid_type(base_client):
    responses.add(
        responses.GET,
        f"{base_client.base_url}/test",
        json={"status": True, "message": "ok", "data": {"x": 1}},
        status=200,
    )
    with pytest.raises(ValidationError, match="Amount must be a valid integer or string representation of an integer"):
        base_client._validate_amount(amount="abc")


@responses.activate
def test_validate_amount_too_small(base_client):
    responses.add(
        responses.GET,
        f"{base_client.base_url}/test",
        json={"status": True, "message": "ok", "data": {"x": 1}},
        status=200,
    )
    with pytest.raises(ValidationError, match="Amount too small for NGN"):
        base_client._validate_amount(amount=50, currency="NGN")


@responses.activate
def test_validate_email_invalid_format(base_client):
    responses.add(
        responses.GET,
        f"{base_client.base_url}/test",
        json={"status": True, "message": "ok", "data": {"x": 1}},
        status=200,
    )
    with pytest.raises(ValidationError, match="Invalid email format"):
        base_client._validate_email(email="invalid-email")


@responses.activate
def test_validate_email_missing(base_client):
    responses.add(
        responses.GET,
        f"{base_client.base_url}/test",
        json={"status": True, "message": "ok", "data": {"x": 1}},
        status=200,
    )
    with pytest.raises(ValidationError, match="Email is required"):
        base_client._validate_email(email="")


@responses.activate
def test_validate_email_too_long(base_client):
    responses.add(
        responses.GET,
        f"{base_client.base_url}/test",
        json={"status": True, "message": "ok", "data": {"x": 1}},
        status=200,
    )
    with pytest.raises(ValidationError, match="Email is required"):
        base_client._validate_email(email="a" * 255 + "@example.com")


@responses.activate
def test_request_with_request_id_headers(base_client):
    responses.add(
        responses.GET,
        f"{base_client.base_url}/test",
        json={"status": True, "message": "ok", "data": {"x": 1}},
        status=200,
        headers={
            "x-amzn-requestid": "test-amzn-request-id",
            "cf-ray": "test-cf-ray",
        },
    )
    data, meta = base_client.request("GET", "test")
    assert data == {"x": 1}
    assert meta == {}


@responses.activate
def test_handle_success_response_with_field_errors(base_client):
    responses.add(
        responses.POST,
        f"{base_client.base_url}/initiate_payment",
        json={
            "status": False,
            "message": "Validation failed",
            "errors": {"email": "Invalid email address"},
        },
        status=200,
    )
    with pytest.raises(ValidationError) as excinfo:
        base_client.request("POST", "initiate_payment")
    assert "Validation failed" in str(excinfo.value)
    assert excinfo.value.field_errors == {"email": "Invalid email address"}


@responses.activate
def test_validate_required_params_missing_values(base_client):
    with pytest.raises(ValidationError) as excinfo:
        base_client._validate_required_params(param1="", param2=None, param3="  ")
    assert "Missing required parameters: param1, param2, param3" in str(excinfo.value)
    assert excinfo.value.field_errors == {
        "param1": "This field is required",
        "param2": "This field is required",
        "param3": "This field is required",
    }


@responses.activate
def test_request_invalid_json_response(base_client):
    responses.add(
        responses.GET,
        f"{base_client.base_url}/test",
        body="this is not json",
        status=200,
        headers={"x-amzn-requestid": "test-request-id"},
    )
    with pytest.raises(InvalidResponseError) as excinfo:
        base_client.request("GET", "test")
    assert "Invalid JSON response" in str(excinfo.value)
    assert excinfo.value.request_id == "test-request-id"


@responses.activate
def test_handle_success_response_paystack_error_with_field_errors(base_client):
    responses.add(
        responses.POST,
        f"{base_client.base_url}/initiate_payment",
        json={
            "status": False,
            "message": "Validation failed",
            "errors": {"email": "Invalid email address"},
        },
        status=200,
    )
    with pytest.raises(ValidationError) as excinfo:
        base_client.request("POST", "initiate_payment")
    assert "Validation failed" in str(excinfo.value)
    assert excinfo.value.field_errors == {"email": "Invalid email address"}
