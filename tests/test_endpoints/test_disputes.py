import responses


from tests.utils import assert_api_error_contains


@responses.activate
def test_list_disputes(disputes_client):
    from_date = "2023-01-01"
    to_date = "2023-01-31"
    mock_response = {
        "status": True,
        "message": "Disputes retrieved",
        "data": [{"id": 1, "status": "pending"}, {"id": 2, "status": "resolved"}],
    }
    responses.add(
        responses.GET,
        f"{disputes_client.base_url}/dispute",
        json=mock_response,
        status=200,
    )

    data, meta = disputes_client.list_disputes(from_date=from_date, to_date=to_date)

    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["status"] == "pending"
    assert meta == {}


@responses.activate
def test_list_disputes_with_all_params(disputes_client):
    from_date = "2023-01-01"
    to_date = "2023-01-31"
    mock_response = {
        "status": True,
        "message": "Disputes retrieved",
        "data": [{"id": 1, "status": "pending"}],
    }
    responses.add(
        responses.GET,
        f"{disputes_client.base_url}/dispute?from=2023-01-01&to=2023-01-31&perPage=1&page=1&transaction=TRN_test&status=pending",
        json=mock_response,
        status=200,
    )

    data, meta = disputes_client.list_disputes(
        from_date=from_date,
        to_date=to_date,
        per_page=1,
        page=1,
        transaction_id="TRN_test",
        status="pending",
    )

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["status"] == "pending"
    assert meta == {}


@responses.activate
def test_fetch_dispute(disputes_client):
    dispute_id = "DIS_test"
    mock_response = {
        "status": True,
        "message": "Dispute retrieved",
        "data": {"id": dispute_id, "status": "pending"},
    }
    responses.add(
        responses.GET,
        f"{disputes_client.base_url}/dispute/{dispute_id}",
        json=mock_response,
        status=200,
    )

    data, meta = disputes_client.fetch_dispute(dispute_id=dispute_id)

    assert data["id"] == dispute_id
    assert data["status"] == "pending"
    assert meta == {}


@responses.activate
def test_list_transaction_disputes(disputes_client):
    transaction_id = "TRN_test"
    mock_response = {
        "status": True,
        "message": "Transaction disputes retrieved",
        "data": [{"id": 1, "transaction_id": transaction_id}],
    }
    responses.add(
        responses.GET,
        f"{disputes_client.base_url}/dispute/transaction/{transaction_id}",
        json=mock_response,
        status=200,
    )

    data, meta = disputes_client.list_transaction_disputes(
        transaction_id=transaction_id
    )

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["transaction_id"] == transaction_id
    assert meta == {}


@responses.activate
def test_update_dispute(disputes_client):
    dispute_id = "DIS_test"
    refund_amount = 1000
    mock_response = {
        "status": True,
        "message": "Dispute updated",
        "data": {"id": dispute_id, "refund_amount": refund_amount},
    }
    responses.add(
        responses.PUT,
        f"{disputes_client.base_url}/dispute/{dispute_id}",
        json=mock_response,
        status=200,
    )

    data, meta = disputes_client.update_dispute(
        dispute_id=dispute_id, refund_amount=refund_amount
    )

    assert data["id"] == dispute_id
    assert data["refund_amount"] == refund_amount
    assert meta == {}


@responses.activate
def test_update_dispute_with_uploaded_filename(disputes_client):
    dispute_id = "DIS_test_file"
    refund_amount = 1000
    uploaded_filename = "test_file.pdf"
    mock_response = {
        "status": True,
        "message": "Dispute updated",
        "data": {"id": dispute_id, "refund_amount": refund_amount},
    }
    responses.add(
        responses.PUT,
        f"{disputes_client.base_url}/dispute/{dispute_id}",
        json=mock_response,
        status=200,
    )

    data, meta = disputes_client.update_dispute(
        dispute_id=dispute_id,
        refund_amount=refund_amount,
        uploaded_filename=uploaded_filename,
    )

    assert data["id"] == dispute_id
    assert data["refund_amount"] == refund_amount
    assert meta == {}


@responses.activate
def test_add_evidence(disputes_client):
    dispute_id = "DIS_test"
    payload = {
        "customer_email": "customer@example.com",
        "customer_name": "John Doe",
        "customer_phone": "08012345678",
        "service_details": "Product delivered",
    }
    mock_response = {
        "status": True,
        "message": "Evidence added",
        "data": {"dispute_id": dispute_id},
    }
    responses.add(
        responses.POST,
        f"{disputes_client.base_url}/dispute/{dispute_id}/evidence",
        json=mock_response,
        status=200,
    )

    data, meta = disputes_client.add_evidence(dispute_id=dispute_id, **payload)

    assert data["dispute_id"] == dispute_id
    assert meta == {}


