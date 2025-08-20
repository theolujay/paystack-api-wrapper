import responses
import json

from tests.utils import assert_api_error_contains


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
def test_create_payment_request_with_all_params(payment_requests_client):
    payload = {
        "customer": "CUS_test_all",
        "amount": 50000,
        "due_date": "2024-01-31",
        "description": "Full payment request",
        "line_items": [{"name": "Item A", "amount": 25000, "quantity": 1}],
        "tax": [{"name": "VAT", "amount": 5000}],
        "currency": "USD",
        "send_notification": False,
        "draft": True,
        "has_invoice": True,
        "invoice_number": 12345,
        "split_code": "SPL_test_all",
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
    request = responses.calls[0].request
    request_payload = json.loads(request.body)
    assert request_payload["customer"] == payload["customer"]
    assert request_payload["amount"] == payload["amount"]
    assert request_payload["due_date"] == payload["due_date"]
    assert request_payload["description"] == payload["description"]
    assert request_payload["line_items"] == payload["line_items"]
    assert request_payload["tax"] == payload["tax"]
    assert request_payload["currency"] == payload["currency"]
    assert request_payload["send_notification"] == payload["send_notification"]
    assert request_payload["draft"] == payload["draft"]
    assert request_payload["has_invoice"] == payload["has_invoice"]
    assert request_payload["invoice_number"] == payload["invoice_number"]
    assert request_payload["split_code"] == payload["split_code"]


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
def test_list_payment_requests_with_all_params(payment_requests_client):
    mock_response = {
        "status": True,
        "message": "Payment requests retrieved",
        "data": [{"id": 1, "status": "pending"}],
    }
    responses.add(
        responses.GET,
        f"{payment_requests_client.base_url}/paymentrequest",
        json=mock_response,
        status=200,
    )
    params = {
        "per_page": 5,
        "page": 2,
        "customer": "CUS_all_params",
        "status": "pending",
        "currency": "GHS",
        "include_archive": "true",
        "from_date": "2023-01-01",
        "to_date": "2023-12-31",
    }
    data, meta = payment_requests_client.list_payment_requests(**params)

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["status"] == "pending"
    assert meta == {}
    request = responses.calls[0].request
    assert request.method == "GET"
    assert "perPage=5" in request.url
    assert "page=2" in request.url
    assert "customer=CUS_all_params" in request.url
    assert "status=pending" in request.url
    assert "currency=GHS" in request.url
    assert "include_archive=true" in request.url
    assert "from=2023-01-01" in request.url
    assert "to=2023-12-31" in request.url


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
def test_finalize_payment_request_with_send_notification_false(payment_requests_client):
    code = "REQ_test_notify_false"
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

    data, meta = payment_requests_client.finalize_payment_request(
        code=code, send_notification=False
    )

    assert data["code"] == code
    assert data["status"] == "finalized"
    assert meta == {}
    request = responses.calls[0].request
    request_payload = json.loads(request.body)
    assert request_payload["send_notification"] is False


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

    data, meta = payment_requests_client.update_payment_request(
        id_or_code=id_or_code, **payload
    )

    assert data["code"] == id_or_code
    assert data["description"] == payload["description"]
    assert meta == {}


@responses.activate
def test_update_payment_request_with_all_params(payment_requests_client):
    id_or_code = "REQ_test_update_all"
    payload = {
        "customer": "CUS_updated",
        "amount": 30000,
        "due_date": "2024-02-29",
        "description": "Updated full payment request",
        "line_items": [{"name": "Item B", "amount": 15000}],
        "tax": [{"name": "GST", "amount": 3000}],
        "currency": "EUR",
        "send_notification": True,
        "draft": False,
        "invoice_number": 54321,
        "split_code": "SPL_updated",
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

    data, meta = payment_requests_client.update_payment_request(
        id_or_code=id_or_code, **payload
    )

    assert data["code"] == id_or_code
    assert data["description"] == payload["description"]
    assert meta == {}
    request = responses.calls[0].request
    request_payload = json.loads(request.body)
    assert request_payload["customer"] == payload["customer"]
    assert request_payload["amount"] == payload["amount"]
    assert request_payload["due_date"] == payload["due_date"]
    assert request_payload["description"] == payload["description"]
    assert request_payload["line_items"] == payload["line_items"]
    assert request_payload["tax"] == payload["tax"]
    assert request_payload["currency"] == payload["currency"]
    assert request_payload["send_notification"] == payload["send_notification"]
    assert request_payload["draft"] == payload["draft"]
    assert request_payload["invoice_number"] == payload["invoice_number"]
    assert request_payload["split_code"] == payload["split_code"]


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
