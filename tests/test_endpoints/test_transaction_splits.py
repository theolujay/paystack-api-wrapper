import responses


from tests.utils import assert_api_error_contains


@responses.activate
def test_create_split(transaction_splits_client):
    payload = {
        "name": "Test Split",
        "type": "percentage",
        "currency": "NGN",
        "subaccounts": [{"subaccount": "ACT_test1", "share": 50}],
        "bearer_type": "account",
    }
    mock_response = {
        "status": True,
        "message": "Split created",
        "data": {"name": payload["name"], "split_code": "SPL_test"},
    }
    responses.add(
        responses.POST,
        f"{transaction_splits_client.base_url}/split",
        json=mock_response,
        status=200,
    )

    data, meta = transaction_splits_client.create_split(**payload)

    assert data["name"] == payload["name"]
    assert data["split_code"] == "SPL_test"
    assert meta == {}


@responses.activate
def test_create_split_with_bearer_subaccount(transaction_splits_client):
    payload = {
        "name": "Test Split with Bearer Subaccount",
        "type": "percentage",
        "currency": "NGN",
        "subaccounts": [{"subaccount": "ACT_test1", "share": 50}],
        "bearer_type": "subaccount",
        "bearer_subaccount": "ACT_bearer",
    }
    mock_response = {
        "status": True,
        "message": "Split created",
        "data": {"name": payload["name"], "split_code": "SPL_test_bearer"},
    }
    responses.add(
        responses.POST,
        f"{transaction_splits_client.base_url}/split",
        json=mock_response,
        status=200,
    )

    data, meta = transaction_splits_client.create_split(**payload)

    assert data["name"] == payload["name"]
    assert data["split_code"] == "SPL_test_bearer"
    assert meta == {}


@responses.activate
def test_create_split_invalid_key(transaction_splits_client):
    payload = {
        "name": "Test Split",
        "type": "percentage",
        "currency": "NGN",
        "subaccounts": [{"subaccount": "ACT_test1", "share": 50}],
        "bearer_type": "account",
    }
    mock_response = {"status": False, "message": "Invalid API key"}
    responses.add(
        responses.POST,
        f"{transaction_splits_client.base_url}/split",
        json=mock_response,
        status=401,
    )
    assert_api_error_contains(
        transaction_splits_client.create_split, "Invalid API key", **payload
    )


@responses.activate
def test_list_splits(transaction_splits_client):
    mock_response = {
        "status": True,
        "message": "Splits retrieved",
        "data": [{"name": "Split 1"}, {"name": "Split 2"}],
    }
    responses.add(
        responses.GET,
        f"{transaction_splits_client.base_url}/split",
        json=mock_response,
        status=200,
    )

    data, meta = transaction_splits_client.list_splits()

    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["name"] == "Split 1"
    assert meta == {}


@responses.activate
def test_list_splits_with_all_params(transaction_splits_client):
    mock_response = {
        "status": True,
        "message": "Splits retrieved",
        "data": [{"name": "Split 1"}],
    }
    responses.add(
        responses.GET,
        f"{transaction_splits_client.base_url}/split?name=Test&active=True&sort_by=createdAt&perPage=10&page=1&from=2023-01-01&to=2023-01-31",
        json=mock_response,
        status=200,
    )

    data, meta = transaction_splits_client.list_splits(
        name="Test",
        active=True,
        sort_by="createdAt",
        per_page=10,
        page=1,
        from_date="2023-01-01",
        to_date="2023-01-31",
    )

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["name"] == "Split 1"
    assert meta == {}


@responses.activate
def test_fetch_split(transaction_splits_client):
    split_id = "SPL_test"
    mock_response = {
        "status": True,
        "message": "Split retrieved",
        "data": {"name": "Test Split", "id": split_id},
    }
    responses.add(
        responses.GET,
        f"{transaction_splits_client.base_url}/split/{split_id}",
        json=mock_response,
        status=200,
    )

    data, meta = transaction_splits_client.fetch_split(split_id=split_id)

    assert data["name"] == "Test Split"
    assert data["id"] == split_id
    assert meta == {}


@responses.activate
def test_update_split(transaction_splits_client):
    split_id = "SPL_test"
    payload = {
        "name": "Updated Split Name",
        "active": False,
    }
    mock_response = {
        "status": True,
        "message": "Split updated",
        "data": {"name": payload["name"], "id": split_id},
    }
    responses.add(
        responses.PUT,
        f"{transaction_splits_client.base_url}/split/{split_id}",
        json=mock_response,
        status=200,
    )

    data, meta = transaction_splits_client.update_split(split_id=split_id, **payload)

    assert data["name"] == payload["name"]
    assert data["id"] == split_id
    assert meta == {}


@responses.activate
def test_update_split_with_optional_params(transaction_splits_client):
    split_id = "SPL_test_optional"
    payload = {
        "name": "Updated Split Name Optional",
        "active": True,
        "bearer_type": "subaccount",
        "bearer_subaccount": "ACT_bearer_update",
    }
    mock_response = {
        "status": True,
        "message": "Split updated",
        "data": {"name": payload["name"], "id": split_id},
    }
    responses.add(
        responses.PUT,
        f"{transaction_splits_client.base_url}/split/{split_id}",
        json=mock_response,
        status=200,
    )

    data, meta = transaction_splits_client.update_split(split_id=split_id, **payload)

    assert data["name"] == payload["name"]
    assert data["id"] == split_id
    assert meta == {}


@responses.activate
def test_add_update_subaccount_split(transaction_splits_client):
    split_id = "SPL_test"
    payload = {
        "subaccount": "ACT_new",
        "share": 30,
    }
    mock_response = {
        "status": True,
        "message": "Subaccount added/updated",
        "data": {"split_id": split_id},
    }
    responses.add(
        responses.POST,
        f"{transaction_splits_client.base_url}/split/{split_id}/subaccount/add",
        json=mock_response,
        status=200,
    )

    data, meta = transaction_splits_client.add_update_subaccount_split(
        split_id=split_id, **payload
    )

    assert data["split_id"] == split_id
    assert meta == {}


@responses.activate
def test_remove_subaccount_from_split(transaction_splits_client):
    split_id = "SPL_test"
    subaccount = "ACT_remove"
    mock_response = {
        "status": True,
        "message": "Subaccount removed",
        "data": {"split_id": split_id},
    }
    responses.add(
        responses.POST,
        f"{transaction_splits_client.base_url}/split/{split_id}/subaccount/remove",
        json=mock_response,
        status=200,
    )

    data, meta = transaction_splits_client.remove_subaccount_from_split(
        split_id=split_id, subaccount=subaccount
    )

    assert data["split_id"] == split_id
    assert meta == {}