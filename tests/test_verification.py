import pytest
import responses
from api.exceptions import AuthenticationError
from api.verification import VerificationAPI


from .utils import assert_api_error_contains


@responses.activate
def test_resolve_account(verification_client):
    account_number = "0123456789"
    bank_code = "044"
    mock_response = {
        "status": True,
        "message": "Account resolved",
        "data": {"account_number": account_number, "account_name": "Test User"},
    }
    responses.add(
        responses.GET,
        f"{verification_client.base_url}/bank/resolve?account_number={account_number}&bank_code={bank_code}",
        json=mock_response,
        status=200,
    )

    data, meta = verification_client.resolve_account(
        account_number=account_number, bank_code=bank_code
    )

    assert data["account_number"] == account_number
    assert data["account_name"] == "Test User"
    assert meta == {}


@responses.activate
def test_resolve_account_invalid_key(verification_client):
    account_number = "0123456789"
    bank_code = "044"
    mock_response = {"status": False, "message": "Invalid API key"}
    responses.add(
        responses.GET,
        f"{verification_client.base_url}/bank/resolve?account_number={account_number}&bank_code={bank_code}",
        json=mock_response,
        status=401,
    )
    assert_api_error_contains(
        verification_client.resolve_account,
        "Invalid API key",
        account_number=account_number,
        bank_code=bank_code,
    )


@responses.activate
def test_validate_account(verification_client):
    payload = {
        "account_name": "Test User",
        "account_number": "0123456789",
        "account_type": "personal",
        "bank_code": "044",
        "country_code": "NG",
        "document_type": "identityNumber",
        "document_number": "12345678901",
    }
    mock_response = {
        "status": True,
        "message": "Account validated",
        "data": {"account_number": payload["account_number"]},
    }
    responses.add(
        responses.POST,
        f"{verification_client.base_url}/bank/validate",
        json=mock_response,
        status=200,
    )

    data, meta = verification_client.validate_account(**payload)

    assert data["account_number"] == payload["account_number"]
    assert meta == {}


@responses.activate
def test_resolve_card_bin(verification_client):
    card_bin = "123456"
    mock_response = {
        "status": True,
        "message": "Card BIN resolved",
        "data": {"bin": card_bin, "brand": "Visa"},
    }
    responses.add(
        responses.GET,
        f"{verification_client.base_url}/decision/bin/{card_bin}",
        json=mock_response,
        status=200,
    )

    data, meta = verification_client.resolve_card_bin(card_bin=card_bin)

    assert data["bin"] == card_bin
    assert data["brand"] == "Visa"
    assert meta == {}