import responses


from tests.utils import assert_api_error_contains


@responses.activate
def test_create_subaccount(subaccounts_client):
    payload = {
        "business_name": "Test Business",
        "bank_code": "044",
        "account_number": "0123456789",
        "percentage_charge": 10.5,
    }
    mock_response = {
        "status": True,
        "message": "Subaccount created",
        "data": {
            "business_name": payload["business_name"],
            "subaccount_code": "SUB_test",
        },
    }
    responses.add(
        responses.POST,
        f"{subaccounts_client.base_url}/subaccount",
        json=mock_response,
        status=200,
    )

    data, meta = subaccounts_client.create_subaccount(**payload)

    assert data["business_name"] == payload["business_name"]
    assert data["subaccount_code"] == "SUB_test"
    assert meta == {}


@responses.activate
def test_create_subaccount_invalid_key(subaccounts_client):
    payload = {
        "business_name": "Test Business",
        "bank_code": "044",
        "account_number": "0123456789",
        "percentage_charge": 10.5,
    }
    mock_response = {"status": False, "message": "Invalid API key"}
    responses.add(
        responses.POST,
        f"{subaccounts_client.base_url}/subaccount",
        json=mock_response,
        status=401,
    )
    assert_api_error_contains(
        subaccounts_client.create_subaccount, "Invalid API key", **payload
    )


@responses.activate
def test_list_subaccounts(subaccounts_client):
    mock_response = {
        "status": True,
        "message": "Subaccounts retrieved",
        "data": [{"business_name": "Subaccount 1"}, {"business_name": "Subaccount 2"}],
    }
    responses.add(
        responses.GET,
        f"{subaccounts_client.base_url}/subaccount",
        json=mock_response,
        status=200,
    )

    data, meta = subaccounts_client.list_subaccounts()

    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["business_name"] == "Subaccount 1"
    assert meta == {}


@responses.activate
def test_list_subaccounts_with_params(subaccounts_client):
    mock_response = {
        "status": True,
        "message": "Subaccounts retrieved",
        "data": [{"business_name": "Subaccount 1"}],
    }
    responses.add(
        responses.GET,
        f"{subaccounts_client.base_url}/subaccount?perPage=1&page=1",
        json=mock_response,
        status=200,
    )

    data, meta = subaccounts_client.list_subaccounts(per_page=1, page=1)

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["business_name"] == "Subaccount 1"
    assert meta == {}


@responses.activate
def test_fetch_subaccount(subaccounts_client):
    id_or_code = "SUB_test"
    mock_response = {
        "status": True,
        "message": "Subaccount retrieved",
        "data": {"business_name": "Test Business", "subaccount_code": id_or_code},
    }
    responses.add(
        responses.GET,
        f"{subaccounts_client.base_url}/subaccount/{id_or_code}",
        json=mock_response,
        status=200,
    )

    data, meta = subaccounts_client.fetch_subaccount(id_or_code=id_or_code)

    assert data["business_name"] == "Test Business"
    assert data["subaccount_code"] == id_or_code
    assert meta == {}


@responses.activate
def test_update_subaccount(subaccounts_client):
    id_or_code = "SUB_test"
    payload = {
        "business_name": "Updated Business Name",
        "percentage_charge": 12.0,
    }
    mock_response = {
        "status": True,
        "message": "Subaccount updated",
        "data": {
            "business_name": payload["business_name"],
            "subaccount_code": id_or_code,
        },
    }
    responses.add(
        responses.PUT,
        f"{subaccounts_client.base_url}/subaccount/{id_or_code}",
        json=mock_response,
        status=200,
    )

    data, meta = subaccounts_client.update_subaccount(id_or_code=id_or_code, **payload)

    assert data["business_name"] == payload["business_name"]
    assert data["subaccount_code"] == id_or_code
    assert meta == {}
