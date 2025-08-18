"""
The Settlements API allows you gain insights into payouts made by Paystack to your bank account.
"""
from typing import Optional

from .core import BaseClient, PaystackResponse


class SettlementsAPI(BaseClient):
    """
    The Settlements API allows you gain insights into payouts made by Paystack to your bank account.
    """

    def __init__(self, secret_key: Optional[str] = None):
        super().__init__(secret_key)

    def list_settlements(self, per_page: Optional[int] = None, page: Optional[int] = None, status: Optional[str] = None, subaccount: Optional[str] = None, from_date: Optional[str] = None, to_date: Optional[str] = None) -> PaystackResponse:
        """
        List settlements made to your settlement accounts

        Args:
            per_page: Specify how many records you want to retrieve per page. If not specify we use a default value of 50.
            page: Specify exactly what page you want to retrieve. If not specify we use a default value of 1.
            status: Fetch settlements based on their state. Value can be one of success, processing, pending or failed.
            subaccount: Provide a subaccount ID to export only settlements for that subaccount. Set to none to export only transactions for the account.
            from_date: A timestamp from which to start listing settlements e.g. 2016-09-24T00:00:05.000Z, 2016-09-21
            to_date: A timestamp at which to stop listing settlements e.g. 2016-09-24T00:00:05.000Z, 2016-09-21

        Returns:
            PaystackResponse: The response from the API
        """
        params = {}
        if per_page:
            params["perPage"] = per_page
        if page:
            params["page"] = page
        if status:
            params["status"] = status
        if subaccount:
            params["subaccount"] = subaccount
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date

        return self.request("GET", "settlement", params=params)

    def list_settlement_transactions(self, settlement_id: str, per_page: Optional[int] = None, page: Optional[int] = None, from_date: Optional[str] = None, to_date: Optional[str] = None) -> PaystackResponse:
        """
        Get the transactions that make up a particular settlement

        Args:
            settlement_id: The settlement ID in which you want to fetch its transactions
            per_page: Specify how many records you want to retrieve per page. If not specify we use a default value of 50.
            page: Specify exactly what page you want to retrieve. If not specify we use a default value of 1.
            from_date: A timestamp from which to start listing settlement transactions e.g. 2016-09-24T00:00:05.000Z, 2016-09-21
            to_date: A timestamp at which to stop listing settlement transactions e.g. 2016-09-24T00:00:05.000Z, 2016-09-21

        Returns:
            PaystackResponse: The response from the API
        """
        params = {}
        if per_page:
            params["perPage"] = per_page
        if page:
            params["page"] = page
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date

        return self.request("GET", f"settlement/{settlement_id}/transactions", params=params)
