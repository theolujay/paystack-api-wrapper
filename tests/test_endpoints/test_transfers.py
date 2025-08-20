import pytest
import responses
import json
import requests

from paystack import (
    NetworkError,
    ValidationError,
    AuthenticationError,
    NotFoundError,
    ServerError,
)


class TestInitiateTransfer:
    def setup_mock_response(self, client, response_data=None, status_code=200):
        if response_data is None:
            response_data = {
                "status": True,
                "message": "Transfer initiated",
                "data": {
                    "domain": "test",
                    "amount": 500000,
                    "currency": "NGN",
                    "source": "balance",
                    "reason": "Salary payment",
                    "recipient": 12345,
                    "status": "pending",
                    "transfer_code": "TRF_testcode",
                    "id": 123456,
                    "createdAt": "2024-01-01T00:00:00.000Z",
                    "updatedAt": "2024-01-01T00:00:00.000Z",
                },
            }
        responses.add(
            responses.POST,
            f"{client.base_url}/transfer",
            json=response_data,
            status=status_code,
        )

    @responses.activate
    def test_initiate_transfer_success(self, transfers_client):
        payload = {
            "source": "balance",
            "amount": 500000,
            "recipient": "REC_abcdefg",
            "reason": "Salary payment",
            "currency": "NGN",
            "reference": "my_unique_ref",
        }
        self.setup_mock_response(transfers_client)

        data, meta = transfers_client.initiate_transfer(**payload)

        assert data["transfer_code"] == "TRF_testcode"
        assert data["amount"] == 500000
        assert data["status"] == "pending"
        assert responses.calls[0].request.method == "POST"
        assert json.loads(responses.calls[0].request.body) == payload

    def test_initiate_transfer_missing_required_fields(self, transfers_client):
        with pytest.raises(
            TypeError, match="missing 1 required positional argument: 'recipient'"
        ):
            transfers_client.initiate_transfer(source="balance", amount=100)

    @responses.activate
    def test_initiate_transfer_api_error(self, transfers_client):
        payload = {
            "source": "balance",
            "amount": 500000,
            "recipient": "REC_abcdefg",
        }
        self.setup_mock_response(
            transfers_client,
            response_data={
                "status": False,
                "message": "Invalid amount",
                "errors": {"amount": "Amount too low"},
            },
            status_code=400,
        )
        with pytest.raises(ValidationError) as excinfo:
            transfers_client.initiate_transfer(**payload)
        assert "Invalid amount" in str(excinfo.value)
        assert "amount: Amount too low" in str(excinfo.value)

    @responses.activate
    def test_initiate_transfer_network_error(self, transfers_client):
        payload = {
            "source": "balance",
            "amount": 500000,
            "recipient": "REC_abcdefg",
        }
        responses.add(
            responses.POST,
            f"{transfers_client.base_url}/transfer",
            body=requests.exceptions.ConnectionError("Connection refused"),
        )
        with pytest.raises(NetworkError) as excinfo:
            transfers_client.initiate_transfer(**payload)
        assert "Connection refused" in str(excinfo.value)


class TestFinalizeTransfer:
    def setup_mock_response(self, client, response_data=None, status_code=200):
        if response_data is None:
            response_data = {
                "status": True,
                "message": "Transfer finalized",
                "data": {
                    "transfer_code": "TRF_testcode",
                    "status": "success",
                },
            }
        responses.add(
            responses.POST,
            f"{client.base_url}/transfer/finalize_transfer",
            json=response_data,
            status=status_code,
        )

    @responses.activate
    def test_finalize_transfer_success(self, transfers_client):
        payload = {"transfer_code": "TRF_testcode", "otp": "123456"}
        self.setup_mock_response(transfers_client)

        data, meta = transfers_client.finalize_transfer(**payload)

        assert data["status"] == "success"
        assert data["transfer_code"] == "TRF_testcode"
        assert responses.calls[0].request.method == "POST"
        assert json.loads(responses.calls[0].request.body) == payload

    def test_finalize_transfer_missing_required_fields(self, transfers_client):
        with pytest.raises(
            TypeError, match="missing 1 required positional argument: 'otp'"
        ):
            transfers_client.finalize_transfer(transfer_code="TRF_testcode")

    @responses.activate
    def test_finalize_transfer_api_error(self, transfers_client):
        payload = {"transfer_code": "TRF_testcode", "otp": "123456"}
        self.setup_mock_response(
            transfers_client,
            response_data={
                "status": False,
                "message": "Invalid OTP",
            },
            status_code=400,
        )
        with pytest.raises(ValidationError) as excinfo:
            transfers_client.finalize_transfer(**payload)
        assert "Invalid OTP" in str(excinfo.value)


class TestInitiateBulkTransfer:
    def setup_mock_response(self, client, response_data=None, status_code=200):
        if response_data is None:
            response_data = {
                "status": True,
                "message": "Bulk transfer initiated",
                "data": {"bulk_transfer_code": "BLK_testcode"},
            }
        responses.add(
            responses.POST,
            f"{client.base_url}/transfer/bulk",
            json=response_data,
            status=status_code,
        )

    @responses.activate
    def test_initiate_bulk_transfer_success(self, transfers_client):
        payload = {
            "source": "balance",
            "transfers": [
                {"amount": 10000, "recipient": "REC_abc"},
                {"amount": 20000, "recipient": "REC_def"},
            ],
        }
        self.setup_mock_response(transfers_client)

        data, meta = transfers_client.initiate_bulk_transfer(**payload)

        assert data["bulk_transfer_code"] == "BLK_testcode"
        assert responses.calls[0].request.method == "POST"
        assert json.loads(responses.calls[0].request.body) == payload

    def test_initiate_bulk_transfer_missing_required_fields(self, transfers_client):
        with pytest.raises(
            TypeError, match="missing 1 required positional argument: 'transfers'"
        ):
            transfers_client.initiate_bulk_transfer(source="balance")

    @responses.activate
    def test_initiate_bulk_transfer_api_error(self, transfers_client):
        payload = {
            "source": "balance",
            "transfers": [
                {"amount": 10000, "recipient": "REC_abc"},
            ],
        }
        self.setup_mock_response(
            transfers_client,
            response_data={
                "status": False,
                "message": "Invalid bulk transfer data",
            },
            status_code=400,
        )
        with pytest.raises(ValidationError) as excinfo:
            transfers_client.initiate_bulk_transfer(**payload)
        assert "Invalid bulk transfer data" in str(excinfo.value)


