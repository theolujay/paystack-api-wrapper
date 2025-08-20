"""
The Transfers API allows you automate sending money to your customers.
"""

import requests
from typing import Optional, List, Dict, Any, Tuple, Union

from ..core import BaseClient


class TransfersAPI(BaseClient):
    """
    The Transfers API allows you automate sending money to your customers.
    """

    def __init__(
        self, secret_key: str, session: requests.Session = None, base_url: str = None
    ):
        super().__init__(secret_key, session=session, base_url=base_url)

    def initiate_transfer(
        self,
        source: str,
        amount: Union[int, str],
        recipient: str,
        reason: Optional[str] = None,
        currency: Optional[str] = None,
        reference: Optional[str] = None,
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Send money to your customers.

        Args:
            source: Where should we transfer from? Only balance for now
            amount: Amount to transfer in kobo if currency is NGN and pesewas if currency is GHS.
            recipient: Code for transfer recipient
            reason: The reason for the transfer
            currency: Specify the currency of the transfer. Defaults to NGN
            reference: If specified, the field should be a unique identifier (in lowercase) for the object. Only -,_ and alphanumeric characters allowed.

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        self._validate_required_params(
            source=source, amount=amount, recipient=recipient
        )
        payload = {
            "source": source,
            "amount": amount,
            "recipient": recipient,
        }
        if reason:
            payload["reason"] = reason
        if currency:
            payload["currency"] = currency
        if reference:
            payload["reference"] = reference

        return self.request("POST", "transfer", json_data=payload)

    def finalize_transfer(
        self, transfer_code: str, otp: str
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Finalize an initiated transfer

        Args:
            transfer_code: The transfer code you want to finalize
            otp: OTP sent to business phone to verify transfer

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        self._validate_required_params(transfer_code=transfer_code, otp=otp)
        payload = {
            "transfer_code": transfer_code,
            "otp": otp,
        }
        return self.request("POST", "transfer/finalize_transfer", json_data=payload)

    def initiate_bulk_transfer(
        self, source: str, transfers: List[Dict[str, Any]]
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Batch multiple transfers in a single request.

        Args:
            source: Where should we transfer from? Only balance for now
            transfers: A list of transfer object. Each object should contain amount, recipient, and reference

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        self._validate_required_params(source=source, transfers=transfers)
        payload = {
            "source": source,
            "transfers": transfers,
        }
        return self.request("POST", "transfer/bulk", json_data=payload)

    def list_transfers(
        self,
        per_page: Optional[int] = None,
        page: Optional[int] = None,
        recipient: Optional[int] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        List the transfers made on your integration.

        Args:
            per_page: Specify how many records you want to retrieve per page. If not specify we use a default value of 50.
            page: Specify exactly what transfer you want to page. If not specify we use a default value of 1.
            recipient: Filter by the recipient ID
            from_date: A timestamp from which to start listing transfer e.g. 2016-09-24T00:00:05.000Z, 2016-09-21
            to_date: A timestamp at which to stop listing transfer e.g. 2016-09-24T00:00:05.000Z, 2016-09-21

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        params = {}
        if per_page:
            params["perPage"] = per_page
        if page:
            params["page"] = page
        if recipient:
            params["recipient"] = recipient
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date

        return self.request("GET", "transfer", params=params)

    def fetch_transfer(self, id_or_code: str) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Get details of a transfer on your integration.

        Args:
            id_or_code: The transfer ID or code you want to fetch

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        self._validate_required_params(id_or_code=id_or_code)
        return self.request("GET", f"transfer/{id_or_code}")

    def verify_transfer(self, reference: str) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Verify the status of a transfer on your integration.

        Args:
            reference: Transfer reference

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        self._validate_required_params(reference=reference)
        return self.request("GET", f"transfer/verify/{reference}")
