import responses

from tests.utils import assert_api_error_contains


@responses.activate
def test_register_domain(apple_pay_client):
    domain_name = "example.com"
    mock_response = {
        "status": True,
        "message": "Domain registered",
        "data": {"domain_name": domain_name},
    }
    responses.add(
        responses.POST,
        f"{apple_pay_client.base_url}/apple-pay/domain",
        json=mock_response,
        status=200,
    )

    data, meta = apple_pay_client.register_domain(domain_name=domain_name)

    assert data["domain_name"] == domain_name
    assert meta == {}


@responses.activate
def test_register_domain_invalid_key(apple_pay_client):
    domain_name = "example.com"
    mock_response = {"status": False, "message": "Invalid API key"}
    responses.add(
        responses.POST,
        f"{apple_pay_client.base_url}/apple-pay/domain",
        json=mock_response,
        status=401,
    )
    assert_api_error_contains(
        apple_pay_client.register_domain, "Invalid API key", domain_name=domain_name
    )


@responses.activate
def test_list_domains(apple_pay_client):
    mock_response = {
        "status": True,
        "message": "Domains retrieved",
        "data": [{"domain_name": "example.com"}, {"domain_name": "test.org"}],
    }
    responses.add(
        responses.GET,
        f"{apple_pay_client.base_url}/apple-pay/domain",
        json=mock_response,
        status=200,
    )

    data, meta = apple_pay_client.list_domains()

    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["domain_name"] == "example.com"
    assert meta == {}


@responses.activate
def test_list_domains_with_cursor(apple_pay_client):
    mock_response = {
        "status": True,
        "message": "Domains retrieved",
        "data": [{"domain_name": "example.com"}],
        "meta": {"next": "cursor_next", "previous": None},
    }
    responses.add(
        responses.GET,
        f"{apple_pay_client.base_url}/apple-pay/domain?use_cursor=True&next=cursor_next",
        json=mock_response,
        status=200,
    )

    data, meta = apple_pay_client.list_domains(
        use_cursor=True, next_cursor="cursor_next"
    )

    assert isinstance(data, list)
    assert len(data) == 1
    assert meta["next"] == "cursor_next"


@responses.activate
def test_list_domains_with_previous_cursor(apple_pay_client):
    mock_response = {
        "status": True,
        "message": "Domains retrieved",
        "data": [{"domain_name": "example.com"}],
        "meta": {"next": None, "previous": "cursor_previous"},
    }
    responses.add(
        responses.GET,
        f"{apple_pay_client.base_url}/apple-pay/domain?previous=cursor_previous",
        json=mock_response,
        status=200,
    )

    data, meta = apple_pay_client.list_domains(previous_cursor="cursor_previous")

    assert isinstance(data, list)
    assert len(data) == 1
    assert meta["previous"] == "cursor_previous"


@responses.activate
def test_list_domains_invalid_key(apple_pay_client):
    mock_response = {"status": False, "message": "Invalid API key"}
    responses.add(
        responses.GET,
        f"{apple_pay_client.base_url}/apple-pay/domain",
        json=mock_response,
        status=401,
    )
    assert_api_error_contains(apple_pay_client.list_domains, "Invalid API key")


@responses.activate
def test_unregister_domain(apple_pay_client):
    domain_name = "example.com"
    mock_response = {
        "status": True,
        "message": "Domain unregistered",
        "data": {"domain_name": domain_name},
    }
    responses.add(
        responses.DELETE,
        f"{apple_pay_client.base_url}/apple-pay/domain",
        json=mock_response,
        status=200,
    )

    data, meta = apple_pay_client.unregister_domain(domain_name=domain_name)

    assert data["domain_name"] == domain_name
    assert meta == {}


@responses.activate
def test_unregister_domain_invalid_key(apple_pay_client):
    domain_name = "example.com"
    mock_response = {"status": False, "message": "Invalid API key"}
    responses.add(
        responses.DELETE,
        f"{apple_pay_client.base_url}/apple-pay/domain",
        json=mock_response,
        status=401,
    )
    assert_api_error_contains(
        apple_pay_client.unregister_domain, "Invalid API key", domain_name=domain_name
    )
