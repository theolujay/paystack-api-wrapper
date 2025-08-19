import responses

from .utils import assert_api_error_contains

@responses.activate
def test_initiate_bulk_charge(bulk_charges_client):
    charges = [
        {"authorization": "AUTH_test1", "amount": 10000, "reference": "ref1"},
        {"authorization": "AUTH_test2", "amount": 20000, "reference": "ref2"},
    ]
    mock_response = {
        "status": True,
        "message": "Bulk charge initiated",
        "data": {"batch_code": "BULK_test"},
    }
    responses.add(
        responses.POST,
        f"{bulk_charges_client.base_url}/bulkcharge",
        json=mock_response,
        status=200,
    )

    data, meta = bulk_charges_client.initiate_bulk_charge(charges=charges)

    assert data["batch_code"] == "BULK_test"
    assert meta == {}


@responses.activate
def test_initiate_bulk_charge_invalid_key(bulk_charges_client):
    charges = [
        {"authorization": "AUTH_test1", "amount": 10000, "reference": "ref1"},
    ]
    mock_response = {"status": False, "message": "Invalid API key"}
    responses.add(
        responses.POST,
        f"{bulk_charges_client.base_url}/bulkcharge",
        json=mock_response,
        status=401,
    )
    assert_api_error_contains(
        bulk_charges_client.initiate_bulk_charge, "Invalid API key", charges=charges
    )


@responses.activate
def test_list_bulk_charge_batches(bulk_charges_client):
    mock_response = {
        "status": True,
        "message": "Bulk charge batches retrieved",
        "data": [{"batch_code": "BULK_test1"}, {"batch_code": "BULK_test2"}],
    }
    responses.add(
        responses.GET,
        f"{bulk_charges_client.base_url}/bulkcharge",
        json=mock_response,
        status=200,
    )

    data, meta = bulk_charges_client.list_bulk_charge_batches()

    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["batch_code"] == "BULK_test1"
    assert meta == {}


@responses.activate
def test_list_bulk_charge_batches_with_params(bulk_charges_client):
    mock_response = {
        "status": True,
        "message": "Bulk charge batches retrieved",
        "data": [{"batch_code": "BULK_test1"}],
    }
    responses.add(
        responses.GET,
        f"{bulk_charges_client.base_url}/bulkcharge?perPage=1&page=1",
        json=mock_response,
        status=200,
    )

    data, meta = bulk_charges_client.list_bulk_charge_batches(per_page=1, page=1)

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["batch_code"] == "BULK_test1"
    assert meta == {}


@responses.activate
def test_list_bulk_charge_batches_invalid_key(bulk_charges_client):
    mock_response = {"status": False, "message": "Invalid API key"}
    responses.add(
        responses.GET,
        f"{bulk_charges_client.base_url}/bulkcharge",
        json=mock_response,
        status=401,
    )
    assert_api_error_contains(bulk_charges_client.list_bulk_charge_batches, "Invalid API key")


@responses.activate
def test_fetch_bulk_charge_batch(bulk_charges_client):
    id_or_code = "BULK_test"
    mock_response = {
        "status": True,
        "message": "Bulk charge batch retrieved",
        "data": {"batch_code": id_or_code, "total_charges": 10, "pending_charges": 5},
    }
    responses.add(
        responses.GET,
        f"{bulk_charges_client.base_url}/bulkcharge/{id_or_code}",
        json=mock_response,
        status=200,
    )

    data, meta = bulk_charges_client.fetch_bulk_charge_batch(id_or_code=id_or_code)

    assert data["batch_code"] == id_or_code
    assert data["total_charges"] == 10
    assert meta == {}


@responses.activate
def test_fetch_bulk_charge_batch_invalid_key(bulk_charges_client):
    id_or_code = "BULK_test"
    mock_response = {"status": False, "message": "Invalid API key"}
    responses.add(
        responses.GET,
        f"{bulk_charges_client.base_url}/bulkcharge/{id_or_code}",
        json=mock_response,
        status=401,
    )
    assert_api_error_contains(
        bulk_charges_client.fetch_bulk_charge_batch, "Invalid API key", id_or_code=id_or_code
    )


