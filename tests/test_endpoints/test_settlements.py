import responses


@responses.activate
def test_list_settlements(settlements_client):
    mock_response = {
        "status": True,
        "message": "Settlements retrieved",
        "data": [{"id": 1, "status": "success"}, {"id": 2, "status": "pending"}],
    }
    responses.add(
        responses.GET,
        f"{settlements_client.base_url}/settlement",
        json=mock_response,
        status=200,
    )

    data, meta = settlements_client.list_settlements()

    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["status"] == "success"
    assert meta == {}


@responses.activate
def test_list_settlements_with_params(settlements_client):
    mock_response = {
        "status": True,
        "message": "Settlements retrieved",
        "data": [{"id": 1, "status": "success"}],
    }
    responses.add(
        responses.GET,
        f"{settlements_client.base_url}/settlement?perPage=1&page=1&status=success",
        json=mock_response,
        status=200,
    )

    data, meta = settlements_client.list_settlements(
        per_page=1, page=1, status="success"
    )

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["status"] == "success"
    assert meta == {}


@responses.activate
def test_list_settlement_transactions(settlements_client):
    settlement_id = "SET_test"
    mock_response = {
        "status": True,
        "message": "Settlement transactions retrieved",
        "data": [{"id": 1, "amount": 1000}, {"id": 2, "amount": 2000}],
    }
    responses.add(
        responses.GET,
        f"{settlements_client.base_url}/settlement/{settlement_id}/transactions",
        json=mock_response,
        status=200,
    )

    data, meta = settlements_client.list_settlement_transactions(
        settlement_id=settlement_id
    )

    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["amount"] == 1000
    assert meta == {}


@responses.activate
def test_list_settlement_transactions_with_params(settlements_client):
    settlement_id = "SET_test"
    mock_response = {
        "status": True,
        "message": "Settlement transactions retrieved",
        "data": [{"id": 1, "amount": 1000}],
    }
    responses.add(
        responses.GET,
        f"{settlements_client.base_url}/settlement/{settlement_id}/transactions?perPage=1&page=1",
        json=mock_response,
        status=200,
    )

    data, meta = settlements_client.list_settlement_transactions(
        settlement_id=settlement_id, per_page=1, page=1
    )

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["amount"] == 1000
    assert meta == {}
