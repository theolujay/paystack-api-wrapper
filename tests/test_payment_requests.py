import pytest
import responses
from paystack_client.exceptions import APIError
from paystack_client.payment_requests import PaymentRequestsAPI


from .utils import assert_api_error_contains


@responses.activate
def test_create_payment_request(payment_requests_client):
    payload = {
        "customer": "CUS_test",
        "amount": 10000,
        "due_date": "2023-12-31",
    }
    mock_response = {
        "status": True,
        "message": "Payment request created",
        "data": {"customer": payload["customer"], "amount": payload["amount"]},
    }
    responses.add(
        responses.POST,
        f"{payment_requests_client.base_url}/paymentrequest",
        json=mock_response,
        status=200,
    )

    data, meta = payment_requests_client.create_payment_request(**payload)

    assert data["customer"] == payload["customer"]
    assert data["amount"] == payload["amount"]
    assert meta == {}


@responses.activate
def test_create_payment_request_invalid_key(payment_requests_client):
    payload = {
        "customer": "CUS_test",
        "amount": 10000,
        "due_date": "2023-12-31",
    }
    mock_response = {"status": False, "message": "Invalid API key"}
    responses.add(
        responses.POST,
        f"{payment_requests_client.base_url}/paymentrequest",
        json=mock_response,
        status=401,
    )
    assert_api_error_contains(
        payment_requests_client.create_payment_request, "Invalid API key", **payload
    )


@responses.activate
def test_list_payment_requests(payment_requests_client):
    mock_response = {
        "status": True,
        "message": "Payment requests retrieved",
        "data": [{"id": 1, "status": "pending"}, {"id": 2, "status": "paid"}],
    }
    responses.add(
        responses.GET,
        f"{payment_requests_client.base_url}/paymentrequest",
        json=mock_response,
        status=200,
    )

    data, meta = payment_requests_client.list_payment_requests()

    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["status"] == "pending"
    assert meta == {}


@responses.activate
def test_list_payment_requests_with_params(payment_requests_client):
    mock_response = {
        "status": True,
        "message": "Payment requests retrieved",
        "data": [{"id": 1, "status": "pending"}],
    }
    responses.add(
        responses.GET,
        f"{payment_requests_client.base_url}/paymentrequest?perPage=1&page=1",
        json=mock_response,
        status=200,
    )

    data, meta = payment_requests_client.list_payment_requests(per_page=1, page=1)

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["status"] == "pending"
    assert meta == {}


@responses.activate
def test_fetch_payment_request(payment_requests_client):
    id_or_code = "REQ_test"
    mock_response = {
        "status": True,
        "message": "Payment request retrieved",
        "data": {"id": 1, "code": id_or_code},
    }
    responses.add(
        responses.GET,
        f"{payment_requests_client.base_url}/paymentrequest/{id_or_code}",
        json=mock_response,
        status=200,
    )

    data, meta = payment_requests_client.fetch_payment_request(id_or_code=id_or_code)

    assert data["code"] == id_or_code
    assert meta == {}


@responses.activate
def test_verify_payment_request(payment_requests_client):
    code = "REQ_test"
    mock_response = {
        "status": True,
        "message": "Payment request verified",
        "data": {"code": code, "status": "paid"},
    }
    responses.add(
        responses.GET,
        f"{payment_requests_client.base_url}/paymentrequest/verify/{code}",
        json=mock_response,
        status=200,
    )

    data, meta = payment_requests_client.verify_payment_request(code=code)

    assert data["code"] == code
    assert data["status"] == "paid"
    assert meta == {}


@responses.activate
def test_send_notification(payment_requests_client):
    code = "REQ_test"
    mock_response = {
        "status": True,
        "message": "Notification sent",
        "data": {"code": code},

    }
    responses.add(
        responses.POST,
        f"{payment_requests_client.base_url}/paymentrequest/notify/{code}",
        json=mock_response,
        status=200,
    )

    data, meta = payment_requests_client.send_notification(code=code)

    assert data["code"] == code
    assert meta == {}


@responses.activate
def test_payment_request_total(payment_requests_client):
    mock_response = {
        "status": True,
        "message": "Payment request totals retrieved",
        "data": {"total_requests": 100, "total_amount": 1000000},
    }
    responses.add(
        responses.GET,
        f"{payment_requests_client.base_url}/paymentrequest/totals",
        json=mock_response,
        status=200,
    )

    data, meta = payment_requests_client.payment_request_total()

    assert data["total_requests"] == 100
    assert data["total_amount"] == 1000000
    assert meta == {}


@responses.activate
def test_finalize_payment_request(payment_requests_client):
    code = "REQ_test"
    mock_response = {
        "status": True,
        "message": "Payment request finalized",
        "data": {"code": code, "status": "finalized"},
    }
    responses.add(
        responses.POST,
        f"{payment_requests_client.base_url}/paymentrequest/finalize/{code}",
        json=mock_response,
        status=200,
    )

    data, meta = payment_requests_client.finalize_payment_request(code=code)

    assert data["code"] == code
    assert data["status"] == "finalized"
    assert meta == {}


@responses.activate
def test_update_payment_request(payment_requests_client):
    id_or_code = "REQ_test"
    payload = {
        "description": "Updated description",
        "amount": 20000,
    }
    mock_response = {
        "status": True,
        "message": "Payment request updated",
        "data": {"code": id_or_code, "description": payload["description"]},
    }
    responses.add(
        responses.PUT,
        f"{payment_requests_client.base_url}/paymentrequest/{id_or_code}",
        json=mock_response,
        status=200,
    )

    data, meta = payment_requests_client.update_payment_request(id_or_code=id_or_code, **payload)

    assert data["code"] == id_or_code
    assert data["description"] == payload["description"]
    assert meta == {}


@responses.activate
def test_archive_payment_request(payment_requests_client):
    code = "REQ_test"
    mock_response = {
        "status": True,
        "message": "Payment request archived",
        "data": {"code": code, "status": "archived"},
    }
    responses.add(
        responses.POST,
        f"{payment_requests_client.base_url}/paymentrequest/archive/{code}",
        json=mock_response,
        status=200,
    )

    data, meta = payment_requests_client.archive_payment_request(code=code)

    assert data["code"] == code
    assert data["status"] == "archived"
    assert meta == {}