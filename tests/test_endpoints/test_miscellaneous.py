import pytest
import responses
from paystack import APIError


from tests.utils import assert_api_error_contains


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

    data, meta = miscellaneous_client.list_banks(
        country="nigeria", use_cursor=False, per_page=10
    )

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["name"] == "Test Bank"
    assert meta == {}


@responses.activate
def test_list_banks_with_all_optional_params(miscellaneous_client):
    mock_response = {
        "status": True,
        "message": "Banks retrieved",
        "data": [{"name": "Test Bank All", "slug": "test-bank-all"}],
    }
    responses.add(
        responses.GET,
        f"{miscellaneous_client.base_url}/bank?country=nigeria&use_cursor=true&perPage=50&pay_with_bank_transfer=true&pay_with_bank=true&enabled_for_verification=true&next=next_cursor_val&previous=previous_cursor_val&gateway=emandate&type=mobile_money&currency=NGN&include_nip_sort_code=true",
        json=mock_response,
        status=200,
    )

    data, meta = miscellaneous_client.list_banks(
        country="nigeria",
        use_cursor=True,
        per_page=50,
        pay_with_bank_transfer=True,
        pay_with_bank=True,
        enabled_for_verification=True,
        next_cursor="next_cursor_val",
        previous="previous_cursor_val",
        gateway="emandate",
        type="mobile_money",
        currency="NGN",
        include_nip_sort_code=True,
    )

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["name"] == "Test Bank All"
    assert meta == {}


@responses.activate
def test_list_banks_invalid_country(miscellaneous_client):
    with pytest.raises(
        APIError, match="country must be one of: ghana, kenya, nigeria, south africa"
    ):
        miscellaneous_client.list_banks(
            country="invalid", use_cursor=False, per_page=10
        )


@responses.activate
def test_list_banks_invalid_per_page(miscellaneous_client):
    with pytest.raises(APIError, match="per_page must be between 1 and 100"):
        miscellaneous_client.list_banks(country="nigeria", use_cursor=False, per_page=0)
    with pytest.raises(APIError, match="per_page must be between 1 and 100"):
        miscellaneous_client.list_banks(
            country="nigeria", use_cursor=False, per_page=101
        )


@responses.activate
def test_list_banks_invalid_gateway(miscellaneous_client):
    with pytest.raises(
        APIError, match="gateway must be one of: emandate, digitalbankmandate"
    ):
        miscellaneous_client.list_banks(
            country="nigeria", use_cursor=False, per_page=10, gateway="invalid"
        )


@responses.activate
def test_list_banks_invalid_type(miscellaneous_client):
    with pytest.raises(APIError, match="type must be one of: mobile_money, ghipps"):
        miscellaneous_client.list_banks(
            country="ghana", use_cursor=False, per_page=10, type="invalid"
        )


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
        f"{miscellaneous_client.base_url}/bank?country=nigeria&use_cursor=false&perPage=50&include_nip_sort_code=false",
        json=mock_response,
        status=200,
    )

    data, meta = miscellaneous_client.get_nigerian_banks()

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["name"] == "Access Bank"
    assert meta == {}


@responses.activate
def test_get_nigerian_banks_with_nip(miscellaneous_client):
    mock_response = {
        "status": True,
        "message": "Banks retrieved",
        "data": [{"name": "Access Bank", "slug": "access-bank", "nip_code": "000001"}],
    }
    responses.add(
        responses.GET,
        f"{miscellaneous_client.base_url}/bank?country=nigeria&use_cursor=false&perPage=50&include_nip_sort_code=true",
        json=mock_response,
        status=200,
    )

    data, meta = miscellaneous_client.get_nigerian_banks(include_nip_sort_code=True)

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["name"] == "Access Bank"
    assert data[0]["nip_code"] == "000001"
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
        f"{miscellaneous_client.base_url}/bank?country=ghana&use_cursor=false&perPage=50&type=mobile_money",
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
        f"{miscellaneous_client.base_url}/bank?country=ghana&use_cursor=false&perPage=50&type=ghipps",
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
        f"{miscellaneous_client.base_url}/bank?country={country}&use_cursor=false&perPage=50&pay_with_bank_transfer=true",
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
        f"{miscellaneous_client.base_url}/bank?country={country}&use_cursor=false&perPage=50&pay_with_bank=true",
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
        f"{miscellaneous_client.base_url}/bank?country=south%20africa&use_cursor=false&perPage=50&enabled_for_verification=true",
        json=mock_response,
        status=200,
    )

    data, meta = miscellaneous_client.get_south_african_verification_banks()

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["name"] == "SA Verify Bank"
    assert meta == {}


@responses.activate
def test_get_south_african_verification_banks_with_currency(miscellaneous_client):
    mock_response = {
        "status": True,
        "message": "Banks retrieved",
        "data": [{"name": "SA Verify Bank USD", "slug": "sa-verify-bank-usd"}],
    }
    responses.add(
        responses.GET,
        f"{miscellaneous_client.base_url}/bank?country=south%20africa&use_cursor=false&perPage=50&enabled_for_verification=true&currency=USD",
        json=mock_response,
        status=200,
    )

    data, meta = miscellaneous_client.get_south_african_verification_banks(
        currency="USD"
    )

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["name"] == "SA Verify Bank USD"
    assert meta == {}
