import pytest
import responses
import json
import requests
from paystack import NetworkError
from paystack.exceptions import APIError, ValidationError


from tests.utils import assert_api_error_contains


# --- test_charge_authorization.py ---
def setup_mock_charge_authorization_response(
    transaction_client, payload, response_data=None, status_code=200
):
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
                "id": 4099490251,
            },
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
        "authorization_code": "AUTH_72btv547",
    }
    setup_mock_charge_authorization_response(transaction_client, payload)

    data, meta = transaction_client.charge_authorization(**payload)

    assert data["reference"] == "0m7frfnr47ezyxl"
    assert data["status"] == "success"
    assert data["authorization"]["authorization_code"] == payload["authorization_code"]


@responses.activate
def test_charge_authorization_with_all_params(transaction_client):
    mock_response = {
        "status": True,
        "message": "Charge attempted",
        "data": {
            "amount": 35247,
            "currency": "NGN",
            "transaction_date": "2024-08-22T10:53:49.000Z",
            "status": "success",
            "reference": "0m7frfnr47ezyxl",
            "authorization": {
                "authorization_code": "AUTH_72btv547",
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
            "customer": {"email": "customer@email.com", "customer_code": "CUS_1rkzaqsv4rrhqo6"},
            "id": 4099490251,
        },
    }
    setup_mock_charge_authorization_response(transaction_client, {}, mock_response)

    payload = {
        "email": "customer@email.com",
        "amount": "20000",
        "authorization_code": "AUTH_72btv547",
        "currency": "NGN",
        "reference": "test_ref",
        "channels": ["card"],
        "subaccount": "SUB_test",
        "transaction_charge": 100,
        "bearer": "account",
        "queue": True,
        "metadata": {"custom_fields": "value"},
    }
    data, meta = transaction_client.charge_authorization(**payload)

    assert data["reference"] == "0m7frfnr47ezyxl"
    assert data["status"] == "success"
    assert data["authorization"]["authorization_code"] == payload["authorization_code"]
    request = responses.calls[0].request
    request_payload = json.loads(request.body)

    assert request.method == "POST"
    assert request_payload["email"] == payload["email"]
    assert request_payload["amount"] == payload["amount"]
    assert request_payload["authorization_code"] == payload["authorization_code"]
    assert request_payload["currency"] == payload["currency"]
    assert request_payload["reference"] == payload["reference"]
    assert request_payload["channels"] == payload["channels"]
    assert request_payload["subaccount"] == payload["subaccount"]
    assert request_payload["transaction_charge"] == payload["transaction_charge"]
    assert request_payload["bearer"] == payload["bearer"]
    assert request_payload["queue"] == payload["queue"]
    assert json.loads(request_payload["metadata"]) == payload["metadata"]


@responses.activate
def test_charge_authorization_invalid_key(transaction_client):
    payload = {
        "email": "customer@email.com",
        "amount": "20000",
        "authorization_code": "AUTH_72btv547",
    }
    mock_response = {"status": False, "message": "Invalid API key"}
    setup_mock_charge_authorization_response(
        transaction_client, payload, mock_response, status_code=401
    )
    assert_api_error_contains(
        transaction_client.charge_authorization, "Invalid API key", **payload
    )


# --- test_export_transactions.py ---
def setup_mock_export_transactions_response(
    transaction_client, response_data=None, status_code=200
):
    if response_data is None:
        response_data = {
            "status": True,
            "message": "Export successful",
            "data": {
                "path": "https://s3.eu-west-1.amazonaws.com/files.paystack.co/exports/463433/transactions/Integration_name_transactions_1724324423843.csv?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=...",
                "expiresAt": "2024-08-22 11:01:23",
            },
        }

    responses.add(
        responses.GET,
        f"{transaction_client.base_url}/transaction/export",
        json=response_data,
        status=status_code,
    )


@responses.activate
def test_export_transactions(transaction_client):
    setup_mock_export_transactions_response(transaction_client)

    data, meta = transaction_client.export_transactions()

    assert "path" in data
    assert data["path"].startswith("https://s3.")
    assert "expiresAt" in data


@responses.activate
def test_export_transactions_with_all_params(transaction_client):
    setup_mock_export_transactions_response(transaction_client)
    params = {
        "per_page": 5,
        "page": 2,
        "from_date": "2024-01-01",
        "to_date": "2024-01-31",
        "customer": 123,
        "status": "success",
        "currency": "NGN",
        "amount": 10000,
        "settled": True,
        "settlement": 456,
        "payment_page": 789,
    }
    data, meta = transaction_client.export_transactions(**params)

    assert "path" in data
    assert data["path"].startswith("https://s3.")
    assert "expiresAt" in data
    request = responses.calls[0].request
    assert request.method == "GET"
    assert "perPage=5" in request.url
    assert "page=2" in request.url
    assert "from=2024-01-01" in request.url
    assert "to=2024-01-31" in request.url
    assert "customer=123" in request.url
    assert "status=success" in request.url
    assert "currency=NGN" in request.url
    assert "amount=10000" in request.url
    assert "settled=true" in request.url
    assert "settlement=456" in request.url
    assert "payment_page=789" in request.url


@responses.activate
def test_export_transactions_invalid_key(transaction_client):
    mock_response = {"status": False, "message": "Invalid API key"}
    setup_mock_export_transactions_response(
        transaction_client, mock_response, status_code=401
    )
    assert_api_error_contains(transaction_client.export_transactions, "Invalid API key")


# --- test_fetch.py ---
def setup_mock_fetch_response(
    transaction_client, transaction_id, response_data=None, status_code=200
):
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
                "customer": {"email": "customer@example.com"},
            },
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
    setup_mock_fetch_response(transaction_client, transaction_id)

    data, meta = transaction_client.fetch(transaction_id)

    assert data["id"] == transaction_id
    assert data["reference"] == "ps_ref_12345"