@responses.activate
def test_add_evidence_with_optional_params(disputes_client):
    dispute_id = "DIS_test_optional"
    payload = {
        "customer_email": "customer_opt@example.com",
        "customer_name": "Jane Doe",
        "customer_phone": "09012345678",
        "service_details": "Service provided",
        "delivery_address": "123 Main St",
        "delivery_date": "2023-01-01",
    }
    mock_response = {
        "status": True,
        "message": "Evidence added",
        "data": {"dispute_id": dispute_id},
    }
    responses.add(
        responses.POST,
        f"{disputes_client.base_url}/dispute/{dispute_id}/evidence",
        json=mock_response,
        status=200,
    )

    data, meta = disputes_client.add_evidence(dispute_id=dispute_id, **payload)

    assert data["dispute_id"] == dispute_id
    assert meta == {}


@responses.activate
def test_get_upload_url(disputes_client):
    dispute_id = "DIS_test"
    upload_filename = "evidence.pdf"
    mock_response = {
        "status": True,
        "message": "Upload URL retrieved",
        "data": {"upload_url": "http://example.com/upload"},
    }
    responses.add(
        responses.GET,
        f"{disputes_client.base_url}/dispute/{dispute_id}/upload_url",
        json=mock_response,
        status=200,
    )

    data, meta = disputes_client.get_upload_url(
        dispute_id=dispute_id, upload_filename=upload_filename
    )

    assert data["upload_url"] == "http://example.com/upload"
    assert meta == {}


@responses.activate
def test_resolve_dispute(disputes_client):
    dispute_id = "DIS_test"
    payload = {
        "resolution": "merchant-accepted",
        "message": "Refund issued",
        "refund_amount": 1000,
        "uploaded_filename": "evidence.pdf",
    }
    mock_response = {
        "status": True,
        "message": "Dispute resolved",
        "data": {"id": dispute_id},
    }
    responses.add(
        responses.PUT,
        f"{disputes_client.base_url}/dispute/{dispute_id}/resolve",
        json=mock_response,
        status=200,
    )

    data, meta = disputes_client.resolve_dispute(dispute_id=dispute_id, **payload)

    assert data["id"] == dispute_id
    assert meta == {}


@responses.activate
def test_resolve_dispute_with_evidence(disputes_client):
    dispute_id = "DIS_test_evidence"
    payload = {
        "resolution": "merchant-accepted",
        "message": "Refund issued",
        "refund_amount": 1000,
        "uploaded_filename": "evidence.pdf",
        "evidence": 123,
    }
    mock_response = {
        "status": True,
        "message": "Dispute resolved",
        "data": {"id": dispute_id},
    }
    responses.add(
        responses.PUT,
        f"{disputes_client.base_url}/dispute/{dispute_id}/resolve",
        json=mock_response,
        status=200,
    )

    data, meta = disputes_client.resolve_dispute(dispute_id=dispute_id, **payload)

    assert data["id"] == dispute_id
    assert meta == {}


@responses.activate
def test_export_disputes(disputes_client):
    from_date = "2023-01-01"
    to_date = "2023-01-31"
    mock_response = {
        "status": True,
        "message": "Disputes exported",
        "data": {"url": "http://example.com/export"},
    }
    responses.add(
        responses.GET,
        f"{disputes_client.base_url}/dispute/export",
        json=mock_response,
        status=200,
    )

    data, meta = disputes_client.export_disputes(from_date=from_date, to_date=to_date)

    assert data["url"] == "http://example.com/export"
    assert meta == {}


@responses.activate
def test_export_disputes_with_all_params(disputes_client):
    from_date = "2023-01-01"
    to_date = "2023-01-31"
    mock_response = {
        "status": True,
        "message": "Disputes exported",
        "data": {"url": "http://example.com/export"},
    }
    responses.add(
        responses.GET,
        f"{disputes_client.base_url}/dispute/export?from=2023-01-01&to=2023-01-31&perPage=10&page=1&transaction=TRN_export&status=resolved",
        json=mock_response,
        status=200,
    )

    data, meta = disputes_client.export_disputes(
        from_date=from_date,
        to_date=to_date,
        per_page=10,
        page=1,
        transaction_id="TRN_export",
        status="resolved",
    )

    assert data["url"] == "http://example.com/export"
    assert meta == {}
