import pytest
import responses
from api.exceptions import AuthenticationError
from api.virtual_terminal import VirtualTerminalAPI


from .utils import assert_api_error_contains


@responses.activate
def test_create_virtual_terminal(virtual_terminal_client):
    payload = {
        "name": "Test Virtual Terminal",
        "destinations": [{"target": "2348012345678", "name": "John Doe"}],
    }
    mock_response = {
        "status": True,
        "message": "Virtual Terminal created",
        "data": {"name": payload["name"], "code": "VT_test"},
    }
    responses.add(
        responses.POST,
        f"{virtual_terminal_client.base_url}/virtual_terminal",
        json=mock_response,
        status=200,
    )

    data, meta = virtual_terminal_client.create_virtual_terminal(**payload)

    assert data["name"] == payload["name"]
    assert data["code"] == "VT_test"
    assert meta == {}


@responses.activate
def test_create_virtual_terminal_invalid_key(virtual_terminal_client):
    payload = {
        "name": "Test Virtual Terminal",
        "destinations": [{"target": "2348012345678", "name": "John Doe"}],
    }
    mock_response = {"status": False, "message": "Invalid API key"}
    responses.add(
        responses.POST,
        f"{virtual_terminal_client.base_url}/virtual_terminal",
        json=mock_response,
        status=401,
    )
    assert_api_error_contains(
        virtual_terminal_client.create_virtual_terminal, "Invalid API key", **payload
    )


@responses.activate
def test_list_virtual_terminals(virtual_terminal_client):
    mock_response = {
        "status": True,
        "message": "Virtual Terminals retrieved",
        "data": [{"name": "VT 1"}, {"name": "VT 2"}],
    }
    responses.add(
        responses.GET,
        f"{virtual_terminal_client.base_url}/virtual_terminal",
        json=mock_response,
        status=200,
    )

    data, meta = virtual_terminal_client.list_virtual_terminals()

    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["name"] == "VT 1"
    assert meta == {}


@responses.activate
def test_list_virtual_terminals_with_params(virtual_terminal_client):
    mock_response = {
        "status": True,
        "message": "Virtual Terminals retrieved",
        "data": [{"name": "VT 1"}],
    }
    responses.add(
        responses.GET,
        f"{virtual_terminal_client.base_url}/virtual_terminal?status=active&perPage=1",
        json=mock_response,
        status=200,
    )

    data, meta = virtual_terminal_client.list_virtual_terminals(status="active", per_page=1)

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["name"] == "VT 1"
    assert meta == {}


@responses.activate
def test_fetch_virtual_terminal(virtual_terminal_client):
    code = "VT_test"
    mock_response = {
        "status": True,
        "message": "Virtual Terminal retrieved",
        "data": {"name": "Test Virtual Terminal", "code": code},
    }
    responses.add(
        responses.GET,
        f"{virtual_terminal_client.base_url}/virtual_terminal/{code}",
        json=mock_response,
        status=200,
    )

    data, meta = virtual_terminal_client.fetch_virtual_terminal(code=code)

    assert data["name"] == "Test Virtual Terminal"
    assert data["code"] == code
    assert meta == {}


@responses.activate
def test_update_virtual_terminal(virtual_terminal_client):
    code = "VT_test"
    name = "Updated VT Name"
    mock_response = {
        "status": True,
        "message": "Virtual Terminal updated",
        "data": {"name": name, "code": code},
    }
    responses.add(
        responses.PUT,
        f"{virtual_terminal_client.base_url}/virtual_terminal/{code}",
        json=mock_response,
        status=200,
    )

    data, meta = virtual_terminal_client.update_virtual_terminal(code=code, name=name)

    assert data["name"] == name
    assert data["code"] == code
    assert meta == {}


@responses.activate
def test_deactivate_virtual_terminal(virtual_terminal_client):
    code = "VT_test"
    mock_response = {
        "status": True,
        "message": "Virtual Terminal deactivated",
        "data": {"code": code},
    }
    responses.add(
        responses.PUT,
        f"{virtual_terminal_client.base_url}/virtual_terminal/{code}/deactivate",
        json=mock_response,
        status=200,
    )

    data, meta = virtual_terminal_client.deactivate_virtual_terminal(code=code)

    assert data["code"] == code
    assert meta == {}


@responses.activate
def test_assign_destination_to_virtual_terminal(virtual_terminal_client):
    code = "VT_test"
    destinations = [{"target": "2348012345678", "name": "John Doe"}]
    mock_response = {
        "status": True,
        "message": "Destination assigned",
        "data": {"code": code},
    }
    responses.add(
        responses.POST,
        f"{virtual_terminal_client.base_url}/virtual_terminal/{code}/destination/assign",
        json=mock_response,
        status=200,
    )

    data, meta = virtual_terminal_client.assign_destination_to_virtual_terminal(
        code=code, destinations=destinations
    )

    assert data["code"] == code
    assert meta == {}


@responses.activate
def test_unassign_destination_from_virtual_terminal(virtual_terminal_client):
    code = "VT_test"
    targets = ["2348012345678"]
    mock_response = {
        "status": True,
        "message": "Destination unassigned",
        "data": {"code": code},
    }
    responses.add(
        responses.POST,
        f"{virtual_terminal_client.base_url}/virtual_terminal/{code}/destination/unassign",
        json=mock_response,
        status=200,
    )

    data, meta = virtual_terminal_client.unassign_destination_from_virtual_terminal(
        code=code, targets=targets
    )

    assert data["code"] == code
    assert meta == {}


@responses.activate
def test_add_split_code_to_virtual_terminal(virtual_terminal_client):
    code = "VT_test"
    split_code = "SPL_test"
    mock_response = {
        "status": True,
        "message": "Split code added",
        "data": {"code": code},
    }
    responses.add(
        responses.PUT,
        f"{virtual_terminal_client.base_url}/virtual_terminal/{code}/split_code",
        json=mock_response,
        status=200,
    )

    data, meta = virtual_terminal_client.add_split_code_to_virtual_terminal(
        code=code, split_code=split_code
    )

    assert data["code"] == code
    assert meta == {}


@responses.activate
def test_remove_split_code_from_virtual_terminal(virtual_terminal_client):
    code = "VT_test"
    split_code = "SPL_test"
    mock_response = {
        "status": True,
        "message": "Split code removed",
        "data": {"code": code},
    }
    responses.add(
        responses.DELETE,
        f"{virtual_terminal_client.base_url}/virtual_terminal/{code}/split_code",
        json=mock_response,
        status=200,
    )

    data, meta = virtual_terminal_client.remove_split_code_from_virtual_terminal(
        code=code, split_code=split_code
    )

    assert data["code"] == code
    assert meta == {}