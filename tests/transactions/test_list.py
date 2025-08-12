import pytest
import requests
import responses
from api.exceptions import APIError

# === Test Helpers ===
def assert_api_error_contains(callable_method, expected_keyword, *args, **kwargs):
    with pytest.raises(APIError) as excinfo:
        callable_method(*args, **kwargs)
    assert str(expected_keyword).lower() in str(excinfo.value).lower()

def setup_mock_response(transaction_client, response_data=None, status_code=200):
    if response_data is None:
        response_data = {
            "status": True,
            "message": "Transactions retrieved",
            "data": [
                {
                    "id": 102934,
                    "reference": "ps_ref_12345",
                    "amount": 500000,
                    "status": "success",
                    "paid_at": "2025-08-01T09:45:00Z",
                    "customer": {
                        "email": "customer@example.com"
                    }
                }
            ],
            "meta": {
                "total": 50,
                "page": 1,
                "perPage": 10
            }
        }

    responses.add(
        responses.GET,
        f"{transaction_client.base_url}/transaction",
        json=response_data,
        status=status_code,
    )

@responses.activate
def test_list_transactions(transaction_client):
    setup_mock_response(transaction_client)
    
    # unpack tuple from BaseClient
    data, meta = transaction_client.list()
    
    assert isinstance(data, list)
    assert data[0]["reference"] == "ps_ref_12345"
    assert isinstance(meta, dict)
    assert meta["total"] == 50

@responses.activate
def test_list_transactions_invalid_key(transaction_client):
    mock_response = {"status": False, "message": "Invalid API key"}
    setup_mock_response(transaction_client, mock_response, status_code=401)
    assert_api_error_contains(transaction_client.list, "unauthorized")

@responses.activate
def test_list_transactions_timeout(transaction_client):
    responses.add(
        responses.GET,
        f"{transaction_client.base_url}/transaction",
        body=requests.exceptions.Timeout(),
    )
    assert_api_error_contains(transaction_client.list, "timed out")

@responses.activate
def test_list_transactions_malformed_json(transaction_client):
    responses.add(
        responses.GET,
        f"{transaction_client.base_url}/transaction",
        body="Not a JSON",
        status=200,
    )
    assert_api_error_contains(transaction_client.list, "invalid json response")
