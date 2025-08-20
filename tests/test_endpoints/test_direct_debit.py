import responses

from tests.utils import assert_api_error_contains


@responses.activate
def test_trigger_activation_charge(direct_debit_client):
    customer_ids = [1, 2, 3]
    mock_response = {
        "status": True,
        "message": "Activation charge triggered",
        "data": {"customer_ids": customer_ids},
    }
    responses.add(
        responses.PUT,
        f"{direct_debit_client.base_url}/directdebit/activation-charge",
        json=mock_response,
        status=200,
    )

    data, meta = direct_debit_client.trigger_activation_charge(
        customer_ids=customer_ids
    )

    assert data["customer_ids"] == customer_ids
    assert meta == {}


@responses.activate
def test_trigger_activation_charge_invalid_key(direct_debit_client):
    customer_ids = [1, 2, 3]
    mock_response = {"status": False, "message": "Invalid API key"}
    responses.add(
        responses.PUT,
        f"{direct_debit_client.base_url}/directdebit/activation-charge",
        json=mock_response,
        status=401,
    )
    assert_api_error_contains(
        direct_debit_client.trigger_activation_charge,
        "Invalid API key",
        customer_ids=customer_ids,
    )


@responses.activate
def test_list_mandate_authorizations(direct_debit_client):
    mock_response = {
        "status": True,
        "message": "Mandate authorizations retrieved",
        "data": [{"id": 1, "status": "active"}, {"id": 2, "status": "pending"}],
    }
    responses.add(
        responses.GET,
        f"{direct_debit_client.base_url}/directdebit/mandate-authorizations",
        json=mock_response,
        status=200,
    )

    data, meta = direct_debit_client.list_mandate_authorizations()

    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["status"] == "active"
    assert meta == {}


@responses.activate
def test_list_mandate_authorizations_with_params(direct_debit_client):
    mock_response = {
        "status": True,
        "message": "Mandate authorizations retrieved",
        "data": [{"id": 1, "status": "active"}],
    }
    responses.add(
        responses.GET,
        f"{direct_debit_client.base_url}/directdebit/mandate-authorizations?status=active&per_page=1",
        json=mock_response,
        status=200,
    )

    data, meta = direct_debit_client.list_mandate_authorizations(
        status="active", per_page=1
    )

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["status"] == "active"
    assert meta == {}


@responses.activate
def test_list_mandate_authorizations_invalid_key(direct_debit_client):
    mock_response = {"status": False, "message": "Invalid API key"}
    responses.add(
        responses.GET,
        f"{direct_debit_client.base_url}/directdebit/mandate-authorizations",
        json=mock_response,
        status=401,
    )
    assert_api_error_contains(
        direct_debit_client.list_mandate_authorizations, "Invalid API key"
    )