@responses.activate
def test_fetch_transaction_invalid_key(transaction_client):
    transaction_id = 102934
    mock_response = {"status": False, "message": "Invalid API key"}
    setup_mock_fetch_response(
        transaction_client, transaction_id, mock_response, status_code=401
    )
    assert_api_error_contains(
        transaction_client.fetch, "invalid api key", transaction_id
    )


# --- test_get_totals.py ---
def setup_mock_get_totals_response(
    transaction_client, response_data=None, status_code=200
):
    if response_data is None:
        response_data = {
            "status": True,
            "message": "Transaction totals",
            "data": {
                "total_transactions": 42670,
                "total_volume": 6617829946,
                "total_volume_by_currency": [
                    {"currency": "NGN", "amount": 6617829946},
                    {"currency": "USD", "amount": 28000},
                ],
                "pending_transfers": 6617829946,
                "pending_transfers_by_currency": [
                    {"currency": "NGN", "amount": 6617829946},
                    {"currency": "USD", "amount": 28000},
                ],
            },
        }

    responses.add(
        responses.GET,
        f"{transaction_client.base_url}/transaction/totals",
        json=response_data,
        status=status_code,
    )


@responses.activate
def test_transaction_totals(transaction_client):
    setup_mock_get_totals_response(transaction_client)

    data, meta = transaction_client.get_totals()

    assert data["total_transactions"] == 42670
    assert isinstance(data["total_volume_by_currency"], list)
    assert data["total_volume_by_currency"][0]["currency"] == "NGN"


@responses.activate
def test_get_totals_with_all_params(transaction_client):
    setup_mock_get_totals_response(transaction_client)
    params = {
        "per_page": 5,
        "page": 2,
        "from_date": "2024-01-01",
        "to_date": "2024-01-31",
    }
    data, meta = transaction_client.get_totals(**params)

    assert data["total_transactions"] == 42670
    assert isinstance(data["total_volume_by_currency"], list)
    assert data["total_volume_by_currency"][0]["currency"] == "NGN"
    request = responses.calls[0].request
    assert request.method == "GET"
    assert "perPage=5" in request.url
    assert "page=2" in request.url
    assert "from=2024-01-01" in request.url
    assert "to=2024-01-31" in request.url


@responses.activate
def test_transaction_totals_invalid_key(transaction_client):
    mock_response = {"status": False, "message": "Invalid API key"}
    setup_mock_get_totals_response(transaction_client, mock_response, status_code=401)
    assert_api_error_contains(transaction_client.get_totals, "invalid api key")


