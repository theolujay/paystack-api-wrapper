import pytest
import requests
import responses

from api.exceptions import APIError

# === Test Helpers ===
def assert_api_error_contains(callable_method, expected_keyword, *args, **kwargs):
    """Helper to test that APIError is raised and contains expected keyword"""
    with pytest.raises(APIError) as excinfo:
        callable_method(*args, **kwargs)
    assert str(expected_keyword).lower() in str(excinfo.value).lower()

def setup_mock_response(transaction_client, reference, response_data=None, status_code=200):
    """Helper to set up a mock GET response for transaction verification"""
    if response_data is None:
        response_data = {
            "status": True,
            "message": "Success",
            "data": {"reference": reference},
        }

    responses.add(
        responses.GET,
        f"{transaction_client.base_url}/transaction/verify/{reference}",
        json=response_data,
        status=status_code,
    )

@responses.activate
def test_verify_transaction(transaction_client):
    reference = "adhvousgtsnsl"
    mock_response = {
        "status": True,
        "message": "Verification successful",
        "data": {
            "reference": reference,
            "status": "success",
            "amount": 40333,
            "gateway_response": "Successful",
        }
    }
    setup_mock_response(transaction_client, reference, mock_response)

    response = transaction_client.verify(reference)

    assert response["reference"] == reference
    assert response["status"] == "success"

@responses.activate
def test_verify_transaction_invalid_key(transaction_client):
    reference = "adhvousgtsnsl"
    mock_response = {"status": False, "message": "Invalid API key"}
    setup_mock_response(transaction_client, reference, mock_response, status_code=401)

    assert_api_error_contains(
        transaction_client.verify, "unauthorized", reference
    )

@responses.activate
def test_verify_transaction_timeout(transaction_client):
    reference = "adhvousgtsnsl"
    responses.add(
        responses.GET,
        f"{transaction_client.base_url}/transaction/verify/{reference}",
        body=requests.exceptions.Timeout(),
    )

    assert_api_error_contains(
        transaction_client.verify, "timed out", reference
    )

@responses.activate
def test_verify_transaction_malformed_json(transaction_client):
    reference = "adhvousgtsnsl"
    responses.add(
        responses.GET,
        f"{transaction_client.base_url}/transaction/verify/{reference}",
        body="Not a JSON",
        status=200,
    )

    assert_api_error_contains(
        transaction_client.verify, "invalid json response", reference
    )
