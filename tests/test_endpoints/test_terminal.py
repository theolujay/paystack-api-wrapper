import responses


from tests.utils import assert_api_error_contains


@responses.activate
def test_send_event(terminal_client):
    terminal_id = "TRM_test"
    payload = {
        "type": "invoice",
        "action": "process",
        "data": {"id": "INV_test", "reference": "offline_ref"},
    }
    mock_response = {
        "status": True,
        "message": "Event sent",
        "data": {"terminal_id": terminal_id},
    }
    responses.add(
        responses.POST,
        f"{terminal_client.base_url}/terminal/{terminal_id}/event",
        json=mock_response,
        status=200,
    )

    data, meta = terminal_client.send_event(terminal_id=terminal_id, **payload)

    assert data["terminal_id"] == terminal_id
    assert meta == {}


@responses.activate
def test_send_event_invalid_key(terminal_client):
    terminal_id = "TRM_test"
    payload = {
        "type": "invoice",
        "action": "process",
        "data": {"id": "INV_test", "reference": "offline_ref"},
    }
    mock_response = {"status": False, "message": "Invalid API key"}
    responses.add(
        responses.POST,
        f"{terminal_client.base_url}/terminal/{terminal_id}/event",
        json=mock_response,
        status=401,
    )
    assert_api_error_contains(
        terminal_client.send_event,
        "Invalid API key",
        terminal_id=terminal_id,
        **payload,
    )


@responses.activate
def test_fetch_event_status(terminal_client):
    terminal_id = "TRM_test"
    event_id = "EVT_test"
    mock_response = {
        "status": True,
        "message": "Event status retrieved",
        "data": {"status": "processed"},
    }
    responses.add(
        responses.GET,
        f"{terminal_client.base_url}/terminal/{terminal_id}/event/{event_id}",
        json=mock_response,
        status=200,
    )

    data, meta = terminal_client.fetch_event_status(
        terminal_id=terminal_id, event_id=event_id
    )

    assert data["status"] == "processed"
    assert meta == {}


@responses.activate
def test_fetch_terminal_status(terminal_client):
    terminal_id = "TRM_test"
    mock_response = {
        "status": True,
        "message": "Terminal status retrieved",
        "data": {"status": "online"},
    }
    responses.add(
        responses.GET,
        f"{terminal_client.base_url}/terminal/{terminal_id}/presence",
        json=mock_response,
        status=200,
    )

    data, meta = terminal_client.fetch_terminal_status(terminal_id=terminal_id)

    assert data["status"] == "online"
    assert meta == {}


@responses.activate
def test_list_terminals(terminal_client):
    mock_response = {
        "status": True,
        "message": "Terminals retrieved",
        "data": [{"id": "TRM_1"}, {"id": "TRM_2"}],
    }
    responses.add(
        responses.GET,
        f"{terminal_client.base_url}/terminal",
        json=mock_response,
        status=200,
    )

    data, meta = terminal_client.list_terminals()

    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["id"] == "TRM_1"
    assert meta == {}


@responses.activate
def test_list_terminals_with_all_params(terminal_client):
    mock_response = {
        "status": True,
        "message": "Terminals retrieved",
        "data": [{"id": "TRM_1"}],
    }
    responses.add(
        responses.GET,
        f"{terminal_client.base_url}/terminal?perPage=1&next=next_cursor&previous=previous_cursor",
        json=mock_response,
        status=200,
    )

    data, meta = terminal_client.list_terminals(
        per_page=1, next_cursor="next_cursor", previous_cursor="previous_cursor"
    )

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["id"] == "TRM_1"
    assert meta == {}


@responses.activate
def test_fetch_terminal(terminal_client):
    terminal_id = "TRM_test"
    mock_response = {
        "status": True,
        "message": "Terminal retrieved",
        "data": {"id": terminal_id, "name": "Test Terminal"},
    }
    responses.add(
        responses.GET,
        f"{terminal_client.base_url}/terminal/{terminal_id}",
        json=mock_response,
        status=200,
    )

    data, meta = terminal_client.fetch_terminal(terminal_id=terminal_id)

    assert data["id"] == terminal_id
    assert data["name"] == "Test Terminal"
    assert meta == {}


@responses.activate
def test_update_terminal(terminal_client):
    terminal_id = "TRM_test"
    payload = {
        "name": "Updated Terminal Name",
        "address": "New Address",
    }
    mock_response = {
        "status": True,
        "message": "Terminal updated",
        "data": {"id": terminal_id, "name": payload["name"]},
    }
    responses.add(
        responses.PUT,
        f"{terminal_client.base_url}/terminal/{terminal_id}",
        json=mock_response,
        status=200,
    )

    data, meta = terminal_client.update_terminal(terminal_id=terminal_id, **payload)

    assert data["id"] == terminal_id
    assert data["name"] == payload["name"]
    assert meta == {}


@responses.activate
def test_commission_terminal(terminal_client):
    serial_number = "SN_test"
    mock_response = {
        "status": True,
        "message": "Terminal commissioned",
        "data": {"serial_number": serial_number},
    }
    responses.add(
        responses.POST,
        f"{terminal_client.base_url}/terminal/commission_device",
        json=mock_response,
        status=200,
    )

    data, meta = terminal_client.commission_terminal(serial_number=serial_number)

    assert data["serial_number"] == serial_number
    assert meta == {}


@responses.activate
def test_decommission_terminal(terminal_client):
    serial_number = "SN_test"
    mock_response = {
        "status": True,
        "message": "Terminal decommissioned",
        "data": {"serial_number": serial_number},
    }
    responses.add(
        responses.POST,
        f"{terminal_client.base_url}/terminal/decommission_device",
        json=mock_response,
        status=200,
    )

    data, meta = terminal_client.decommission_terminal(serial_number=serial_number)

    assert data["serial_number"] == serial_number
    assert meta == {}