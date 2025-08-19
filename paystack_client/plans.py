"""
The Plans API allows you create and manage installment payment options on your integration.
"""

from typing import Optional, Dict, Any, Tuple, Union

from .core import BaseClient


class PlansAPI(BaseClient):
    """
    The Plans API allows you create and manage installment payment options on your integration.
    """

    def __init__(self, secret_key: Optional[str] = None):
        super().__init__(secret_key)

    def create_plan(
        self,
        name: str,
        amount: Union[int, str],
        interval: str,
        description: Optional[str] = None,
        send_invoices: Optional[bool] = None,
        send_sms: Optional[bool] = None,
        currency: Optional[str] = None,
        invoice_limit: Optional[int] = None,
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Create a plan on your integration

        Args:
            name: Name of plan
            amount: Amount should be in the subunit of the supported currency
            interval: Interval in words. Valid intervals are: daily, weekly, monthly,quarterly, biannually (every 6 months), annually.
            description: A description for this plan
            send_invoices: Set to false if you don't want invoices to be sent to your customers
            send_sms: Set to false if you don't want text messages to be sent to your customers
            currency: Currency in which amount is set
            invoice_limit: Number of invoices to raise during subscription to this plan. Can be overridden by specifying an invoice_limit while subscribing.

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        payload = {
            "name": name,
            "amount": amount,
            "interval": interval,
        }
        if description:
            payload["description"] = description
        if send_invoices is not None:
            payload["send_invoices"] = send_invoices
        if send_sms is not None:
            payload["send_sms"] = send_sms
        if currency:
            payload["currency"] = currency
        if invoice_limit:
            payload["invoice_limit"] = invoice_limit

        return self.request("POST", "plan", json_data=payload)

    def list_plans(
        self,
        per_page: Optional[int] = None,
        page: Optional[int] = None,
        status: Optional[str] = None,
        interval: Optional[str] = None,
        amount: Optional[Union[int, str]] = None,
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        List plans available on your integration

        Args:
            per_page: Specify how many records you want to retrieve per page. If not specify we use a default value of 50.
            page: Specify exactly what page you want to retrieve. If not specify we use a default value of 1.
            status: Filter list by plans with specified status
            interval: Filter list by plans with specified interval
            amount: Filter list by plans with specified amount using the supported currency

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        params = {}
        if per_page:
            params["perPage"] = per_page
        if page:
            params["page"] = page
        if status:
            params["status"] = status
        if interval:
            params["interval"] = interval
        if amount:
            params["amount"] = amount

        return self.request("GET", "plan", params=params)

    def fetch_plan(self, id_or_code: str) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Get details of a plan on your integration

        Args:
            id_or_code: The plan ID or code you want to fetch

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        return self.request("GET", f"plan/{id_or_code}")

    def update_plan(
        self,
        id_or_code: str,
        name: Optional[str] = None,
        amount: Optional[Union[int, str]] = None,
        interval: Optional[str] = None,
        description: Optional[str] = None,
        send_invoices: Optional[bool] = None,
        send_sms: Optional[bool] = None,
        currency: Optional[str] = None,
        invoice_limit: Optional[int] = None,
        update_existing_subscriptions: Optional[bool] = None,
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Update a plan details on your integration

        Args:
            id_or_code: Plan's ID or code
            name: Name of plan
            amount: Amount should be in the subunit of the supported currency
            interval: Interval in words. Valid intervals are hourly, daily, weekly, monthly,quarterly, biannually (every 6 months), annually.
            description: A description for this plan
            send_invoices: Set to false if you don't want invoices to be sent to your customers
            send_sms: Set to false if you don't want text messages to be sent to your customers
            currency: Currency in which amount is set
            invoice_limit: Number of invoices to raise during subscription to this plan. Can be overridden by specifying an invoice_limit while subscribing.
            update_existing_subscriptions: Set to true if you want the existing subscriptions to use the new changes. Set to false and only new subscriptions will be changed. Defaults to true when not set.

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        payload = {}
        if name:
            payload["name"] = name
        if amount:
            payload["amount"] = amount
        if interval:
            payload["interval"] = interval
        if description:
            payload["description"] = description
        if send_invoices is not None:
            payload["send_invoices"] = send_invoices
        if send_sms is not None:
            payload["send_sms"] = send_sms
        if currency:
            payload["currency"] = currency
        if invoice_limit:
            payload["invoice_limit"] = invoice_limit
        if update_existing_subscriptions is not None:
            payload["update_existing_subscriptions"] = update_existing_subscriptions

        return self.request("PUT", f"plan/{id_or_code}", json_data=payload)
