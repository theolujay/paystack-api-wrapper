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
            "message": "Export successful",
            "data": {
                "path": "https://s3.eu-west-1.amazonaws.com/files.paystack.co/exports/463433/transactions/Integration_name_transactions_1724324423843.csv?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=...",
                "expiresAt": "2024-08-22 11:01:23"
            }
        }

    responses.add(
        responses.GET,
        f"{transaction_client.base_url}/transaction/export",
        json=response_data,
        status=status_code,
    )

@responses.activate
def test_export_transactions(transaction_client):
    setup_mock_response(transaction_client)
    
    data = transaction_client.export()
    
    assert isinstance(data, dict)
    assert "path" in data
    assert data["path"].startswith("https://s3.")
    assert "expiresAt" in data

@responses.activate
def test_export_transactions_invalid_key(transaction_client):
    mock_response = {"status": False, "message": "Invalid API key"}
    setup_mock_response(transaction_client, mock_response, status_code=401)
    assert_api_error_contains(transaction_client.export, "unauthorized")

@responses.activate
def test_export_transactions_timeout(transaction_client):
    responses.add(
        responses.GET,
        f"{transaction_client.base_url}/transaction/export",
        body=requests.exceptions.Timeout(),
    )
    assert_api_error_contains(transaction_client.export, "timed out")

@responses.activate
def test_export_transactions_malformed_json(transaction_client):
    responses.add(
        responses.GET,
        f"{transaction_client.base_url}/transaction/export",
        body="Not a JSON",
        status=200,
    )
    assert_api_error_contains(transaction_client.export, "invalid json response")