# --- test_initialize.py ---
def setup_mock_initialize_response(
    transaction_client, response_data=None, status_code=200
):
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
    setup_mock_initialize_response(transaction_client, mock_response)
    data = {"email": "customer@email.com", "amount": "20000", "currency": "NGN"}

    response_data, response_meta = transaction_client.initialize(
        email=data["email"], amount=data["amount"]
    )
    request = responses.calls[0].request
    payload = json.loads(request.body)

    assert request.method == "POST"
    assert response_data["reference"] == "re4lyvq3s3"
    assert payload == data


@responses.activate
def test_initialize_transaction_with_all_params(transaction_client):
    mock_response = {
        "status": True,
        "message": "Authorization URL created",
        "data": {
            "authorization_url": "https://checkout.paystack.com/3ni8kdavz62431k",
            "access_code": "3ni8kdavz62431k",
            "reference": "re4lyvq3s3",
        },
    }
    setup_mock_initialize_response(transaction_client, mock_response)
    payload = {
        "email": "customer@email.com",
        "amount": "20000",
        "currency": "NGN",
        "reference": "test_ref",
        "callback_url": "https://example.com/callback",
        "plan": "PLN_test",
        "invoice_limit": 5,
        "metadata": {"custom_fields": "value"},
        "channels": ["card", "bank"],
        "split_code": "SPL_test",
        "subaccount": "SUB_test",
        "transaction_charge": 100,
        "bearer": "account",
    }

    response_data, response_meta = transaction_client.initialize(**payload)
    request = responses.calls[0].request
    request_payload = json.loads(request.body)

    assert request.method == "POST"
    assert response_data["reference"] == "re4lyvq3s3"
    assert request_payload["email"] == payload["email"]
    assert request_payload["amount"] == payload["amount"]
    assert request_payload["currency"] == payload["currency"]
    assert request_payload["reference"] == payload["reference"]
    assert request_payload["callback_url"] == payload["callback_url"]
    assert request_payload["plan"] == payload["plan"]
    assert request_payload["invoice_limit"] == payload["invoice_limit"]
    assert json.loads(request_payload["metadata"]) == payload["metadata"]
    assert request_payload["channels"] == payload["channels"]
    assert request_payload["split_code"] == payload["split_code"]
    assert request_payload["subaccount"] == payload["subaccount"]
    assert request_payload["transaction_charge"] == payload["transaction_charge"]
    assert request_payload["bearer"] == payload["bearer"]


@responses.activate
def test_initialize_transaction_with_empty_metadata(transaction_client):
    mock_response = {
        "status": True,
        "message": "Authorization URL created",
        "data": {
            "authorization_url": "https://checkout.paystack.com/3ni8kdavz62431k",
            "access_code": "3ni8kdavz62431k",
            "reference": "re4lyvq3s3",
        },
    }
    setup_mock_initialize_response(transaction_client, mock_response)
    payload = {
        "email": "customer@email.com",
        "amount": "20000",
        "currency": "NGN",
        "metadata": {},
    }

    response_data, response_meta = transaction_client.initialize(**payload)
    request = responses.calls[0].request
    request_payload = json.loads(request.body)

    # The metadata field is expected to be a JSON string in the request payload
    print(f"request_payload: {request_payload}") # Debug print
    assert "metadata" in request_payload
    assert request_payload["metadata"] == json.dumps(payload["metadata"])


@pytest.mark.parametrize(
    "test_kwargs",
    [
        {"amount": 20000},
        {"email": "customer@email.com"},
    ],
)
def test_validate_transaction_missing_required_fields(transaction_client, test_kwargs):
    """Test validation for missing required fields."""
    with pytest.raises(TypeError):
        transaction_client.initialize(**test_kwargs)


@responses.activate
def test_initialize_transaction_invalid_api_key(transaction_client):
    mock_response = {
        "status": False,
        "message": "Invalid API key",
    }
    setup_mock_initialize_response(transaction_client, mock_response, 401)
    assert_api_error_contains(
        transaction_client.initialize,
        "invalid api key",
        email="customer@email.com",
        amount=20000,
    )


