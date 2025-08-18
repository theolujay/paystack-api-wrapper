"""
The Transfers Control API allows you manage settings of your transfers.
"""
from typing import Optional

from .core import BaseClient, PaystackResponse


class TransfersControlAPI(BaseClient):
    """
    The Transfers Control API allows you manage settings of your transfers.
    """

    def __init__(self, secret_key: Optional[str] = None):
        super().__init__(secret_key)

    def check_balance(self) -> PaystackResponse:
        """
        Fetch the available balance on your integration

        Returns:
            PaystackResponse: The response from the API
        """
        return self.request("GET", "balance")

    def fetch_balance_ledger(self) -> PaystackResponse:
        """
        Fetch all pay-ins and pay-outs that occured on your integration

        Returns:
            PaystackResponse: The response from the API
        """
        return self.request("GET", "balance/ledger")

    def resend_otp(self, transfer_code: str, reason: str) -> PaystackResponse:
        """
        Generates a new OTP and sends to customer in the event they are having trouble receiving one.

        Args:
            transfer_code: Transfer code
            reason: Either resend_otp or transfer

        Returns:
            PaystackResponse: The response from the API
        """
        self._validate_required_params(transfer_code=transfer_code, reason=reason)
        payload = {
            "transfer_code": transfer_code,
            "reason": reason,
        }
        return self.request("POST", "transfer/resend_otp", json_data=payload)

    def disable_otp(self) -> PaystackResponse:
        """
        This is used in the event that you want to be able to complete transfers programmatically without use of OTPs. No arguments required. You will get an OTP to complete the request.

        Returns:
            PaystackResponse: The response from the API
        """
        return self.request("POST", "transfer/disable_otp")

    def finalize_disable_otp(self, otp: str) -> PaystackResponse:
        """
        Finalize the request to disable OTP on your transfers.

        Args:
            otp: OTP sent to business phone to verify disabling OTP requirement

        Returns:
            PaystackResponse: The response from the API
        """
        self._validate_required_params(otp=otp)
        payload = {"otp": otp}
        return self.request("POST", "transfer/disable_otp_finalize", json_data=payload)

    def enable_otp(self) -> PaystackResponse:
        """
        In the event that a customer wants to stop being able to complete transfers programmatically, this endpoint helps turn OTP requirement back on. No arguments required.

        Returns:
            PaystackResponse: The response from the API
        """
        return self.request("POST", "transfer/enable_otp")
