import responses


from tests.utils import assert_api_error_contains


@responses.activate
def test_fetch_timeout(integration_client):
    mock_response = {
        "status": True,
        "message": "Payment session timeout retrieved",
        "data": {"timeout": 3600},
    }
    responses.add(
        responses.GET,
        f"{integration_client.base_url}/integration/payment_session_timeout",
        json=mock_response,
        status=200,
    )

    data, meta = integration_client.fetch_timeout()

    assert data["timeout"] == 3600
    assert meta == {}


@responses.activate
def test_fetch_timeout_invalid_key(integration_client):
    mock_response = {"status": False, "message": "Invalid API key"}
    responses.add(
        responses.GET,
        f"{integration_client.base_url}/integration/payment_session_timeout",
        json=mock_response,
        status=401,
    )
    assert_api_error_contains(integration_client.fetch_timeout, "Invalid API key")


@responses.activate
def test_update_timeout(integration_client):
    timeout = 1800
    mock_response = {
        "status": True,
        "message": "Payment session timeout updated",
        "data": {"timeout": timeout},
    }
    responses.add(
        responses.PUT,
        f"{integration_client.base_url}/integration/payment_session_timeout",
        json=mock_response,
        status=200,
    )

    data, meta = integration_client.update_timeout(timeout=timeout)

    assert data["timeout"] == timeout
    assert meta == {}


@responses.activate
def test_update_timeout_invalid_key(integration_client):
    timeout = 1800
    mock_response = {"status": False, "message": "Invalid API key"}
    responses.add(
        responses.PUT,
        f"{integration_client.base_url}/integration/payment_session_timeout",
        json=mock_response,
        status=401,
    )
    assert_api_error_contains(integration_client.update_timeout, "Invalid API key", timeout=timeout)