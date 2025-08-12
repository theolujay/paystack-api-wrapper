import pytest
import requests
import responses
from requests.exceptions import Timeout

from api.core import BaseClient
from api.exceptions import APIError

BASE = "https://api.paystack.co"

@responses.activate
def test_baseclient_sets_authorization_header(secret_key):
    client = BaseClient(secret_key=secret_key, base_url=BASE)

    responses.add(
        responses.GET, f"{BASE}/test",
        json={
            "status": True,
            "message": "ok",
            "data": {"x": 1}
        }, status=200
    )
    data = client.request("GET", "test")
    assert responses.calls[0].request.headers["Authorization"] == f"Bearer {secret_key}"
    assert data == {"x": 1}

@responses.activate
def test_request_timeout(secret_key):
    client = BaseClient(secret_key=secret_key)
    
    def request_callback(request):
        raise Timeout("Connection timed out")

    responses.add_callback(
        responses.GET,
        f"{BASE}/test",
        callback=request_callback,
        content_type="application/json"
    )
    
    with pytest.raises(APIError) as excinfo:
        client.request("GET", "test")
    
    assert "Request timed out" in str(excinfo.value)
