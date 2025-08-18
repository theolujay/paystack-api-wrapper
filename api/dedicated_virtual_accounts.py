"""
The Dedicated Virtual Account API enables Nigerian and Ghanaian merchants to manage unique payment accounts of their customers.
"""
from typing import Optional, Dict, Any

from .core import BaseClient, PaystackResponse


class DedicatedVirtualAccountsAPI(BaseClient):
    """
    The Dedicated Virtual Account API enables Nigerian and Ghanaian merchants to manage unique payment accounts of their customers.
    """

    def __init__(self, secret_key: Optional[str] = None):
        super().__init__(secret_key)

    def create_dedicated_virtual_account(self, customer: str, preferred_bank: Optional[str] = None, subaccount: Optional[str] = None, split_code: Optional[str] = None, first_name: Optional[str] = None, last_name: Optional[str] = None, phone: Optional[str] = None) -> PaystackResponse:
        """
        Create a dedicated virtual account for an existing customer

        Args:
            customer: Customer ID or code
            preferred_bank: The bank slug for preferred bank. To get a list of available banks, use the List Providers endpoint.
            subaccount: Subaccount code of the account you want to split the transaction with
            split_code: Split code consisting of the lists of accounts you want to split the transaction with
            first_name: Customer's first name
            last_name: Customer's last name
            phone: Customer's phone number

        Returns:
            PaystackResponse: The response from the API
        """
        payload = {"customer": customer}
        if preferred_bank:
            payload["preferred_bank"] = preferred_bank
        if subaccount:
            payload["subaccount"] = subaccount
        if split_code:
            payload["split_code"] = split_code
        if first_name:
            payload["first_name"] = first_name
        if last_name:
            payload["last_name"] = last_name
        if phone:
            payload["phone"] = phone

        return self.request("POST", "dedicated_account", json_data=payload)

    def assign_dedicated_virtual_account(self, email: str, first_name: str, last_name: str, phone: str, preferred_bank: str, country: str, account_number: Optional[str] = None, bvn: Optional[str] = None, bank_code: Optional[str] = None, subaccount: Optional[str] = None, split_code: Optional[str] = None) -> PaystackResponse:
        """
        With this endpoint, you can create a customer, validate the customer, and assign a DVA to the customer.

        Args:
            email: Customer email address
            first_name: Customer's first name
            last_name: Customer's last name
            phone: Customer's phone number
            preferred_bank: The bank slug for preferred bank. To get a list of available banks, use the List Providers endpoint.
            country: Currently accepts NG and GH only
            account_number: Customer's account number
            bvn: Customer's Bank Verification Number (Nigeria only)
            bank_code: Customer's bank code
            subaccount: Subaccount code of the account you want to split the transaction with
            split_code: Split code consisting of the lists of accounts you want to split the transaction with

        Returns:
            PaystackResponse: The response from the API
        """
        payload = {
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "phone": phone,
            "preferred_bank": preferred_bank,
            "country": country,
        }
        if account_number:
            payload["account_number"] = account_number
        if bvn:
            payload["bvn"] = bvn
        if bank_code:
            payload["bank_code"] = bank_code
        if subaccount:
            payload["subaccount"] = subaccount
        if split_code:
            payload["split_code"] = split_code

        return self.request("POST", "dedicated_account/assign", json_data=payload)

    def list_dedicated_virtual_accounts(self, active: Optional[bool] = None, currency: Optional[str] = None, provider_slug: Optional[str] = None, bank_id: Optional[str] = None, customer: Optional[str] = None) -> PaystackResponse:
        """
        List dedicated virtual accounts available on your integration.

        Args:
            active: Status of the dedicated virtual account
            currency: The currency of the dedicated virtual account. Only NGN and GHS are currently allowed
            provider_slug: The bank's slug in lowercase, without spaces e.g. wema-bank
            bank_id: The bank's ID e.g. 035
            customer: The customer's ID

        Returns:
            PaystackResponse: The response from the API
        """
        params = {}
        if active is not None:
            params["active"] = active
        if currency:
            params["currency"] = currency
        if provider_slug:
            params["provider_slug"] = provider_slug
        if bank_id:
            params["bank_id"] = bank_id
        if customer:
            params["customer"] = customer

        return self.request("GET", "dedicated_account", params=params)

    def fetch_dedicated_virtual_account(self, dedicated_account_id: int) -> PaystackResponse:
        """
        Get details of a dedicated virtual account on your integration.

        Args:
            dedicated_account_id: ID of dedicated virtual account

        Returns:
            PaystackResponse: The response from the API
        """
        return self.request("GET", f"dedicated_account/{dedicated_account_id}")

    def requery_dedicated_account(self, account_number: str, provider_slug: str, date: Optional[str] = None) -> PaystackResponse:
        """
        Requery Dedicated Virtual Account for new transactions

        Args:
            account_number: Virtual account number to requery
            provider_slug: The bank's slug in lowercase, without spaces e.g. wema-bank
            date: The day the transfer was made in YYYY-MM-DD format

        Returns:
            PaystackResponse: The response from the API
        """
        params = {
            "account_number": account_number,
            "provider_slug": provider_slug,
        }
        if date:
            params["date"] = date

        return self.request("GET", "dedicated_account/requery", params=params)

    def deactivate_dedicated_account(self, dedicated_account_id: int) -> PaystackResponse:
        """
        Deactivate a dedicated virtual account on your integration.

        Args:
            dedicated_account_id: ID of dedicated virtual account

        Returns:
            PaystackResponse: The response from the API
        """
        return self.request("DELETE", f"dedicated_account/{dedicated_account_id}")

    def split_dedicated_account_transaction(self, customer: str, subaccount: Optional[str] = None, split_code: Optional[str] = None, preferred_bank: Optional[str] = None) -> PaystackResponse:
        """
        Split a dedicated virtual account transaction with one or more accounts

        Args:
            customer: Customer ID or code
            subaccount: Subaccount code of the account you want to split the transaction with
            split_code: Split code consisting of the lists of accounts you want to split the transaction with
            preferred_bank: The bank slug for preferred bank. To get a list of available banks, use the List Providers endpoint

        Returns:
            PaystackResponse: The response from the API
        """
        payload = {"customer": customer}
        if subaccount:
            payload["subaccount"] = subaccount
        if split_code:
            payload["split_code"] = split_code
        if preferred_bank:
            payload["preferred_bank"] = preferred_bank

        return self.request("POST", "dedicated_account/split", json_data=payload)

    def remove_split_from_dedicated_account(self, account_number: str) -> PaystackResponse:
        """
        If you've previously set up split payment for transactions on a dedicated virtual account, you can remove it with this endpoint

        Args:
            account_number: Dedicated virtual account number

        Returns:
            PaystackResponse: The response from the API
        """
        payload = {"account_number": account_number}
        return self.request("DELETE", "dedicated_account/split", json_data=payload)

    def fetch_bank_providers(self) -> PaystackResponse:
        """
        Get available bank providers for a dedicated virtual account

        Returns:
            PaystackResponse: The response from the API
        """
        return self.request("GET", "dedicated_account/available_providers")
