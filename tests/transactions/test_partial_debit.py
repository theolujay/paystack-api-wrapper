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
            "message": "Charge attempted",
            "data": {
                "amount": 50000,
                "currency": "NGN",
                "transaction_date": "2024-08-22T11:13:48.000Z",
                "status": "success",
                "reference": "ofuhmnzw05vny9j",
                "gateway_response": "Approved",
                "authorization": {
                    "authorization_code": "AUTH_uh8bcl3zbn",
                    "bin": "408408",
                    "last4": "4081",
                    "exp_month": "12",
                    "exp_year": "2030",
                    "channel": "card",
                    "card_type": "visa",
                    "bank": "TEST BANK",
                    "country_code": "NG",
                    "brand": "visa",
                    "reusable": True,
                    "signature": "SIG_yEXu7dLBeqG0kU7g95Ke",
                },
                "customer": {
                    "email": "demo@test.com",
                    "customer_code": "CUS_1rkzaqsv4rrhqo6",
                },
                "requested_amount": 50000,
                "id": 4099546180
            }
        }

    responses.add(
        responses.POST,
        f"{transaction_client.base_url}/transaction/partial_debit",
        json=response_data,
        status=status_code,
    )

@responses.activate
def test_partial_debit_success(transaction_client):
    setup_mock_response(transaction_client)
    
    payload = {
        "authorization_code": "AUTH_72btv547",
        "currency": "NGN",
        "amount": "20000",
        "email": "customer@email.com"
    }
    response = transaction_client.partial_debit(**payload)
    
    assert isinstance(response, PaystackResponse)
    assert response.data["status"] == "success"
    assert response.data["currency"] == "NGN"
    assert response.data["amount"] == 50000
    assert "authorization" in response.data
    assert response.data["authorization"]["reusable"] is True

@responses.activate
def test_partial_debit_invalid_key(transaction_client):
    mock_response = {"status": False, "message": "Invalid API key"}
    setup_mock_response(transaction_client, mock_response, status_code=401)
    
    payload = {
        "authorization_code": "AUTH_invalid",
        "currency": "NGN",
        "amount": "20000",
        "email": "customer@email.com"
    }
    assert_api_error_contains(transaction_client.partial_debit, "invalid api key", **payload)

@responses.activate
def test_partial_debit_timeout(transaction_client):
    responses.add(
        responses.POST,
        f"{transaction_client.base_url}/transaction/partial_debit",
        body=requests.exceptions.Timeout(),
    )
    payload = {
        "authorization_code": "AUTH_72btv547",
        "currency": "NGN",
        "amount": "20000",
        "email": "customer@email.com"
    }
    assert_api_error_contains(transaction_client.partial_debit, "timed out", **payload)

@responses.activate
def test_partial_debit_malformed_json(transaction_client):
    responses.add(
        responses.POST,
        f"{transaction_client.base_url}/transaction/partial_debit",
        body="Not a JSON",
        status=200,
    )
    payload = {
        "authorization_code": "AUTH_72btv547",
        "currency": "NGN",
        "amount": "20000",
        "email": "customer@email.com"
    }
    assert_api_error_contains(transaction_client.partial_debit, "invalid json response", **payload)