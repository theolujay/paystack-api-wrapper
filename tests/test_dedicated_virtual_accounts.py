import pytest
import responses

from .utils import assert_api_error_contains
from paystack_client.exceptions import APIError
from paystack_client.dedicated_virtual_accounts import DedicatedVirtualAccountsAPI


@responses.activate
def test_create_dedicated_virtual_account(dedicated_virtual_accounts_client):
    payload = {
        "customer": "CUS_test",
        "preferred_bank": "wema-bank",
    }
    mock_response = {
        "status": True,
        "message": "Dedicated account created",
        "data": {"customer": payload["customer"], "account_number": "0123456789"},
    }
    responses.add(
        responses.POST,
        f"{dedicated_virtual_accounts_client.base_url}/dedicated_account",
        json=mock_response,
        status=200,
    )

    data, meta = dedicated_virtual_accounts_client.create_dedicated_virtual_account(**payload)

    assert data["customer"] == payload["customer"]
    assert data["account_number"] == "0123456789"
    assert meta == {}


@responses.activate
def test_create_dedicated_virtual_account_invalid_key(dedicated_virtual_accounts_client):
    payload = {
        "customer": "CUS_test",
        "preferred_bank": "wema-bank",
    }
    mock_response = {"status": False, "message": "Invalid API key"}
    responses.add(
        responses.POST,
        f"{dedicated_virtual_accounts_client.base_url}/dedicated_account",
        json=mock_response,
        status=401,
    )
    assert_api_error_contains(
        dedicated_virtual_accounts_client.create_dedicated_virtual_account,
        "Invalid API key",
        **payload,
    )


@responses.activate
def test_assign_dedicated_virtual_account(dedicated_virtual_accounts_client):
    payload = {
        "email": "customer@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "phone": "08012345678",
        "preferred_bank": "wema-bank",
        "country": "NG",
    }
    mock_response = {
        "status": True,
        "message": "Dedicated account assigned",
        "data": {"customer": payload["email"], "account_number": "0123456789"},
    }
    responses.add(
        responses.POST,
        f"{dedicated_virtual_accounts_client.base_url}/dedicated_account/assign",
        json=mock_response,
        status=200,
    )

    data, meta = dedicated_virtual_accounts_client.assign_dedicated_virtual_account(**payload)

    assert data["customer"] == payload["email"]
    assert data["account_number"] == "0123456789"
    assert meta == {}


@responses.activate
def test_assign_dedicated_virtual_account_invalid_key(dedicated_virtual_accounts_client):
    payload = {
        "email": "customer@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "phone": "08012345678",
        "preferred_bank": "wema-bank",
        "country": "NG",
    }
    mock_response = {"status": False, "message": "Invalid API key"}
    responses.add(
        responses.POST,
        f"{dedicated_virtual_accounts_client.base_url}/dedicated_account/assign",
        json=mock_response,
        status=401,
    )
    assert_api_error_contains(
        dedicated_virtual_accounts_client.assign_dedicated_virtual_account,
        "Invalid API key",
        **payload,
    )


@responses.activate
def test_list_dedicated_virtual_accounts(dedicated_virtual_accounts_client):
    mock_response = {
        "status": True,
        "message": "Dedicated accounts retrieved",
        "data": [{"account_number": "0123456789"}, {"account_number": "9876543210"}],
    }
    responses.add(
        responses.GET,
        f"{dedicated_virtual_accounts_client.base_url}/dedicated_account",
        json=mock_response,
        status=200,
    )

    data, meta = dedicated_virtual_accounts_client.list_dedicated_virtual_accounts()

    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["account_number"] == "0123456789"
    assert meta == {}


@responses.activate
def test_list_dedicated_virtual_accounts_with_params(dedicated_virtual_accounts_client):
    mock_response = {
        "status": True,
        "message": "Dedicated accounts retrieved",
        "data": [{"account_number": "0123456789"}],
    }
    responses.add(
        responses.GET,
        f"{dedicated_virtual_accounts_client.base_url}/dedicated_account?active=True&currency=NGN",
        json=mock_response,
        status=200,
    )

    data, meta = dedicated_virtual_accounts_client.list_dedicated_virtual_accounts(
        active=True, currency="NGN"
    )

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["account_number"] == "0123456789"
    assert meta == {}


