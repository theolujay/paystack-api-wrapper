"""
The Integration API allows you manage some settings on your integration.
"""
from typing import Optional, Dict, Any, Tuple

from .core import BaseClient


class IntegrationAPI(BaseClient):
    """
    The Integration API allows you manage some settings on your integration.
    """

    def __init__(self, secret_key: Optional[str] = None):
        super().__init__(secret_key)

    def fetch_timeout(self) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Fetch the payment session timeout on your integration

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        return self.request("GET", "integration/payment_session_timeout")

    def update_timeout(self, timeout: int) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Update the payment session timeout on your integration

        Args:
            timeout: Time before stopping session (in seconds). Set to 0 to cancel session timeouts

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        self._validate_required_params(timeout=timeout)
        payload = {"timeout": timeout}
        return self.request("PUT", "integration/payment_session_timeout", json_data=payload)
