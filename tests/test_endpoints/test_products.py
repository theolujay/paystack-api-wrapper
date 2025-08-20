import responses


from tests.utils import assert_api_error_contains


@responses.activate
def test_create_product(products_client):
    payload = {
        "name": "Test Product",
        "description": "A test product description",
        "price": 10000,
        "currency": "NGN",
    }
    mock_response = {
        "status": True,
        "message": "Product created",
        "data": {"name": payload["name"], "id": 123},
    }
    responses.add(
        responses.POST,
        f"{products_client.base_url}/product",
        json=mock_response,
        status=200,
    )

    data, meta = products_client.create_product(**payload)

    assert data["name"] == payload["name"]
    assert data["id"] == 123
    assert meta == {}


@responses.activate
def test_create_product_invalid_key(products_client):
    payload = {
        "name": "Test Product",
        "description": "A test product description",
        "price": 10000,
        "currency": "NGN",
    }
    mock_response = {"status": False, "message": "Invalid API key"}
    responses.add(
        responses.POST,
        f"{products_client.base_url}/product",
        json=mock_response,
        status=401,
    )
    assert_api_error_contains(
        products_client.create_product, "Invalid API key", **payload
    )


@responses.activate
def test_list_products(products_client):
    mock_response = {
        "status": True,
        "message": "Products retrieved",
        "data": [{"name": "Product 1"}, {"name": "Product 2"}],
    }
    responses.add(
        responses.GET,
        f"{products_client.base_url}/product",
        json=mock_response,
        status=200,
    )

    data, meta = products_client.list_products()

    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["name"] == "Product 1"
    assert meta == {}


@responses.activate
def test_list_products_with_params(products_client):
    mock_response = {
        "status": True,
        "message": "Products retrieved",
        "data": [{"name": "Product 1"}],
    }
    responses.add(
        responses.GET,
        f"{products_client.base_url}/product?perPage=1&page=1",
        json=mock_response,
        status=200,
    )

    data, meta = products_client.list_products(per_page=1, page=1)

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["name"] == "Product 1"
    assert meta == {}


@responses.activate
def test_fetch_product(products_client):
    product_id = "123"
    mock_response = {
        "status": True,
        "message": "Product retrieved",
        "data": {"name": "Test Product", "id": product_id},
    }
    responses.add(
        responses.GET,
        f"{products_client.base_url}/product/{product_id}",
        json=mock_response,
        status=200,
    )

    data, meta = products_client.fetch_product(product_id=product_id)

    assert data["name"] == "Test Product"
    assert data["id"] == product_id
    assert meta == {}


@responses.activate
def test_update_product(products_client):
    product_id = "123"
    payload = {
        "name": "Updated Product Name",
        "price": 15000,
    }
    mock_response = {
        "status": True,
        "message": "Product updated",
        "data": {"name": payload["name"], "id": product_id},
    }
    responses.add(
        responses.PUT,
        f"{products_client.base_url}/product/{product_id}",
        json=mock_response,
        status=200,
    )

    data, meta = products_client.update_product(product_id=product_id, **payload)

    assert data["name"] == payload["name"]
    assert data["id"] == product_id
    assert meta == {}
