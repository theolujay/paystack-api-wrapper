import pytest
import requests
import responses
from api.core import PaystackResponse
from api.exceptions import APIError

# === Test Helpers ===
def assert_api_error_contains(callable_method, expected_keyword, *args, **kwargs):
    with pytest.raises(APIError) as excinfo:
        callable_method(*args, **kwargs)
    assert str(expected_keyword).lower() in str(excinfo.value).lower()

def setup_mock_response(transaction_client, transaction_id, response_data=None, status_code=200):
    if response_data is None:
        response_data = {
            "status": True,
            "message": "Transaction retrieved",
            "data": {
                "id": transaction_id,
                "reference": "ps_ref_12345",
                "amount": 500000,
                "status": "success",
                "paid_at": "2025-08-01T09:45:00Z",
                "customer": {
                    "email": "customer@example.com"
                }
            }
        }

    responses.add(
        responses.GET,
        f"{transaction_client.base_url}/transaction/{transaction_id}",
        json=response_data,
        status=status_code,
    )

@responses.activate
def test_fetch_transaction(transaction_client):
    transaction_id = 102934
    setup_mock_response(transaction_client, transaction_id)
    
    response = transaction_client.fetch(transaction_id)
    
    assert isinstance(response, PaystackResponse)
    assert response.data["id"] == transaction_id
    assert response.data["reference"] == "ps_ref_12345"

@responses.activate
def test_fetch_transaction_invalid_key(transaction_client):
    transaction_id = 102934
    mock_response = {"status": False, "message": "Invalid API key"}
    setup_mock_response(transaction_client, transaction_id, mock_response, status_code=401)
    assert_api_error_contains(transaction_client.fetch, "invalid api key", transaction_id)

@responses.activate
def test_fetch_transaction_timeout(transaction_client):
    transaction_id = 102934
    responses.add(
        responses.GET,
        f"{transaction_client.base_url}/transaction/{transaction_id}",
        body=requests.exceptions.Timeout(),
    )
    assert_api_error_contains(transaction_client.fetch, "timed out", transaction_id)

@responses.activate
def test_fetch_transaction_malformed_json(transaction_client):
    transaction_id = 102934
    responses.add(
        responses.GET,
        f"{transaction_client.base_url}/transaction/{transaction_id}",
        body="Not a JSON",
        status=200,
    )
    assert_api_error_contains(transaction_client.fetch, "invalid json response", transaction_id)
