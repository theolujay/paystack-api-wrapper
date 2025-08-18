"""
The Apple Pay API allows you register your application's top-level domain or subdomain.
"""
from typing import Optional

from .core import BaseClient, PaystackResponse


class ApplePayAPI(BaseClient):
    """
    The Apple Pay API allows you register your application's top-level domain or subdomain.
    """

    def __init__(self, secret_key: Optional[str] = None):
        super().__init__(secret_key)

    def register_domain(self, domain_name: str) -> PaystackResponse:
        """
        Register a top-level domain or subdomain for your Apple Pay integration.

        Args:
            domain_name: Domain name to be registered

        Returns:
            PaystackResponse: The response from the API
        """
        payload = {"domainName": domain_name}
        return self.request("POST", "apple-pay/domain", json_data=payload)

    def list_domains(self, use_cursor: Optional[bool] = None, next_cursor: Optional[str] = None, previous_cursor: Optional[str] = None) -> PaystackResponse:
        """
        Lists all registered domains on your integration. Returns an empty array if no domains have been added.

        Args:
            use_cursor: Flag to enable cursor pagination on the endpoint
            next_cursor: A cursor that indicates your place in the list. It can be used to fetch the next page of the list
            previous_cursor: A cursor that indicates your place in the list. It should be used to fetch the previous page of the list after an intial next request

        Returns:
            PaystackResponse: The response from the API
        """
        params = {}
        if use_cursor is not None:
            params["use_cursor"] = use_cursor
        if next_cursor:
            params["next"] = next_cursor
        if previous_cursor:
            params["previous"] = previous_cursor

        return self.request("GET", "apple-pay/domain", params=params)

    def unregister_domain(self, domain_name: str) -> PaystackResponse:
        """
        Unregister a top-level domain or subdomain previously used for your Apple Pay integration.

        Args:
            domain_name: Domain name to be registered

        Returns:
            PaystackResponse: The response from the API
        """
        payload = {"domainName": domain_name}
        return self.request("DELETE", "apple-pay/domain", json_data=payload)
