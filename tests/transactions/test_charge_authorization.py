import pytest
import requests
import responses
from api.exceptions import APIError
from api.core import PaystackResponse

# === Test Helpers ===
def assert_api_error_contains(callable_method, expected_keyword, *args, **kwargs):
    with pytest.raises(APIError) as excinfo:
        callable_method(*args, **kwargs)
    assert str(expected_keyword).lower() in str(excinfo.value).lower()

def setup_mock_response(transaction_client, payload, response_data=None, status_code=200):
    if response_data is None:
        response_data = {
            "status": True,
            "message": "Charge attempted",
            "data": {
                "amount": 35247,
                "currency": "NGN",
                "transaction_date": "2024-08-22T10:53:49.000Z",
                "status": "success",
                "reference": "0m7frfnr47ezyxl",
                "authorization": {
                    "authorization_code": payload.get("authorization_code"),
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
                },
                "customer": {
                    "email": payload.get("email"),
                    "customer_code": "CUS_1rkzaqsv4rrhqo6",
                },
                "id": 4099490251
            }
        }

    responses.add(
        responses.POST,
        f"{transaction_client.base_url}/transaction/charge_authorization",
        json=response_data,
        status=status_code,
    )

@responses.activate
def test_charge_authorization(transaction_client):
    payload = {
        "email": "customer@email.com",
        "amount": "20000",
        "authorization_code": "AUTH_72btv547"
    }
    setup_mock_response(transaction_client, payload)
    
    response = transaction_client.charge_authorization(**payload)
    
    assert isinstance(response, PaystackResponse)
    assert response.data["reference"] == "0m7frfnr47ezyxl"
    assert response.data["status"] == "success"
    assert response.data["authorization"]["authorization_code"] == payload["authorization_code"]

@responses.activate
def test_charge_authorization_invalid_key(transaction_client):
    payload = {
        "email": "customer@email.com",
        "amount": "20000",
        "authorization_code": "AUTH_72btv547"
    }
    mock_response = {"status": False, "message": "Invalid API key"}
    setup_mock_response(transaction_client, payload, mock_response, status_code=401)
    assert_api_error_contains(transaction_client.charge_authorization, "invalid api key", **payload)

@responses.activate
def test_charge_authorization_timeout(transaction_client):
    payload = {
        "email": "customer@email.com",
        "amount": "20000",
        "authorization_code": "AUTH_72btv547"
    }
    responses.add(
        responses.POST,
        f"{transaction_client.base_url}/transaction/charge_authorization",
        body=requests.exceptions.Timeout(),
    )
    assert_api_error_contains(transaction_client.charge_authorization, "timed out", **payload)

@responses.activate
def test_charge_authorization_malformed_json(transaction_client):
    payload = {
        "email": "customer@email.com",
        "amount": "20000",
        "authorization_code": "AUTH_72btv547"
    }
    responses.add(
        responses.POST,
        f"{transaction_client.base_url}/transaction/charge_authorization",
        body="Not a JSON",
        status=200,
    )
    assert_api_error_contains(transaction_client.charge_authorization, "invalid json response", **payload)
