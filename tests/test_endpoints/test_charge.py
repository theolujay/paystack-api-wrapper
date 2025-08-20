import pytest
import responses

from paystack import ValidationError
from tests.utils import assert_api_error_contains


@responses.activate
def test_create_charge(charge_client):
    payload = {
        "email": "customer@example.com",
        "amount": "10000",
    }
    mock_response = {
        "status": True,
        "message": "Charge initiated",
        "data": {"reference": "test_ref"},
    }
    responses.add(
        responses.POST,
        f"{charge_client.base_url}/charge",
        json=mock_response,
        status=200,
    )

    data, meta = charge_client.create(**payload)

    assert data["reference"] == "test_ref"
    assert meta == {}


@responses.activate
def test_create_charge_with_all_optional_params(charge_client):
    payload = {
        "email": "customer_all@example.com",
        "amount": "20000",
        "split_code": "SPL_all",
        "subaccount": "ACCT_all",
        "transaction_charge": 500,
        "bearer": "account",
        "bank": {"code": "044", "account_number": "0123456789"},
        "bank_transfer": {"account_number": "0987654321"},
        "ussd": {"type": "737"},
        "mobile_money": {"phone": "08012345678", "provider": "mtn"},
        "qr": {"provider": "visa"},
        "authorization_code": "AUTH_all",
        "pin": "1234",
        "metadata": {"custom_fields": "value_all"},
        "reference": "test_ref_all",
        "device_id": "device_all",
        "birthday": "1990-01-01",
    }
    mock_response = {
        "status": True,
        "message": "Charge initiated",
        "data": {"reference": "test_ref_all"},
    }
    responses.add(
        responses.POST,
        f"{charge_client.base_url}/charge",
        json=mock_response,
        status=200,
    )

    data, meta = charge_client.create(**payload)

    assert data["reference"] == "test_ref_all"
    assert meta == {}


@responses.activate
def test_create_charge_invalid_bearer(charge_client):
    payload = {
        "email": "customer@example.com",
        "amount": "10000",
        "bearer": "invalid",
    }
    with pytest.raises(ValidationError, match="bearer must be either 'account' or 'subaccount'"):
        charge_client.create(**payload)


@responses.activate
def test_create_charge_invalid_email(charge_client):
    payload = {
        "email": "invalid-email",
        "amount": "10000",
    }
    with pytest.raises(ValidationError):
        charge_client.create(**payload)


@responses.activate
def test_create_charge_invalid_amount(charge_client):
    payload = {
        "email": "customer@example.com",
        "amount": "abc",
    }
    with pytest.raises(ValidationError):
        charge_client.create(**payload)


@responses.activate
def test_submit_pin(charge_client):
    payload = {
        "pin": "1234",
        "reference": "test_ref",
    }
    mock_response = {
        "status": True,
        "message": "PIN submitted",
        "data": {"status": "success"},
    }
    responses.add(
        responses.POST,
        f"{charge_client.base_url}/charge/submit_pin",
        json=mock_response,
        status=200,
    )

    data, meta = charge_client.submit_pin(**payload)

    assert data["status"] == "success"
    assert meta == {}


@responses.activate
def test_submit_pin_invalid_key(charge_client):
    payload = {
        "pin": "1234",
        "reference": "test_ref",
    }
    mock_response = {"status": False, "message": "Invalid API key"}
    responses.add(
        responses.POST,
        f"{charge_client.base_url}/charge/submit_pin",
        json=mock_response,
        status=401,
    )
    assert_api_error_contains(charge_client.submit_pin, "Invalid API key", **payload)


@responses.activate
def test_submit_otp(charge_client):
    payload = {
        "otp": "123456",
        "reference": "test_ref",
    }
    mock_response = {
        "status": True,
        "message": "OTP submitted",
        "data": {"status": "success"},
    }
    responses.add(
        responses.POST,
        f"{charge_client.base_url}/charge/submit_otp",
        json=mock_response,
        status=200,
    )

    data, meta = charge_client.submit_otp(**payload)

    assert data["status"] == "success"
    assert meta == {}


