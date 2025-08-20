import responses


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
