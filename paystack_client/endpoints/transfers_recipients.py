"""
The Transfer Recipients API allows you create and manage beneficiaries that you send money to.
"""

import requests
from typing import Optional, List, Dict, Any, Tuple

from ..core import BaseClient


class TransferRecipientsAPI(BaseClient):
    """
    The Transfer Recipients API allows you create and manage beneficiaries that you send money to.
    """

    def __init__(self, secret_key: str, session: requests.Session = None, base_url: str = None):
        super().__init__(secret_key, session=session, base_url=base_url)

    def create_transfer_recipient(
        self,
        type: str,
        name: str,
        account_number: Optional[str] = None,
        bank_code: Optional[str] = None,
        description: Optional[str] = None,
        currency: Optional[str] = None,
        authorization_code: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
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
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
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

    def bulk_create_transfer_recipient(
        self, batch: List[Dict[str, Any]]
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Create multiple transfer recipients in batches. A duplicate account number will lead to the retrieval of the existing record.

        Args:
            batch: A list of transfer recipient object. Each object should contain type, name, and bank_code. Any Create Transfer Recipient param can also be passed.

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        payload = {"batch": batch}
        return self.request("POST", "transferrecipient/bulk", json_data=payload)

    def list_transfer_recipients(
        self,
        per_page: Optional[int] = None,
        page: Optional[int] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        List transfer recipients available on your integration

        Args:
            per_page: Specify how many records you want to retrieve per page. If not specify we use a default value of 50.
            page: Specify exactly what page you want to retrieve. If not specify we use a default value of 1.
            from_date: A timestamp from which to start listing transfer recipients e.g. 2016-09-24T00:00:05.000Z, 2016-09-21
            to_date: A timestamp at which to stop listing transfer recipients e.g. 2016-09-24T00:00:05.000Z, 2016-09-21

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
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

    def fetch_transfer_recipient(
        self, id_or_code: str
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Fetch the details of a transfer recipient

        Args:
            id_or_code: An ID or code for the recipient whose details you want to receive.

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        return self.request("GET", f"transferrecipient/{id_or_code}")

    def update_transfer_recipient(
        self, id_or_code: str, name: Optional[str] = None, email: Optional[str] = None
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Update transfer recipients available on your integration

        Args:
            id_or_code: Transfer Recipient's ID or code
            name: A name for the recipient
            email: Email address of the recipient

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        payload = {}
        if name:
            payload["name"] = name
        if email:
            payload["email"] = email

        return self.request("PUT", f"transferrecipient/{id_or_code}", json_data=payload)

    def delete_transfer_recipient(
        self, id_or_code: str
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Delete a transfer recipient (sets the transfer recipient to inactive)

        Args:
            id_or_code: An ID or code for the recipient who you want to delete.

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        return self.request("DELETE", f"transferrecipient/{id_or_code}")
