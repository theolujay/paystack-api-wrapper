import pytest
import responses
from paystack_client.exceptions import APIError
from paystack_client.plans import PlansAPI

from .utils import assert_api_error_contains


@responses.activate
def test_create_plan(plans_client):
    payload = {
        "name": "Monthly Plan",
        "amount": 10000,
        "interval": "monthly",
    }
    mock_response = {
        "status": True,
        "message": "Plan created",
        "data": {"name": payload["name"], "plan_code": "PLN_test"},
    }
    responses.add(
        responses.POST,
        f"{plans_client.base_url}/plan",
        json=mock_response,
        status=200,
    )

    data, meta = plans_client.create_plan(**payload)

    assert data["name"] == payload["name"]
    assert data["plan_code"] == "PLN_test"
    assert meta == {}


@responses.activate
def test_create_plan_invalid_key(plans_client):
    payload = {
        "name": "Monthly Plan",
        "amount": 10000,
        "interval": "monthly",
    }
    mock_response = {"status": False, "message": "Invalid API key"}
    responses.add(
        responses.POST,
        f"{plans_client.base_url}/plan",
        json=mock_response,
        status=401,
    )
    assert_api_error_contains(plans_client.create_plan, "Invalid API key", **payload)


@responses.activate
def test_list_plans(plans_client):
    mock_response = {
        "status": True,
        "message": "Plans retrieved",
        "data": [{"name": "Plan 1"}, {"name": "Plan 2"}],
    }
    responses.add(
        responses.GET,
        f"{plans_client.base_url}/plan",
        json=mock_response,
        status=200,
    )

    data, meta = plans_client.list_plans()

    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["name"] == "Plan 1"
    assert meta == {}


@responses.activate
def test_list_plans_with_params(plans_client):
    mock_response = {
        "status": True,
        "message": "Plans retrieved",
        "data": [{"name": "Plan 1"}],
    }
    responses.add(
        responses.GET,
        f"{plans_client.base_url}/plan?perPage=1&page=1",
        json=mock_response,
        status=200,
    )

    data, meta = plans_client.list_plans(per_page=1, page=1)

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["name"] == "Plan 1"
    assert meta == {}


@responses.activate
def test_fetch_plan(plans_client):
    id_or_code = "PLN_test"
    mock_response = {
        "status": True,
        "message": "Plan retrieved",
        "data": {"name": "Test Plan", "plan_code": id_or_code},
    }
    responses.add(
        responses.GET,
        f"{plans_client.base_url}/plan/{id_or_code}",
        json=mock_response,
        status=200,
    )

    data, meta = plans_client.fetch_plan(id_or_code=id_or_code)

    assert data["name"] == "Test Plan"
    assert data["plan_code"] == id_or_code
    assert meta == {}


@responses.activate
def test_update_plan(plans_client):
    id_or_code = "PLN_test"
    payload = {
        "name": "Updated Plan Name",
        "amount": 15000,
    }
    mock_response = {
        "status": True,
        "message": "Plan updated",
        "data": {"name": payload["name"], "plan_code": id_or_code},
    }
    responses.add(
        responses.PUT,
        f"{plans_client.base_url}/plan/{id_or_code}",
        json=mock_response,
        status=200,
    )

    data, meta = plans_client.update_plan(id_or_code=id_or_code, **payload)

    assert data["name"] == payload["name"]
    assert data["plan_code"] == id_or_code
    assert meta == {}