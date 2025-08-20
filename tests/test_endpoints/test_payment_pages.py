import responses
import json

from tests.utils import assert_api_error_contains


@responses.activate
def test_create_payment_page(payment_pages_client):
    payload = {
        "name": "Test Page",
        "description": "A test payment page",
        "amount": 10000,
    }
    mock_response = {
        "status": True,
        "message": "Page created",
        "data": {"name": payload["name"], "slug": "test-page"},
    }
    responses.add(
        responses.POST,
        f"{payment_pages_client.base_url}/page",
        json=mock_response,
        status=200,
    )

    data, meta = payment_pages_client.create_payment_page(**payload)

    assert data["name"] == payload["name"]
    assert data["slug"] == "test-page"
    assert meta == {}


@responses.activate
def test_create_payment_page_with_all_params(payment_pages_client):
    payload = {
        "name": "Test Page All Params",
        "description": "A test payment page with all parameters",
        "amount": 20000,
        "currency": "USD",
        "slug": "test-page-all",
        "type": "subscription",
        "plan": "PLN_test",
        "fixed_amount": False,
        "split_code": "SPL_test",
        "metadata": {"key": "value"},
        "redirect_url": "https://example.com/redirect",
        "success_message": "Payment successful!",
        "notification_email": "test@example.com",
        "collect_phone": False,
        "custom_fields": [
            {
                "display_name": "Custom Field",
                "variable_name": "custom_field",
                "type": "text",
            }
        ],
    }
    mock_response = {
        "status": True,
        "message": "Page created",
        "data": {"name": payload["name"], "slug": payload["slug"]},
    }
    responses.add(
        responses.POST,
        f"{payment_pages_client.base_url}/page",
        json=mock_response,
        status=200,
    )

    data, meta = payment_pages_client.create_payment_page(**payload)

    assert data["name"] == payload["name"]
    assert data["slug"] == payload["slug"]
    assert meta == {}
    request = responses.calls[0].request
    request_payload = json.loads(request.body)
    assert request_payload["name"] == payload["name"]
    assert request_payload["description"] == payload["description"]
    assert request_payload["amount"] == payload["amount"]
    assert request_payload["currency"] == payload["currency"]
    assert request_payload["slug"] == payload["slug"]
    assert request_payload["type"] == payload["type"]
    assert request_payload["plan"] == payload["plan"]
    assert request_payload["fixed_amount"] == payload["fixed_amount"]
    assert request_payload["split_code"] == payload["split_code"]
    assert request_payload["metadata"] == payload["metadata"]
    assert request_payload["redirect_url"] == payload["redirect_url"]
    assert request_payload["success_message"] == payload["success_message"]
    assert request_payload["notification_email"] == payload["notification_email"]
    assert request_payload["collect_phone"] == payload["collect_phone"]
    assert request_payload["custom_fields"] == payload["custom_fields"]


@responses.activate
def test_create_payment_page_invalid_key(payment_pages_client):
    payload = {
        "name": "Test Page",
        "description": "A test payment page",
        "amount": 10000,
    }
    mock_response = {"status": False, "message": "Invalid API key"}
    responses.add(
        responses.POST,
        f"{payment_pages_client.base_url}/page",
        json=mock_response,
        status=401,
    )
    assert_api_error_contains(
        payment_pages_client.create_payment_page, "Invalid API key", **payload
    )


@responses.activate
def test_list_payment_pages(payment_pages_client):
    mock_response = {
        "status": True,
        "message": "Pages retrieved",
        "data": [{"name": "Page 1"}, {"name": "Page 2"}],
    }
    responses.add(
        responses.GET,
        f"{payment_pages_client.base_url}/page",
        json=mock_response,
        status=200,
    )

    data, meta = payment_pages_client.list_payment_pages()

    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["name"] == "Page 1"
    assert meta == {}


@responses.activate
def test_list_payment_pages_with_params(payment_pages_client):
    mock_response = {
        "status": True,
        "message": "Pages retrieved",
        "data": [{"name": "Page 1"}],
    }
    responses.add(
        responses.GET,
        f"{payment_pages_client.base_url}/page?perPage=1&page=1",
        json=mock_response,
        status=200,
    )

    data, meta = payment_pages_client.list_payment_pages(per_page=1, page=1)

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["name"] == "Page 1"
    assert meta == {}