@responses.activate
def test_initialize_transaction_timeout(transaction_client):
    responses.add(
        responses.POST,
        f"{transaction_client.base_url}/transaction/initialize",
        body=requests.exceptions.Timeout(),
    )
    with pytest.raises(NetworkError) as excinfo:
        transaction_client.initialize(email="customer@email.com", amount=20000)
        expected_keyword = "Request failed:"
        assert str(expected_keyword).lower() in str(excinfo.value).lower()


# === Invalid Email Tests ===
@pytest.mark.parametrize(
    "invalid_email",
    [
        "invalid-email",  # No @ symbol
        "user@",  # No domain
        "@domain.com",  # No user part
        "user@@domain.com",  # Multiple @ symbols
        "a" * 250 + "@example.com",  # Too long
    ],
)
def test_invalid_email_formats(transaction_client, invalid_email):
    """Test validation for various invalid email formats"""
    with pytest.raises(ValidationError) as excinfo:
        transaction_client.initialize(email=invalid_email, amount=20000)
    assert "email" in str(excinfo.value).lower()


# === Invalid Amount Tests ===
@pytest.mark.parametrize(
    "invalid_amount,expected_keyword",
    [
        ("abc", "amount"),  # Non-numeric
        ("-1000", "amount"),  # Negative
        ("0", "amount"),  # Zero
        ("200.50", "amount"),  # Decimal
        ("20,000", "amount"),  # With commas
        ("₦20000", "amount"),  # With currency symbol
    ],
)
def test_invalid_amounts(transaction_client, invalid_amount, expected_keyword):
    """Test validation for various invalid amount formats"""
    with pytest.raises(ValidationError) as excinfo:
        transaction_client.initialize(email="test@example.com", amount=invalid_amount)
    assert expected_keyword in str(excinfo.value).lower()


# --- test_list_transactions.py ---
def setup_mock_list_transactions_response(
    transaction_client, response_data=None, status_code=200
):
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
                    "customer": {"email": "customer@example.com"},
                }
            ],
            "meta": {"total": 50, "page": 1, "perPage": 10},
        }

    responses.add(
        responses.GET,
        f"{transaction_client.base_url}/transaction",
        json=response_data,
        status=status_code,
    )


@responses.activate
def test_list_transactions(transaction_client):
    setup_mock_list_transactions_response(transaction_client)

    data, meta = transaction_client.list_transactions()

    assert isinstance(data, list)
    assert data[0]["reference"] == "ps_ref_12345"
    assert isinstance(meta, dict)
    assert meta["total"] == 50


@responses.activate
def test_list_transactions_invalid_key(transaction_client):
    mock_response = {"status": False, "message": "Invalid API key"}
    setup_mock_list_transactions_response(
        transaction_client, mock_response, status_code=401
    )
    assert_api_error_contains(transaction_client.list_transactions, "Invalid API key")


@responses.activate
def test_list_transactions_with_all_params(transaction_client):
    setup_mock_list_transactions_response(transaction_client)
    params = {
        "per_page": 5,
        "page": 2,
        "customer": 123,
        "terminal_id": "T123",
        "status": "success",
        "from_date": "2024-01-01",
        "to_date": "2024-01-31",
        "amount": 10000,
    }
    data, meta = transaction_client.list_transactions(**params)

    assert isinstance(data, list)
    assert data[0]["reference"] == "ps_ref_12345"
    assert isinstance(meta, dict)
    assert meta["total"] == 50
    request = responses.calls[0].request
    assert request.method == "GET"
    assert "perPage=5" in request.url
    assert "page=2" in request.url
    assert "customer=123" in request.url
    assert "terminalid=T123" in request.url
    assert "status=success" in request.url
    assert "from=2024-01-01" in request.url
    assert "to=2024-01-31" in request.url
    assert "amount=10000" in request.url


@responses.activate
def test_list_transactions_invalid_status(transaction_client):
    with pytest.raises(APIError, match="status must be one of: 'failed', 'success', 'abandoned'"):
        transaction_client.list_transactions(status="invalid_status")


