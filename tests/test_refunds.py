import pytest
import responses
from api.exceptions import APIError
from api.refunds import RefundsAPI

from .utils import assert_api_error_contains


@responses.activate
def test_create_refund(refunds_client):
    payload = {
        "transaction": "TRN_test",
        "amount": 10000,
    }
    mock_response = {
        "status": True,
        "message": "Refund created",
        "data": {"transaction": payload["transaction"], "amount": payload["amount"]},
    }
    responses.add(
        responses.POST,
        f"{refunds_client.base_url}/refund",
        json=mock_response,
        status=200,
    )

    data, meta = refunds_client.create(**payload)

    assert data["transaction"] == payload["transaction"]
    assert data["amount"] == payload["amount"]
    assert meta == {}


@responses.activate
def test_create_refund_invalid_amount(refunds_client):
    payload = {
        "transaction": "TRN_test",
        "amount": 0,
    }
    with pytest.raises(APIError):
        refunds_client.create(**payload)


@responses.activate
def test_create_refund_invalid_key(refunds_client):
    payload = {
        "transaction": "TRN_test",
        "amount": 10000,
    }
    mock_response = {"status": False, "message": "Invalid API key"}
    responses.add(
        responses.POST,
        f"{refunds_client.base_url}/refund",
        json=mock_response,
        status=401,
    )
    assert_api_error_contains(refunds_client.create, "Invalid API key", **payload)


@responses.activate
def test_list_refunds(refunds_client):
    transaction = "TRN_test"
    currency = "NGN"
    mock_response = {
        "status": True,
        "message": "Refunds retrieved",
        "data": [{"id": 1, "transaction": transaction}],
    }
    responses.add(
        responses.GET,
        f"{refunds_client.base_url}/refund",
        json=mock_response,
        status=200,
    )

    data, meta = refunds_client.list_refunds(transaction=transaction, currency=currency)

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["transaction"] == transaction
    assert meta == {}


@responses.activate
def test_list_refunds_invalid_per_page(refunds_client):
    transaction = "TRN_test"
    currency = "NGN"
    with pytest.raises(APIError):
        refunds_client.list_refunds(transaction=transaction, currency=currency, per_page=0)


@responses.activate
def test_fetch_refund(refunds_client):
    refund_id = 123
    mock_response = {
        "status": True,
        "message": "Refund retrieved",
        "data": {"id": refund_id, "status": "successful"},
    }
    responses.add(
        responses.GET,
        f"{refunds_client.base_url}/refund/{refund_id}",
        json=mock_response,
        status=200,
    )

    data, meta = refunds_client.fetch(refund_id=refund_id)

    assert data["id"] == refund_id
    assert data["status"] == "successful"
    assert meta == {}