class TestListTransfers:
    def setup_mock_response(self, client, response_data=None, status_code=200):
        if response_data is None:
            response_data = {
                "status": True,
                "message": "Transfers retrieved",
                "data": [
                    {"id": 1, "amount": 10000},
                    {"id": 2, "amount": 20000},
                ],
                "meta": {"total": 2, "page": 1, "perPage": 50},
            }
        responses.add(
            responses.GET,
            f"{client.base_url}/transfer",
            json=response_data,
            status=status_code,
        )

    @responses.activate
    def test_list_transfers_success(self, transfers_client):
        self.setup_mock_response(transfers_client)

        data, meta = transfers_client.list_transfers()

        assert len(data) == 2
        assert data[0]["amount"] == 10000
        assert meta["total"] == 2
        assert responses.calls[0].request.method == "GET"
        assert responses.calls[0].request.url == f"{transfers_client.base_url}/transfer"

    @responses.activate
    def test_list_transfers_with_params(self, transfers_client):
        self.setup_mock_response(transfers_client)

        data, meta = transfers_client.list_transfers(
            per_page=10,
            page=2,
            recipient=123,
            from_date="2023-01-01",
            to_date="2023-01-31",
        )

        assert len(data) == 2
        assert responses.calls[0].request.method == "GET"
        expected_url = (
            f"{transfers_client.base_url}/transfer?perPage=10&page=2&recipient=123"
            "&from=2023-01-01&to=2023-01-31"
        )
        assert responses.calls[0].request.url == expected_url

    @responses.activate
    def test_list_transfers_authentication_error(self, transfers_client):
        self.setup_mock_response(
            transfers_client,
            response_data={
                "status": False,
                "message": "Invalid API key",
            },
            status_code=401,
        )
        with pytest.raises(AuthenticationError) as excinfo:
            transfers_client.list_transfers()
        assert "Invalid API key" in str(excinfo.value)


class TestFetchTransfer:
    def setup_mock_response(
        self, client, id_or_code, response_data=None, status_code=200
    ):
        if response_data is None:
            response_data = {
                "status": True,
                "message": "Transfer retrieved",
                "data": {"id": 123, "transfer_code": id_or_code, "amount": 50000},
            }
        responses.add(
            responses.GET,
            f"{client.base_url}/transfer/{id_or_code}",
            json=response_data,
            status=status_code,
        )

    @responses.activate
    def test_fetch_transfer_success(self, transfers_client):
        id_or_code = "TRF_testcode"
        self.setup_mock_response(transfers_client, id_or_code)

        data, meta = transfers_client.fetch_transfer(id_or_code=id_or_code)

        assert data["transfer_code"] == id_or_code
        assert data["amount"] == 50000
        assert responses.calls[0].request.method == "GET"
        assert (
            responses.calls[0].request.url
            == f"{transfers_client.base_url}/transfer/{id_or_code}"
        )

    def test_fetch_transfer_missing_required_fields(self, transfers_client):
        with pytest.raises(TypeError, match="id_or_code"):
            transfers_client.fetch_transfer()

    @responses.activate
    def test_fetch_transfer_not_found_error(self, transfers_client):
        id_or_code = "TRF_nonexistent"
        self.setup_mock_response(
            transfers_client,
            id_or_code,
            response_data={
                "status": False,
                "message": "Transfer not found",
            },
            status_code=404,
        )
        with pytest.raises(NotFoundError) as excinfo:
            transfers_client.fetch_transfer(id_or_code=id_or_code)
        assert "Transfer not found" in str(excinfo.value)


class TestVerifyTransfer:
    def setup_mock_response(
        self, client, reference, response_data=None, status_code=200
    ):
        if response_data is None:
            response_data = {
                "status": True,
                "message": "Transfer verified",
                "data": {"id": 123, "reference": reference, "status": "success"},
            }
        responses.add(
            responses.GET,
            f"{client.base_url}/transfer/verify/{reference}",
            json=response_data,
            status=status_code,
        )

    @responses.activate
    def test_verify_transfer_success(self, transfers_client):
        reference = "REF_testref"
        self.setup_mock_response(transfers_client, reference)

        data, meta = transfers_client.verify_transfer(reference=reference)

        assert data["reference"] == reference
        assert data["status"] == "success"
        assert responses.calls[0].request.method == "GET"
        assert (
            responses.calls[0].request.url
            == f"{transfers_client.base_url}/transfer/verify/{reference}"
        )

    def test_verify_transfer_missing_required_fields(self, transfers_client):
        with pytest.raises(TypeError, match="reference"):
            transfers_client.verify_transfer()

    @responses.activate
    def test_verify_transfer_server_error(self, transfers_client):
        reference = "REF_testref"
        self.setup_mock_response(
            transfers_client,
            reference,
            response_data={
                "status": False,
                "message": "Server error",
            },
            status_code=500,
        )
        with pytest.raises(ServerError) as excinfo:
            transfers_client.verify_transfer(reference=reference)
        assert "Server error" in str(excinfo.value)
