import pytest
import requests
import responses
from api.exceptions import APIError

# === Test Helpers ===
def assert_api_error_contains(callable_method, expected_keyword, *args, **kwargs):
    with pytest.raises(APIError) as excinfo:
        callable_method(*args, **kwargs)
    assert str(expected_keyword).lower() in str(excinfo.value).lower()

def setup_mock_response(transaction_client, id_or_reference, response_data=None, status_code=200):
    if response_data is None:
        response_data = {
            "status": True,
            "message": "Timeline retrieved",
            "data": {
                "start_time": 1724318098,
                "time_spent": 4,
                "attempts": 1,
                "errors": 0,
                "success": True,
                "mobile": False,
                "input": [],
                "history": [
                    {
                        "type": "action",
                        "message": "Attempted to pay with card",
                        "time": 3
                    },
                    {
                        "type": "success",
                        "message": "Successfully paid with card",
                        "time": 4
                    }
                ]
            }
        }

    responses.add(
        responses.GET,
        f"{transaction_client.base_url}/transaction/timeline/{id_or_reference}",
        json=response_data,
        status=status_code,
    )

@responses.activate
def test_view_timeline(transaction_client):
    id_or_reference = "0m7frfnr47ezyxl"
    setup_mock_response(transaction_client, id_or_reference)
    
    data = transaction_client.view_timeline(id_or_reference)
    
    assert isinstance(data, dict)
    assert data["success"] is True
    assert isinstance(data["history"], list)
    assert data["history"][0]["message"] == "Attempted to pay with card"

@responses.activate
def test_view_timeline_invalid_key(transaction_client):
    id_or_reference = "0m7frfnr47ezyxl"
    mock_response = {"status": False, "message": "Invalid API key"}
    setup_mock_response(transaction_client, id_or_reference, mock_response, status_code=401)
    assert_api_error_contains(transaction_client.view_timeline, "unauthorized", id_or_reference)

@responses.activate
def test_view_timeline_timeout(transaction_client):
    id_or_reference = "0m7frfnr47ezyxl"
    responses.add(
        responses.GET,
        f"{transaction_client.base_url}/transaction/timeline/{id_or_reference}",
        body=requests.exceptions.Timeout(),
    )
    assert_api_error_contains(transaction_client.view_timeline, "timed out", id_or_reference)

@responses.activate
def test_view_timeline_malformed_json(transaction_client):
    id_or_reference = "0m7frfnr47ezyxl"
    responses.add(
        responses.GET,
        f"{transaction_client.base_url}/transaction/timeline/{id_or_reference}",
        body="Not a JSON",
        status=200,
    )
    assert_api_error_contains(transaction_client.view_timeline, "invalid json response", id_or_reference)
