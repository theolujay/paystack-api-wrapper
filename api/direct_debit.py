"""
The Direct Debit API allows you manage the authorization on your customer's bank accounts.
"""
from typing import Optional, List

from .core import BaseClient, PaystackResponse


class DirectDebitAPI(BaseClient):
    """
    The Direct Debit API allows you manage the authorization on your customer's bank accounts.
    """

    def __init__(self, secret_key: Optional[str] = None):
        super().__init__(secret_key)

    def trigger_activation_charge(self, customer_ids: List[int]) -> PaystackResponse:
        """
        Trigger an activation charge on pending mandates on behalf of your customers.

        Args:
            customer_ids: An array of customer IDs with pending mandate authorizations.

        Returns:
            PaystackResponse: The response from the API
        """
        payload = {"customer_ids": customer_ids}
        return self.request("PUT", "directdebit/activation-charge", json_data=payload)

    def list_mandate_authorizations(self, cursor: Optional[str] = None, status: Optional[str] = None, per_page: Optional[int] = None) -> PaystackResponse:
        """
        Get the list of direct debit mandates on your integration.

        Args:
            cursor: The cursor value of the next set of authorizations to fetch. You can get this from the meta object of the response
            status: Filter by the authorization status. Accepted values are: pending, active, revoked
            per_page: The number of authorizations to fetch per request

        Returns:
            PaystackResponse: The response from the API
        """
        params = {}
        if cursor:
            params["cursor"] = cursor
        if status:
            params["status"] = status
        if per_page:
            params["per_page"] = per_page

        return self.request("GET", "directdebit/mandate-authorizations", params=params)