@responses.activate
def test_fetch_dedicated_virtual_account(dedicated_virtual_accounts_client):
    dedicated_account_id = 123
    mock_response = {
        "status": True,
        "message": "Dedicated account retrieved",
        "data": {"id": dedicated_account_id, "account_number": "0123456789"},
    }
    responses.add(
        responses.GET,
        f"{dedicated_virtual_accounts_client.base_url}/dedicated_account/{dedicated_account_id}",
        json=mock_response,
        status=200,
    )

    data, meta = dedicated_virtual_accounts_client.fetch_dedicated_virtual_account(
        dedicated_account_id=dedicated_account_id
    )

    assert data["id"] == dedicated_account_id
    assert data["account_number"] == "0123456789"
    assert meta == {}


@responses.activate
def test_requery_dedicated_account(dedicated_virtual_accounts_client):
    payload = {
        "account_number": "0123456789",
        "provider_slug": "wema-bank",
    }
    mock_response = {
        "status": True,
        "message": "Dedicated account requery successful",
        "data": {"account_number": payload["account_number"]},
    }
    responses.add(
        responses.GET,
        f"{dedicated_virtual_accounts_client.base_url}/dedicated_account/requery",
        json=mock_response,
        status=200,
    )

    data, meta = dedicated_virtual_accounts_client.requery_dedicated_account(**payload)

    assert data["account_number"] == payload["account_number"]
    assert meta == {}


@responses.activate
def test_deactivate_dedicated_account(dedicated_virtual_accounts_client):
    dedicated_account_id = 123
    mock_response = {
        "status": True,
        "message": "Dedicated account deactivated",
        "data": {"id": dedicated_account_id},
    }
    responses.add(
        responses.DELETE,
        f"{dedicated_virtual_accounts_client.base_url}/dedicated_account/{dedicated_account_id}",
        json=mock_response,
        status=200,
    )

    data, meta = dedicated_virtual_accounts_client.deactivate_dedicated_account(
        dedicated_account_id=dedicated_account_id
    )

    assert data["id"] == dedicated_account_id
    assert meta == {}


@responses.activate
def test_split_dedicated_account_transaction(dedicated_virtual_accounts_client):
    payload = {
        "customer": "CUS_test",
        "split_code": "SPL_test",
    }
    mock_response = {
        "status": True,
        "message": "Dedicated account split successful",
        "data": {"customer": payload["customer"]},
    }
    responses.add(
        responses.POST,
        f"{dedicated_virtual_accounts_client.base_url}/dedicated_account/split",
        json=mock_response,
        status=200,
    )

    data, meta = dedicated_virtual_accounts_client.split_dedicated_account_transaction(**payload)

    assert data["customer"] == payload["customer"]
    assert meta == {}


@responses.activate
def test_remove_split_from_dedicated_account(dedicated_virtual_accounts_client):
    account_number = "0123456789"
    mock_response = {
        "status": True,
        "message": "Split removed from dedicated account",
        "data": {"account_number": account_number},
    }
    responses.add(
        responses.DELETE,
        f"{dedicated_virtual_accounts_client.base_url}/dedicated_account/split",
        json=mock_response,
        status=200,
    )

    data, meta = dedicated_virtual_accounts_client.remove_split_from_dedicated_account(
        account_number=account_number
    )

    assert data["account_number"] == account_number
    assert meta == {}


@responses.activate
def test_fetch_bank_providers(dedicated_virtual_accounts_client):
    mock_response = {
        "status": True,
        "message": "Bank providers retrieved",
        "data": [{"slug": "wema-bank", "name": "Wema Bank"}],
    }
    responses.add(
        responses.GET,
        f"{dedicated_virtual_accounts_client.base_url}/dedicated_account/available_providers",
        json=mock_response,
        status=200,
    )

    data, meta = dedicated_virtual_accounts_client.fetch_bank_providers()

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["slug"] == "wema-bank"
    assert meta == {}