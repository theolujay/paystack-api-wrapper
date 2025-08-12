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

@responses.activate
def test_false_status_response(secret_key):
    client = BaseClient(secret_key=secret_key)
    
    responses.add(
        responses.POST, f"{BASE}/initiate_payment",
        json={
            "status": False,
            "message": "API error",
        }, status=200
    )
    with pytest.raises(APIError) as excinfo:
        client.request("POST", "initiate_payment")
    assert "API error" in str(excinfo.value)

@responses.activate
def test_invalid_response_structure(secret_key):
    client = BaseClient(secret_key=secret_key)
    
    responses.add(
        responses.POST, f"{BASE}/initiate_payment",
        json={
            "status": True,
            "message": "Invalid JSON response",
        }, status=200
    )
    with pytest.raises(APIError) as excinfo:
        client.request("POST", "initiate_payment")
    assert "Unexpected response structure from Paystack" in str(excinfo.value)

@responses.activate
def test_error_status_code(secret_key):
    client = BaseClient(secret_key=secret_key)
    
    responses.add(
        responses.POST, f"{BASE}/initiate_payment",
        json={
            "status": False,
            "message": "API error",
        }, status=400
    )
    with pytest.raises(APIError) as excinfo:
        client.request("POST", "initiate_payment")
    assert "HTTP error" in str(excinfo.value)
    assert "400" in str(excinfo.value)
    
@responses.activate
def test_invalid_json(secret_key):
    client = BaseClient(secret_key=secret_key)
    responses.add(
        responses.GET, f"{BASE}/test",
        body="not json",
        status=200,
        content_type="application/json"
    )
    with pytest.raises(APIError) as excinfo:
        client.request("GET", "test")
    assert "Invalid JSON response" in str(excinfo.value)