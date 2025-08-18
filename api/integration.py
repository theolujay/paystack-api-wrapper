"""
The Integration API allows you manage some settings on your integration.
"""
from typing import Optional

from .core import BaseClient, PaystackResponse


class IntegrationAPI(BaseClient):
    """
    The Integration API allows you manage some settings on your integration.
    """

    def __init__(self, secret_key: Optional[str] = None):
        super().__init__(secret_key)

    def fetch_timeout(self) -> PaystackResponse:
        """
        Fetch the payment session timeout on your integration

        Returns:
            PaystackResponse: The response from the API
        """
        return self.request("GET", "integration/payment_session_timeout")

    def update_timeout(self, timeout: int) -> PaystackResponse:
        """
        Update the payment session timeout on your integration

        Args:
            timeout: Time before stopping session (in seconds). Set to 0 to cancel session timeouts

        Returns:
            PaystackResponse: The response from the API
        """
        self._validate_required_params(timeout=timeout)
        payload = {"timeout": timeout}
        return self.request("PUT", "integration/payment_session_timeout", json_data=payload)