# --- test_partial_debit.py ---
def setup_mock_partial_debit_response(
    transaction_client, response_data=None, status_code=200
):
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
                "id": 4099546180,
            },
        }

    responses.add(
        responses.POST,
        f"{transaction_client.base_url}/transaction/partial_debit",
        json=response_data,
        status=status_code,
    )


@responses.activate
def test_partial_debit_success(transaction_client):
    setup_mock_partial_debit_response(transaction_client)

    payload = {
        "authorization_code": "AUTH_72btv547",
        "currency": "NGN",
        "amount": "20000",
        "email": "customer@email.com",
        "reference": "test_ref",
        "at_least": "10000",
    }
    data, meta = transaction_client.partial_debit(**payload)

    assert data["status"] == "success"
    assert data["currency"] == "NGN"
    assert data["amount"] == 50000
    assert "authorization" in data
    assert data["authorization"]["reusable"] is True
    request = responses.calls[0].request
    request_payload = json.loads(request.body)
    assert request_payload["reference"] == payload["reference"]
    assert request_payload["at_least"] == payload["at_least"]


@responses.activate
def test_partial_debit_invalid_key(transaction_client):
    mock_response = {"status": False, "message": "Invalid API key"}
    setup_mock_partial_debit_response(
        transaction_client, mock_response, status_code=401
    )

    payload = {
        "authorization_code": "AUTH_invalid",
        "currency": "NGN",
        "amount": "20000",
        "email": "customer@email.com",
    }
    assert_api_error_contains(
        transaction_client.partial_debit, "invalid api key", **payload
    )


@responses.activate
def test_partial_debit_invalid_currency(transaction_client):
    with pytest.raises(ValidationError, match="currency must be 'NGN' or 'GHS' for partial debit"):
        transaction_client.partial_debit(
            authorization_code="AUTH_test",
            currency="USD",
            amount="20000",
            email="customer@example.com",
        )


# --- test_verify.py ---
def setup_mock_verify_response(
    transaction_client, reference, response_data=None, status_code=200
):
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
        },
    }
    setup_mock_verify_response(transaction_client, reference, mock_response)

    data, meta = transaction_client.verify(reference)

    assert data["reference"] == reference
    assert data["status"] == "success"


@responses.activate
def test_verify_transaction_invalid_key(transaction_client):
    reference = "adhvousgtsnsl"
    mock_response = {"status": False, "message": "Invalid API key"}
    setup_mock_verify_response(
        transaction_client, reference, mock_response, status_code=401
    )

    assert_api_error_contains(transaction_client.verify, "invalid api key", reference)


# --- test_view_timeline.py ---
def setup_mock_view_timeline_response(
    transaction_client, id_or_reference, response_data=None, status_code=200
):
    if response_data is None:
        response_data = {
            "status": True,
            "message": "Timeline retrieved",
            "data": {
                "start_time": 1724318098,
                "time_spent": 4,
                "attempts": 1,
                "errors": 0,
                "success": True,
                "mobile": False,
                "input": [],
                "history": [
                    {
                        "type": "action",
                        "message": "Attempted to pay with card",
                        "time": 3,
                    },
                    {
                        "type": "success",
                        "message": "Successfully paid with card",
                        "time": 4,
                    },
                ],
            },
        }

    responses.add(
        responses.GET,
        f"{transaction_client.base_url}/transaction/timeline/{id_or_reference}",
        json=response_data,
        status=status_code,
    )


@responses.activate
def test_view_timeline(transaction_client):
    id_or_reference = "0m7frfnr47ezyxl"
    setup_mock_view_timeline_response(transaction_client, id_or_reference)

    data, meta = transaction_client.view_timeline(id_or_reference)

    assert data["success"] is True
    assert isinstance(data["history"], list)
    assert data["history"][0]["message"] == "Attempted to pay with card"


@responses.activate
def test_view_timeline_invalid_key(transaction_client):
    id_or_reference = "0m7frfnr47ezyxl"
    mock_response = {"status": False, "message": "Invalid API key"}
    setup_mock_view_timeline_response(
        transaction_client, id_or_reference, mock_response, status_code=401
    )
    assert_api_error_contains(
        transaction_client.view_timeline, "invalid api key", id_or_reference
    )