@responses.activate
def test_list_payment_pages_with_all_params(payment_pages_client):
    mock_response = {
        "status": True,
        "message": "Pages retrieved",
        "data": [{"name": "Page 1"}],
    }
    responses.add(
        responses.GET,
        f"{payment_pages_client.base_url}/page?perPage=5&page=2&from=2024-01-01&to=2024-01-31",
        json=mock_response,
        status=200,
    )
    params = {
        "per_page": 5,
        "page": 2,
        "from_date": "2024-01-01",
        "to_date": "2024-01-31",
    }
    data, meta = payment_pages_client.list_payment_pages(**params)

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["name"] == "Page 1"
    assert meta == {}
    request = responses.calls[0].request
    assert request.method == "GET"
    assert "perPage=5" in request.url
    assert "page=2" in request.url
    assert "from=2024-01-01" in request.url
    assert "to=2024-01-31" in request.url


@responses.activate
def test_fetch_payment_page(payment_pages_client):
    id_or_slug = "test-page"
    mock_response = {
        "status": True,
        "message": "Page retrieved",
        "data": {"name": "Test Page", "slug": id_or_slug},
    }
    responses.add(
        responses.GET,
        f"{payment_pages_client.base_url}/page/{id_or_slug}",
        json=mock_response,
        status=200,
    )

    data, meta = payment_pages_client.fetch_payment_page(id_or_slug=id_or_slug)

    assert data["name"] == "Test Page"
    assert data["slug"] == id_or_slug
    assert meta == {}


@responses.activate
def test_update_payment_page(payment_pages_client):
    id_or_slug = "test-page"
    payload = {
        "name": "Updated Page Name",
        "active": False,
    }
    mock_response = {
        "status": True,
        "message": "Page updated",
        "data": {"name": payload["name"], "slug": id_or_slug},
    }
    responses.add(
        responses.PUT,
        f"{payment_pages_client.base_url}/page/{id_or_slug}",
        json=mock_response,
        status=200,
    )

    data, meta = payment_pages_client.update_payment_page(
        id_or_slug=id_or_slug, **payload
    )

    assert data["name"] == payload["name"]
    assert data["slug"] == id_or_slug
    assert meta == {}


@responses.activate
def test_update_payment_page_with_all_params(payment_pages_client):
    id_or_slug = "test-page-update"
    payload = {
        "name": "Updated Page Name All Params",
        "description": "Updated description",
        "amount": 30000,
        "active": False,
    }
    mock_response = {
        "status": True,
        "message": "Page updated",
        "data": {"name": payload["name"], "slug": id_or_slug},
    }
    responses.add(
        responses.PUT,
        f"{payment_pages_client.base_url}/page/{id_or_slug}",
        json=mock_response,
        status=200,
    )

    data, meta = payment_pages_client.update_payment_page(
        id_or_slug=id_or_slug, **payload
    )

    assert data["name"] == payload["name"]
    assert data["slug"] == id_or_slug
    assert meta == {}
    request = responses.calls[0].request
    request_payload = json.loads(request.body)
    assert request_payload["name"] == payload["name"]
    assert request_payload["description"] == payload["description"]
    assert request_payload["amount"] == payload["amount"]
    assert request_payload["active"] == payload["active"]


@responses.activate
def test_check_slug_availability(payment_pages_client):
    slug = "available-slug"
    mock_response = {
        "status": True,
        "message": "Slug available",
        "data": {"available": True},
    }
    responses.add(
        responses.GET,
        f"{payment_pages_client.base_url}/page/check_slug_availability/{slug}",
        json=mock_response,
        status=200,
    )

    data, meta = payment_pages_client.check_slug_availability(slug=slug)

    assert data["available"] is True
    assert meta == {}


@responses.activate
def test_add_products(payment_pages_client):
    page_id = 123
    product_ids = [1, 2, 3]
    mock_response = {
        "status": True,
        "message": "Products added",
        "data": {"page_id": page_id},
    }
    responses.add(
        responses.POST,
        f"{payment_pages_client.base_url}/page/{page_id}/product",
        json=mock_response,
        status=200,
    )

    data, meta = payment_pages_client.add_products(
        page_id=page_id, product_ids=product_ids
    )

    assert data["page_id"] == page_id
    assert meta == {}