@responses.activate
def test_fetch_charges_in_batch(bulk_charges_client):
    id_or_code = "BULK_test"
    mock_response = {
        "status": True,
        "message": "Charges in batch retrieved",
        "data": [{"reference": "ref1"}, {"reference": "ref2"}],
    }
    responses.add(
        responses.GET,
        f"{bulk_charges_client.base_url}/bulkcharge/{id_or_code}/charges",
        json=mock_response,
        status=200,
    )

    data, meta = bulk_charges_client.fetch_charges_in_batch(id_or_code=id_or_code)

    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["reference"] == "ref1"
    assert meta == {}


@responses.activate
def test_fetch_charges_in_batch_with_params(bulk_charges_client):
    id_or_code = "BULK_test"
    mock_response = {
        "status": True,
        "message": "Charges in batch retrieved",
        "data": [{"reference": "ref1"}],
    }
    responses.add(
        responses.GET,
        f"{bulk_charges_client.base_url}/bulkcharge/{id_or_code}/charges?status=success&perPage=1",
        json=mock_response,
        status=200,
    )

    data, meta = bulk_charges_client.fetch_charges_in_batch(
        id_or_code=id_or_code, status="success", per_page=1
    )

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["reference"] == "ref1"
    assert meta == {}


@responses.activate
def test_fetch_charges_in_batch_invalid_key(bulk_charges_client):
    id_or_code = "BULK_test"
    mock_response = {"status": False, "message": "Invalid API key"}
    responses.add(
        responses.GET,
        f"{bulk_charges_client.base_url}/bulkcharge/{id_or_code}/charges",
        json=mock_response,
        status=401,
    )
    assert_api_error_contains(
        bulk_charges_client.fetch_charges_in_batch, "Invalid API key", id_or_code=id_or_code
    )


@responses.activate
def test_pause_bulk_charge_batch(bulk_charges_client):
    batch_code = "BULK_test"
    mock_response = {
        "status": True,
        "message": "Bulk charge batch paused",
        "data": {"batch_code": batch_code},
    }
    responses.add(
        responses.GET,
        f"{bulk_charges_client.base_url}/bulkcharge/pause/{batch_code}",
        json=mock_response,
        status=200,
    )

    data, meta = bulk_charges_client.pause_bulk_charge_batch(batch_code=batch_code)

    assert data["batch_code"] == batch_code
    assert meta == {}


@responses.activate
def test_pause_bulk_charge_batch_invalid_key(bulk_charges_client):
    batch_code = "BULK_test"
    mock_response = {"status": False, "message": "Invalid API key"}
    responses.add(
        responses.GET,
        f"{bulk_charges_client.base_url}/bulkcharge/pause/{batch_code}",
        json=mock_response,
        status=401,
    )
    assert_api_error_contains(
        bulk_charges_client.pause_bulk_charge_batch, "Invalid API key", batch_code=batch_code
    )


@responses.activate
def test_resume_bulk_charge_batch(bulk_charges_client):
    batch_code = "BULK_test"
    mock_response = {
        "status": True,
        "message": "Bulk charge batch resumed",
        "data": {"batch_code": batch_code},
    }
    responses.add(
        responses.GET,
        f"{bulk_charges_client.base_url}/bulkcharge/resume/{batch_code}",
        json=mock_response,
        status=200,
    )

    data, meta = bulk_charges_client.resume_bulk_charge_batch(batch_code=batch_code)

    assert data["batch_code"] == batch_code
    assert meta == {}


@responses.activate
def test_resume_bulk_charge_batch_invalid_key(bulk_charges_client):
    batch_code = "BULK_test"
    mock_response = {"status": False, "message": "Invalid API key"}
    responses.add(
        responses.GET,
        f"{bulk_charges_client.base_url}/bulkcharge/resume/{batch_code}",
        json=mock_response,
        status=401,
    )
    assert_api_error_contains(
        bulk_charges_client.resume_bulk_charge_batch, "Invalid API key", batch_code=batch_code
    )