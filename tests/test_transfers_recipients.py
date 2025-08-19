import pytest
import responses
from api.exceptions import AuthenticationError
from api.transfers_recipients import TransferRecipientsAPI

from .utils import assert_api_error_contains


@responses.activate
def test_create_transfer_recipient(transfer_recipients_client):
    payload = {
        "type": "nuban",
        "name": "Test Recipient",
        "account_number": "0123456789",
        "bank_code": "044",
    }
    mock_response = {
        "status": True,
        "message": "Recipient created",
        "data": {"name": payload["name"], "recipient_code": "RCP_test"},
    }
    responses.add(
        responses.POST,
        f"{transfer_recipients_client.base_url}/transferrecipient",
        json=mock_response,
        status=200,
    )

    data, meta = transfer_recipients_client.create_transfer_recipient(**payload)

    assert data["name"] == payload["name"]
    assert data["recipient_code"] == "RCP_test"
    assert meta == {}


@responses.activate
def test_create_transfer_recipient_invalid_key(transfer_recipients_client):
    payload = {
        "type": "nuban",
        "name": "Test Recipient",
        "account_number": "0123456789",
        "bank_code": "044",
    }
    mock_response = {"status": False, "message": "Invalid API key"}
    responses.add(
        responses.POST,
        f"{transfer_recipients_client.base_url}/transferrecipient",
        json=mock_response,
        status=401,
    )
    assert_api_error_contains(
        transfer_recipients_client.create_transfer_recipient, "Invalid API key", **payload
    )


@responses.activate
def test_bulk_create_transfer_recipient(transfer_recipients_client):
    batch = [
        {"type": "nuban", "name": "Recipient 1", "account_number": "0123", "bank_code": "044"},
        {"type": "nuban", "name": "Recipient 2", "account_number": "0456", "bank_code": "044"},
    ]
    mock_response = {
        "status": True,
        "message": "Recipients created",
        "data": {"success": 2, "failures": 0},
    }
    responses.add(
        responses.POST,
        f"{transfer_recipients_client.base_url}/transferrecipient/bulk",
        json=mock_response,
        status=200,
    )

    data, meta = transfer_recipients_client.bulk_create_transfer_recipient(batch=batch)

    assert data["success"] == 2
    assert meta == {}


@responses.activate
def test_list_transfer_recipients(transfer_recipients_client):
    mock_response = {
        "status": True,
        "message": "Recipients retrieved",
        "data": [{"name": "Recipient 1"}, {"name": "Recipient 2"}],
    }
    responses.add(
        responses.GET,
        f"{transfer_recipients_client.base_url}/transferrecipient",
        json=mock_response,
        status=200,
    )

    data, meta = transfer_recipients_client.list_transfer_recipients()

    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["name"] == "Recipient 1"
    assert meta == {}


@responses.activate
def test_list_transfer_recipients_with_params(transfer_recipients_client):
    mock_response = {
        "status": True,
        "message": "Recipients retrieved",
        "data": [{"name": "Recipient 1"}],
    }
    responses.add(
        responses.GET,
        f"{transfer_recipients_client.base_url}/transferrecipient?perPage=1&page=1",
        json=mock_response,
        status=200,
    )

    data, meta = transfer_recipients_client.list_transfer_recipients(per_page=1, page=1)

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["name"] == "Recipient 1"
    assert meta == {}


@responses.activate
def test_fetch_transfer_recipient(transfer_recipients_client):
    id_or_code = "RCP_test"
    mock_response = {
        "status": True,
        "message": "Recipient retrieved",
        "data": {"name": "Test Recipient", "recipient_code": id_or_code},
    }
    responses.add(
        responses.GET,
        f"{transfer_recipients_client.base_url}/transferrecipient/{id_or_code}",
        json=mock_response,
        status=200,
    )

    data, meta = transfer_recipients_client.fetch_transfer_recipient(id_or_code=id_or_code)

    assert data["name"] == "Test Recipient"
    assert data["recipient_code"] == id_or_code
    assert meta == {}


@responses.activate
def test_update_transfer_recipient(transfer_recipients_client):
    id_or_code = "RCP_test"
    payload = {
        "name": "Updated Recipient Name",
        "email": "updated@example.com",
    }
    mock_response = {
        "status": True,
        "message": "Recipient updated",
        "data": {"name": payload["name"], "recipient_code": id_or_code},
    }
    responses.add(
        responses.PUT,
        f"{transfer_recipients_client.base_url}/transferrecipient/{id_or_code}",
        json=mock_response,
        status=200,
    )

    data, meta = transfer_recipients_client.update_transfer_recipient(id_or_code=id_or_code, **payload)

    assert data["name"] == payload["name"]
    assert data["recipient_code"] == id_or_code
    assert meta == {}


@responses.activate
def test_delete_transfer_recipient(transfer_recipients_client):
    id_or_code = "RCP_test"
    mock_response = {
        "status": True,
        "message": "Recipient deleted",
        "data": {"recipient_code": id_or_code},
    }
    responses.add(
        responses.DELETE,
        f"{transfer_recipients_client.base_url}/transferrecipient/{id_or_code}",
        json=mock_response,
        status=200,
    )

    data, meta = transfer_recipients_client.delete_transfer_recipient(id_or_code=id_or_code)

    assert data["recipient_code"] == id_or_code
    assert meta == {}