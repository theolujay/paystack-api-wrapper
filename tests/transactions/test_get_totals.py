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

def setup_mock_response(transaction_client, response_data=None, status_code=200):
    if response_data is None:
        response_data = {
            "status": True,
            "message": "Transaction totals",
            "data": {
                "total_transactions": 42670,
                "total_volume": 6617829946,
                "total_volume_by_currency": [
                    {"currency": "NGN", "amount": 6617829946},
                    {"currency": "USD", "amount": 28000}
                ],
                "pending_transfers": 6617829946,
                "pending_transfers_by_currency": [
                    {"currency": "NGN", "amount": 6617829946},
                    {"currency": "USD", "amount": 28000}
                ]
            }
        }

    responses.add(
        responses.GET,
        f"{transaction_client.base_url}/transaction/totals",
        json=response_data,
        status=status_code,
    )

@responses.activate
def test_transaction_totals(transaction_client):
    setup_mock_response(transaction_client)
    
    response = transaction_client.get_totals()
    
    assert isinstance(response, PaystackResponse)
    assert response.data["total_transactions"] == 42670
    assert isinstance(response.data["total_volume_by_currency"], list)
    assert response.data["total_volume_by_currency"][0]["currency"] == "NGN"

@responses.activate
def test_transaction_totals_invalid_key(transaction_client):
    mock_response = {"status": False, "message": "Invalid API key"}
    setup_mock_response(transaction_client, mock_response, status_code=401)
    assert_api_error_contains(transaction_client.get_totals, "invalid api key")

@responses.activate
def test_transaction_totals_timeout(transaction_client):
    responses.add(
        responses.GET,
        f"{transaction_client.base_url}/transaction/totals",
        body=requests.exceptions.Timeout(),
    )
    assert_api_error_contains(transaction_client.get_totals, "timed out")

@responses.activate
def test_transaction_totals_malformed_json(transaction_client):
    responses.add(
        responses.GET,
        f"{transaction_client.base_url}/transaction/totals",
        body="Not a JSON",
        status=200,
    )
    assert_api_error_contains(transaction_client.get_totals, "invalid json response")
