import pytest
import responses
from requests.exceptions import Timeout

from paystack_client import (
    APIError,
    NetworkError,
    InvalidResponseError,
    ValidationError,
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


@responses.activate
def test_request_timeout(base_client):

    def request_callback(request):
        raise Timeout("Connection timed out")

    responses.add_callback(
        responses.GET,
        f"{base_client.base_url}/test",
        callback=request_callback,
        content_type="application/json",
    )

    with pytest.raises(NetworkError) as excinfo:
        base_client.request("GET", "test")

    assert "Connection timed out" in str(excinfo.value)


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
    )
    with pytest.raises(InvalidResponseError) as excinfo:
        base_client.request("GET", "test")
    assert "Invalid JSON response" in str(excinfo.value)
