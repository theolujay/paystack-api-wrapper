import json
import re
import pytest
import requests
import responses

from api.exceptions import APIError


# === Test Helpers ===
def assert_api_error_contains(transaction_client, expected_keyword, **kwargs):
    """Helper to test that APIError is raised and contains expected keyword"""
    with pytest.raises(APIError) as excinfo:
        transaction_client.initialize(**kwargs)
    assert str(expected_keyword).lower() in str(excinfo.value).lower()

def setup_mock_response(transaction_client, response_data=None, status_code=200):
    """Helper to set up a mock response"""
    if response_data is None:
        response_data = {
            "status": True,
            "message": "Success",
            "data": {"reference": "rest_ref"},
        }

    responses.add(
        responses.POST,
        f"{transaction_client.base_url}/transaction/initialize",
        json=response_data,
        status=status_code,
    )


@responses.activate
def test_initialize_transaction(transaction_client):
    mock_response = {
        "status": True,
        "message": "Authorization URL created",
        "data": {
            "authorization_url": "https://checkout.paystack.com/3ni8kdavz62431k",
            "access_code": "3ni8kdavz62431k",
            "reference": "re4lyvq3s3",
        },
    }
    setup_mock_response(transaction_client, mock_response)
    data = {"email": "customer@email.com", "amount": 20000}

    response = transaction_client.initialize(email=data["email"], amount=data["amount"])
    request = responses.calls[0].request
    payload = json.loads(request.body)

    assert request.method == "POST"
    assert all(
        key in response for key in ["authorization_url", "access_code", "reference"]
    )
    assert payload == data


@pytest.mark.parametrize(
    "missing_arg, test_kwargs",
    [
        ("email", {"amount": 20000}),
        ("amount", {"email": "customer@email.com"}),
    ],
)
def test_validate_transaction_missing_required_fields(transaction_client, missing_arg, test_kwargs):
    """Test validation for missing required fields."""
    with pytest.raises(APIError) as excinfo:
        transaction_client.initialize(**test_kwargs)
    assert missing_arg in str(excinfo.value).lower()


@responses.activate
def test_initialize_transaction_invalid_api_key(transaction_client):
    mock_response = {
        "status": False,
        "message": "Invalid API key",
    }
    setup_mock_response(transaction_client, mock_response, 401)
    assert_api_error_contains(
        transaction_client, "unauthorized", email="customer@email.com", amount=20000
    )

@responses.activate
def test_initialize_transaction_timeout(transaction_client):
    responses.add(
        responses.POST,
        f"{transaction_client.base_url}/transaction/initialize",
        body=requests.exceptions.Timeout()
    )
    
    assert_api_error_contains(
        transaction_client, "Request timed out", email="customer@email.com", amount=20000
    )
@responses.activate
def test_initialize_transaction_malformed_json(transaction_client):
    responses.add(
        responses.POST,
        f"{transaction_client.base_url}/transaction/initialize",
        body="Not a JSON",
        status=200
    )

    assert_api_error_contains(
        transaction_client, "Invalid JSON response", email="customer@email.com", amount=20000
    )
    
# === Invalid Email Tests ===
@pytest.mark.parametrize("invalid_email", [
    "invalid-email",           # No @ symbol
    "user@",                   # No domain
    "@domain.com",             # No user part
    "user@@domain.com",        # Multiple @ symbols
    "a" * 250 + "@example.com" # Too long
])
def test_invalid_email_formats(transaction_client, invalid_email):
    """Test validation for various invalid email formats"""
    assert_api_error_contains(transaction_client, "email", email=invalid_email, amount=20000)

# === Invalid Amount Tests ===
@pytest.mark.parametrize("invalid_amount,expected_keyword", [
    ("abc", "number"),           # Non-numeric
    ("-1000", "amount"),         # Negative
    ("0", "amount"),             # Zero
    ("200.50", "decimal"),        # Decimal
    ("20,000", "comma"),        # With commas
    ("₦20000", "number"),        # With currency symbol
])
def test_invalid_amounts(transaction_client, invalid_amount, expected_keyword):
    """Test validation for various invalid amount formats"""
    assert_api_error_contains(transaction_client, expected_keyword, 
                            email="test@example.com", amount=invalid_amount)