@responses.activate
def test_submit_otp_invalid_key(charge_client):
    payload = {
        "otp": "123456",
        "reference": "test_ref",
    }
    mock_response = {"status": False, "message": "Invalid API key"}
    responses.add(
        responses.POST,
        f"{charge_client.base_url}/charge/submit_otp",
        json=mock_response,
        status=401,
    )
    assert_api_error_contains(charge_client.submit_otp, "Invalid API key", **payload)


@responses.activate
def test_submit_phone(charge_client):
    payload = {
        "phone": "08012345678",
        "reference": "test_ref",
    }
    mock_response = {
        "status": True,
        "message": "Phone submitted",
        "data": {"status": "success"},
    }
    responses.add(
        responses.POST,
        f"{charge_client.base_url}/charge/submit_phone",
        json=mock_response,
        status=200,
    )

    data, meta = charge_client.submit_phone(**payload)

    assert data["status"] == "success"
    assert meta == {}


@responses.activate
def test_submit_phone_invalid_key(charge_client):
    payload = {
        "phone": "08012345678",
        "reference": "test_ref",
    }
    mock_response = {"status": False, "message": "Invalid API key"}
    responses.add(
        responses.POST,
        f"{charge_client.base_url}/charge/submit_phone",
        json=mock_response,
        status=401,
    )
    assert_api_error_contains(charge_client.submit_phone, "Invalid API key", **payload)


@responses.activate
def test_submit_birthday(charge_client):
    payload = {
        "birthday": "1990-01-01",
        "reference": "test_ref",
    }
    mock_response = {
        "status": True,
        "message": "Birthday submitted",
        "data": {"status": "success"},
    }
    responses.add(
        responses.POST,
        f"{charge_client.base_url}/charge/submit_birthday",
        json=mock_response,
        status=200,
    )

    data, meta = charge_client.submit_birthday(**payload)

    assert data["status"] == "success"
    assert meta == {}


@responses.activate
def test_submit_birthday_invalid_key(charge_client):
    payload = {
        "birthday": "1990-01-01",
        "reference": "test_ref",
    }
    mock_response = {"status": False, "message": "Invalid API key"}
    responses.add(
        responses.POST,
        f"{charge_client.base_url}/charge/submit_birthday",
        json=mock_response,
        status=401,
    )
    assert_api_error_contains(
        charge_client.submit_birthday, "Invalid API key", **payload
    )


@responses.activate
def test_submit_address(charge_client):
    payload = {
        "address": "123 Main St",
        "reference": "test_ref",
        "city": "Lagos",
        "state": "Lagos",
        "zip_code": "100001",
    }
    mock_response = {
        "status": True,
        "message": "Address submitted",
        "data": {"status": "success"},
    }
    responses.add(
        responses.POST,
        f"{charge_client.base_url}/charge/submit_address",
        json=mock_response,
        status=200,
    )

    data, meta = charge_client.submit_address(**payload)

    assert data["status"] == "success"
    assert meta == {}


@responses.activate
def test_submit_address_invalid_key(charge_client):
    payload = {
        "address": "123 Main St",
        "reference": "test_ref",
        "city": "Lagos",
        "state": "Lagos",
        "zip_code": "100001",
    }
    mock_response = {"status": False, "message": "Invalid API key"}
    responses.add(
        responses.POST,
        f"{charge_client.base_url}/charge/submit_address",
        json=mock_response,
        status=401,
    )
    assert_api_error_contains(
        charge_client.submit_address, "Invalid API key", **payload
    )


@responses.activate
def test_check_pending_charge(charge_client):
    reference = "test_ref"
    mock_response = {
        "status": True,
        "message": "Charge status retrieved",
        "data": {"status": "success", "reference": reference},
    }
    responses.add(
        responses.GET,
        f"{charge_client.base_url}/charge/{reference}",
        json=mock_response,
        status=200,
    )

    data, meta = charge_client.check_pending_charge(reference=reference)

    assert data["status"] == "success"
    assert data["reference"] == reference
    assert meta == {}


@responses.activate
def test_check_pending_charge_invalid_key(charge_client):
    reference = "test_ref"
    mock_response = {"status": False, "message": "Invalid API key"}
    responses.add(
        responses.GET,
        f"{charge_client.base_url}/charge/{reference}",
        json=mock_response,
        status=401,
    )
    assert_api_error_contains(
        charge_client.check_pending_charge, "Invalid API key", reference=reference
    )