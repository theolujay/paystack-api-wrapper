"""
The Transfer Recipients API allows you create and manage beneficiaries that you send money to.
"""
from typing import Optional, List, Dict, Any

from .core import BaseClient, PaystackResponse


class TransferRecipientsAPI(BaseClient):
    """
    The Transfer Recipients API allows you create and manage beneficiaries that you send money to.
    """

    def __init__(self, secret_key: Optional[str] = None):
        super().__init__(secret_key)

    def create_transfer_recipient(self, type: str, name: str, account_number: Optional[str] = None, bank_code: Optional[str] = None, description: Optional[str] = None, currency: Optional[str] = None, authorization_code: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> PaystackResponse:
        """
        Creates a new recipient. A duplicate account number will lead to the retrieval of the existing record.

        Args:
            type: Recipient Type. It could be one of: nuban, ghipss, mobile_money or basa
            name: The recipient's name according to their account registration.
            account_number: Required for all recipient types except authorization
            bank_code: Required for all recipient types except authorization. You can get the list of Bank Codes by calling the List Banks endpoint.
            description: A description for this recipient
            currency: Currency for the account receiving the transfer
            authorization_code: An authorization code from a previous transaction
            metadata: Store additional information about your recipient in a structured format, JSON

        Returns:
            PaystackResponse: The response from the API
        """
        payload = {
            "type": type,
            "name": name,
        }
        if account_number:
            payload["account_number"] = account_number
        if bank_code:
            payload["bank_code"] = bank_code
        if description:
            payload["description"] = description
        if currency:
            payload["currency"] = currency
        if authorization_code:
            payload["authorization_code"] = authorization_code
        if metadata:
            payload["metadata"] = metadata

        return self.request("POST", "transferrecipient", json_data=payload)

    def bulk_create_transfer_recipient(self, batch: List[Dict[str, Any]]) -> PaystackResponse:
        """
        Create multiple transfer recipients in batches. A duplicate account number will lead to the retrieval of the existing record.

        Args:
            batch: A list of transfer recipient object. Each object should contain type, name, and bank_code. Any Create Transfer Recipient param can also be passed.

        Returns:
            PaystackResponse: The response from the API
        """
        payload = {"batch": batch}
        return self.request("POST", "transferrecipient/bulk", json_data=payload)

    def list_transfer_recipients(self, per_page: Optional[int] = None, page: Optional[int] = None, from_date: Optional[str] = None, to_date: Optional[str] = None) -> PaystackResponse:
        """
        List transfer recipients available on your integration

        Args:
            per_page: Specify how many records you want to retrieve per page. If not specify we use a default value of 50.
            page: Specify exactly what page you want to retrieve. If not specify we use a default value of 1.
            from_date: A timestamp from which to start listing transfer recipients e.g. 2016-09-24T00:00:05.000Z, 2016-09-21
            to_date: A timestamp at which to stop listing transfer recipients e.g. 2016-09-24T00:00:05.000Z, 2016-09-21

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

        return self.request("GET", "transferrecipient", params=params)

    def fetch_transfer_recipient(self, id_or_code: str) -> PaystackResponse:
        """
        Fetch the details of a transfer recipient

        Args:
            id_or_code: An ID or code for the recipient whose details you want to receive.

        Returns:
            PaystackResponse: The response from the API
        """
        return self.request("GET", f"transferrecipient/{id_or_code}")

    def update_transfer_recipient(self, id_or_code: str, name: Optional[str] = None, email: Optional[str] = None) -> PaystackResponse:
        """
        Update transfer recipients available on your integration

        Args:
            id_or_code: Transfer Recipient's ID or code
            name: A name for the recipient
            email: Email address of the recipient

        Returns:
            PaystackResponse: The response from the API
        """
        payload = {}
        if name:
            payload["name"] = name
        if email:
            payload["email"] = email

        return self.request("PUT", f"transferrecipient/{id_or_code}", json_data=payload)

    def delete_transfer_recipient(self, id_or_code: str) -> PaystackResponse:
        """
        Delete a transfer recipient (sets the transfer recipient to inactive)

        Args:
            id_or_code: An ID or code for the recipient who you want to delete.

        Returns:
            PaystackResponse: The response from the API
        """
        return self.request("DELETE", f"transferrecipient/{id_or_code}")
