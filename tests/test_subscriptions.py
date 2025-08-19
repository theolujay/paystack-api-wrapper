import pytest
import responses
from api.exceptions import APIError
from api.subscriptions import SubscriptionsAPI


from .utils import assert_api_error_contains

@responses.activate
def test_create_subscription(subscriptions_client):
    payload = {
        "customer": "customer@example.com",
        "plan": "PLN_test",
    }
    mock_response = {
        "status": True,
        "message": "Subscription created",
        "data": {"customer": payload["customer"], "plan": payload["plan"]},
    }
    responses.add(
        responses.POST,
        f"{subscriptions_client.base_url}/subscription",
        json=mock_response,
        status=200,
    )

    data, meta = subscriptions_client.create_subscription(**payload)

    assert data["customer"] == payload["customer"]
    assert data["plan"] == payload["plan"]
    assert meta == {}


@responses.activate
def test_create_subscription_invalid_key(subscriptions_client):
    payload = {
        "customer": "customer@example.com",
        "plan": "PLN_test",
    }
    mock_response = {"status": False, "message": "Invalid API key"}
    responses.add(
        responses.POST,
        f"{subscriptions_client.base_url}/subscription",
        json=mock_response,
        status=401,
    )
    assert_api_error_contains(subscriptions_client.create_subscription, "Invalid API key", **payload)


@responses.activate
def test_list_subscriptions(subscriptions_client):
    mock_response = {
        "status": True,
        "message": "Subscriptions retrieved",
        "data": [{"id": 1, "status": "active"}, {"id": 2, "status": "inactive"}],
    }
    responses.add(
        responses.GET,
        f"{subscriptions_client.base_url}/subscription",
        json=mock_response,
        status=200,
    )

    data, meta = subscriptions_client.list_subscriptions()

    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["status"] == "active"
    assert meta == {}


@responses.activate
def test_list_subscriptions_with_params(subscriptions_client):
    mock_response = {
        "status": True,
        "message": "Subscriptions retrieved",
        "data": [{"id": 1, "status": "active"}],
    }
    responses.add(
        responses.GET,
        f"{subscriptions_client.base_url}/subscription?perPage=1&page=1",
        json=mock_response,
        status=200,
    )

    data, meta = subscriptions_client.list_subscriptions(per_page=1, page=1)

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["status"] == "active"
    assert meta == {}


@responses.activate
def test_fetch_subscription(subscriptions_client):
    id_or_code = "SUB_test"
    mock_response = {
        "status": True,
        "message": "Subscription retrieved",
        "data": {"id": 1, "subscription_code": id_or_code},
    }
    responses.add(
        responses.GET,
        f"{subscriptions_client.base_url}/subscription/{id_or_code}",
        json=mock_response,
        status=200,
    )

    data, meta = subscriptions_client.fetch_subscription(id_or_code=id_or_code)

    assert data["subscription_code"] == id_or_code
    assert meta == {}


@responses.activate
def test_enable_subscription(subscriptions_client):
    code = "SUB_test"
    token = "test_token"
    mock_response = {
        "status": True,
        "message": "Subscription enabled",
        "data": {"code": code},
    }
    responses.add(
        responses.POST,
        f"{subscriptions_client.base_url}/subscription/enable",
        json=mock_response,
        status=200,
    )

    data, meta = subscriptions_client.enable_subscription(code=code, token=token)

    assert data["code"] == code
    assert meta == {}


@responses.activate
def test_disable_subscription(subscriptions_client):
    code = "SUB_test"
    token = "test_token"
    mock_response = {
        "status": True,
        "message": "Subscription disabled",
        "data": {"code": code},
    }
    responses.add(
        responses.POST,
        f"{subscriptions_client.base_url}/subscription/disable",
        json=mock_response,
        status=200,
    )

    data, meta = subscriptions_client.disable_subscription(code=code, token=token)

    assert data["code"] == code
    assert meta == {}


@responses.activate
def test_generate_update_subscription_link(subscriptions_client):
    code = "SUB_test"
    mock_response = {
        "status": True,
        "message": "Update link generated",
        "data": {"link": "http://example.com/update"},
    }
    responses.add(
        responses.GET,
        f"{subscriptions_client.base_url}/subscription/{code}/manage/link",
        json=mock_response,
        status=200,
    )

    data, meta = subscriptions_client.generate_update_subscription_link(code=code)

    assert data["link"] == "http://example.com/update"
    assert meta == {}


@responses.activate
def test_send_update_subscription_link(subscriptions_client):
    code = "SUB_test"
    mock_response = {
        "status": True,
        "message": "Update link sent",
        "data": {"code": code},
    }
    responses.add(
        responses.POST,
        f"{subscriptions_client.base_url}/subscription/{code}/manage/email",
        json=mock_response,
        status=200,
    )

    data, meta = subscriptions_client.send_update_subscription_link(code=code)

    assert data["code"] == code
    assert meta == {}