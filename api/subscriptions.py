"""
The Subscriptions API allows you create and manage recurring payment on your integration.
"""

from typing import Optional, Dict, Any, Tuple

from .core import BaseClient


class SubscriptionsAPI(BaseClient):
    """
    The Subscriptions API allows you create and manage recurring payment on your integration.
    """

    def __init__(self, secret_key: Optional[str] = None):
        super().__init__(secret_key)

    def create_subscription(
        self,
        customer: str,
        plan: str,
        authorization: Optional[str] = None,
        start_date: Optional[str] = None,
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Create a subscription on your integration

        Args:
            customer: Customer's email address or customer code
            plan: Plan code
            authorization: If customer has multiple authorizations, you can set the desired authorization you wish to use for this subscription here. If this is not supplied, the customer's most recent authorization would be used
            start_date: Set the date for the first debit. (ISO 8601 format) e.g. 2017-05-16T00:30:13+01:00

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        payload = {
            "customer": customer,
            "plan": plan,
        }
        if authorization:
            payload["authorization"] = authorization
        if start_date:
            payload["start_date"] = start_date

        return self.request("POST", "subscription", json_data=payload)

    def list_subscriptions(
        self,
        per_page: Optional[int] = None,
        page: Optional[int] = None,
        customer: Optional[int] = None,
        plan: Optional[int] = None,
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        List subscriptions available on your integration

        Args:
            per_page: Specify how many records you want to retrieve per page. If not specify we use a default value of 50.
            page: Specify exactly what page you want to retrieve. If not specify we use a default value of 1.
            customer: Filter by Customer ID
            plan: Filter by Plan ID

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        params = {}
        if per_page:
            params["perPage"] = per_page
        if page:
            params["page"] = page
        if customer:
            params["customer"] = customer
        if plan:
            params["plan"] = plan

        return self.request("GET", "subscription", params=params)

    def fetch_subscription(
        self, id_or_code: str
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Get details of a subscription on your integration

        Args:
            id_or_code: The subscription ID or code you want to fetch

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        return self.request("GET", f"subscription/{id_or_code}")

    def enable_subscription(
        self, code: str, token: str
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Enable a subscription on your integration

        Args:
            code: Subscription code
            token: Email token

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        payload = {
            "code": code,
            "token": token,
        }
        return self.request("POST", "subscription/enable", json_data=payload)

    def disable_subscription(
        self, code: str, token: str
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Disable a subscription on your integration

        Args:
            code: Subscription code
            token: Email token

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        payload = {
            "code": code,
            "token": token,
        }
        return self.request("POST", "subscription/disable", json_data=payload)

    def generate_update_subscription_link(
        self, code: str
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Generate a link for updating the card on a subscription

        Args:
            code: Subscription code

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        return self.request("GET", f"subscription/{code}/manage/link")

    def send_update_subscription_link(
        self, code: str
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Email a customer a link for updating the card on their subscription

        Args:
            code: Subscription code

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        return self.request("POST", f"subscription/{code}/manage/email")
