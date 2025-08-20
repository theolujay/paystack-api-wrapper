"""
The Apple Pay API allows you register your application's top-level domain or subdomain.
"""

import requests
from typing import Optional, Dict, Any, Tuple

from ..core import BaseClient


class ApplePayAPI(BaseClient):
    """
    The Apple Pay API allows you register your application's top-level domain or subdomain.
    """

    def __init__(
        self, secret_key: str, session: requests.Session = None, base_url: str = None
    ):
        super().__init__(secret_key, session=session, base_url=base_url)

    def register_domain(
        self, domain_name: str
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Register a top-level domain or subdomain for your Apple Pay integration.

        Args:
            domain_name: Domain name to be registered

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        payload = {"domainName": domain_name}
        return self.request("POST", "apple-pay/domain", json_data=payload)

    def list_domains(
        self,
        use_cursor: Optional[bool] = None,
        next_cursor: Optional[str] = None,
        previous_cursor: Optional[str] = None,
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Lists all registered domains on your integration. Returns an empty array if no domains have been added.

        Args:
            use_cursor: Flag to enable cursor pagination on the endpoint
            next_cursor: A cursor that indicates your place in the list. It can be used to fetch the next page of the list
            previous_cursor: A cursor that indicates your place in the list. It should be used to fetch the previous page of the list after an intial next request

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        params = {}
        if use_cursor is not None:
            params["use_cursor"] = use_cursor
        if next_cursor:
            params["next"] = next_cursor
        if previous_cursor:
            params["previous"] = previous_cursor

        return self.request("GET", "apple-pay/domain", params=params)

    def unregister_domain(
        self, domain_name: str
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Unregister a top-level domain or subdomain previously used for your Apple Pay integration.

        Args:
            domain_name: Domain name to be registered

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        payload = {"domainName": domain_name}
        return self.request("DELETE", "apple-pay/domain", json_data=payload)
