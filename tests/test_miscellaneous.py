import pytest
import responses
from paystack_client.exceptions import APIError
from paystack_client.miscellaneous import MiscellaneousAPI


from .utils import assert_api_error_contains


@responses.activate
def test_list_banks(miscellaneous_client):
    mock_response = {
        "status": True,
        "message": "Banks retrieved",
        "data": [{"name": "Test Bank", "slug": "test-bank"}],
    }
    responses.add(
        responses.GET,
        f"{miscellaneous_client.base_url}/bank",
        json=mock_response,
        status=200,
    )

    data, meta = miscellaneous_client.list_banks(country="nigeria", use_cursor=False, per_page=10)

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["name"] == "Test Bank"
    assert meta == {}


@responses.activate
def test_list_banks_invalid_country(miscellaneous_client):
    with pytest.raises(APIError):
        miscellaneous_client.list_banks(country="invalid", use_cursor=False, per_page=10)


@responses.activate
def test_list_banks_invalid_per_page(miscellaneous_client):
    with pytest.raises(APIError):
        miscellaneous_client.list_banks(country="nigeria", use_cursor=False, per_page=0)
    with pytest.raises(APIError):
        miscellaneous_client.list_banks(country="nigeria", use_cursor=False, per_page=101)


@responses.activate
def test_list_countries(miscellaneous_client):
    mock_response = {
        "status": True,
        "message": "Countries retrieved",
        "data": [{"name": "Nigeria", "code": "NG"}],
    }
    responses.add(
        responses.GET,
        f"{miscellaneous_client.base_url}/country",
        json=mock_response,
        status=200,
    )

    data, meta = miscellaneous_client.list_countries()

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["name"] == "Nigeria"
    assert meta == {}


@responses.activate
def test_list_states(miscellaneous_client):
    country = "NG"
    mock_response = {
        "status": True,
        "message": "States retrieved",
        "data": [{"name": "Lagos", "slug": "lagos"}],
    }
    responses.add(
        responses.GET,
        f"{miscellaneous_client.base_url}/address_verification/states?country={country}",
        json=mock_response,
        status=200,
    )

    data, meta = miscellaneous_client.list_states(country=country)

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["name"] == "Lagos"
    assert meta == {}


@responses.activate
def test_get_nigerian_banks(miscellaneous_client):
    mock_response = {
        "status": True,
        "message": "Banks retrieved",
        "data": [{"name": "Access Bank", "slug": "access-bank"}],
    }
    responses.add(
        responses.GET,
        f"{miscellaneous_client.base_url}/bank",
        json=mock_response,
        status=200,
    )

    data, meta = miscellaneous_client.get_nigerian_banks()

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["name"] == "Access Bank"
    assert meta == {}


@responses.activate
def test_get_ghanaian_mobile_money_providers(miscellaneous_client):
    mock_response = {
        "status": True,
        "message": "Banks retrieved",
        "data": [{"name": "MTN Mobile Money", "slug": "mtn-mobile-money"}],
    }
    responses.add(
        responses.GET,
        f"{miscellaneous_client.base_url}/bank",
        json=mock_response,
        status=200,
    )

    data, meta = miscellaneous_client.get_ghanaian_mobile_money_providers()

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["name"] == "MTN Mobile Money"
    assert meta == {}


@responses.activate
def test_get_ghanaian_banks(miscellaneous_client):
    mock_response = {
        "status": True,
        "message": "Banks retrieved",
        "data": [{"name": "Ghana Commercial Bank", "slug": "ghana-commercial-bank"}],
    }
    responses.add(
        responses.GET,
        f"{miscellaneous_client.base_url}/bank",
        json=mock_response,
        status=200,
    )

    data, meta = miscellaneous_client.get_ghanaian_banks()

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["name"] == "Ghana Commercial Bank"
    assert meta == {}


@responses.activate
def test_get_banks_for_transfer(miscellaneous_client):
    country = "nigeria"
    mock_response = {
        "status": True,
        "message": "Banks retrieved",
        "data": [{"name": "Transfer Bank", "slug": "transfer-bank"}],
    }
    responses.add(
        responses.GET,
        f"{miscellaneous_client.base_url}/bank",
        json=mock_response,
        status=200,
    )

    data, meta = miscellaneous_client.get_banks_for_transfer(country=country)

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["name"] == "Transfer Bank"
    assert meta == {}


@responses.activate
def test_get_banks_for_direct_payment(miscellaneous_client):
    country = "nigeria"
    mock_response = {
        "status": True,
        "message": "Banks retrieved",
        "data": [{"name": "Direct Pay Bank", "slug": "direct-pay-bank"}],
    }
    responses.add(
        responses.GET,
        f"{miscellaneous_client.base_url}/bank",
        json=mock_response,
        status=200,
    )

    data, meta = miscellaneous_client.get_banks_for_direct_payment(country=country)

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["name"] == "Direct Pay Bank"
    assert meta == {}


@responses.activate
def test_get_south_african_verification_banks(miscellaneous_client):
    mock_response = {
        "status": True,
        "message": "Banks retrieved",
        "data": [{"name": "SA Verify Bank", "slug": "sa-verify-bank"}],
    }
    responses.add(
        responses.GET,
        f"{miscellaneous_client.base_url}/bank",
        json=mock_response,
        status=200,
    )

    data, meta = miscellaneous_client.get_south_african_verification_banks()

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["name"] == "SA Verify Bank"
    assert meta == {}