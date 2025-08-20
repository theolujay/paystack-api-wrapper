import responses


from tests.utils import assert_api_error_contains


@responses.activate
def test_check_balance(transfers_control_client):
    mock_response = {
        "status": True,
        "message": "Balance retrieved",
        "data": [{"currency": "NGN", "balance": 100000}],
    }
    responses.add(
        responses.GET,
        f"{transfers_control_client.base_url}/balance",
        json=mock_response,
        status=200,
    )

    data, meta = transfers_control_client.check_balance()

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["currency"] == "NGN"
    assert data[0]["balance"] == 100000
    assert meta == {}


@responses.activate
def test_check_balance_invalid_key(transfers_control_client):
    mock_response = {"status": False, "message": "Invalid API key"}
    responses.add(
        responses.GET,
        f"{transfers_control_client.base_url}/balance",
        json=mock_response,
        status=401,
    )
    assert_api_error_contains(transfers_control_client.check_balance, "Invalid API key")


@responses.activate
def test_fetch_balance_ledger(transfers_control_client):
    mock_response = {
        "status": True,
        "message": "Balance ledger retrieved",
        "data": [{"type": "credit", "amount": 50000}],
    }
    responses.add(
        responses.GET,
        f"{transfers_control_client.base_url}/balance/ledger",
        json=mock_response,
        status=200,
    )

    data, meta = transfers_control_client.fetch_balance_ledger()

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["type"] == "credit"
    assert data[0]["amount"] == 50000
    assert meta == {}


@responses.activate
def test_resend_otp(transfers_control_client):
    payload = {
        "transfer_code": "TRF_test",
        "reason": "resend_otp",
    }
    mock_response = {
        "status": True,
        "message": "OTP resent",
        "data": {"transfer_code": payload["transfer_code"]},
    }
    responses.add(
        responses.POST,
        f"{transfers_control_client.base_url}/transfer/resend_otp",
        json=mock_response,
        status=200,
    )

    data, meta = transfers_control_client.resend_otp(**payload)

    assert data["transfer_code"] == payload["transfer_code"]
    assert meta == {}


@responses.activate
def test_disable_otp(transfers_control_client):
    mock_response = {
        "status": True,
        "message": "OTP disable initiated",
        "data": {"status": "pending_validation"},
    }
    responses.add(
        responses.POST,
        f"{transfers_control_client.base_url}/transfer/disable_otp",
        json=mock_response,
        status=200,
    )

    data, meta = transfers_control_client.disable_otp()

    assert data["status"] == "pending_validation"
    assert meta == {}


@responses.activate
def test_finalize_disable_otp(transfers_control_client):
    otp = "123456"
    mock_response = {
        "status": True,
        "message": "OTP disable finalized",
        "data": {"status": "disabled"},
    }
    responses.add(
        responses.POST,
        f"{transfers_control_client.base_url}/transfer/disable_otp_finalize",
        json=mock_response,
        status=200,
    )

    data, meta = transfers_control_client.finalize_disable_otp(otp=otp)

    assert data["status"] == "disabled"
    assert meta == {}


@responses.activate
def test_enable_otp(transfers_control_client):
    mock_response = {
        "status": True,
        "message": "OTP enable successful",
        "data": {"status": "enabled"},
    }
    responses.add(
        responses.POST,
        f"{transfers_control_client.base_url}/transfer/enable_otp",
        json=mock_response,
        status=200,
    )

    data, meta = transfers_control_client.enable_otp()

    assert data["status"] == "enabled"
    assert meta == {}
