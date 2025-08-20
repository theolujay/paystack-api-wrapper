# refund.py
import requests
from typing import Optional, Union, Dict, Any, Tuple
from ..core import BaseClient
from ..exceptions import APIError


class RefundsAPI(BaseClient):
    """Refund API client for creating and managing transaction refunds."""

    def __init__(self, secret_key: str, session: requests.Session = None, base_url: str = None):
        super().__init__(secret_key, session=session, base_url=base_url)

    def create(
        self,
        transaction: Union[str, int],
        amount: Optional[int] = None,
        currency: Optional[str] = None,
        customer_note: Optional[str] = None,
        merchant_note: Optional[str] = None,
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Initiate a refund on your integration.

        Args:
            transaction (Union[str, int]): Transaction reference or ID to refund
            amount (Optional[int]): Amount in subunit of supported currency to be refunded.
                                  Defaults to original transaction amount and cannot exceed it
            currency (Optional[str]): Any of the supported currency codes
            customer_note (Optional[str]): Customer-facing reason for the refund
            merchant_note (Optional[str]): Internal merchant reason for the refund

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.

        Raises:
            APIError: If transaction parameter is not provided
        """
        self._validate_required_params(transaction=transaction)

        payload = {"transaction": str(transaction)}

        if amount is not None:
            if amount <= 0:
                raise APIError("amount must be greater than 0")
            payload["amount"] = amount
        if currency:
            payload["currency"] = currency
        if customer_note:
            payload["customer_note"] = customer_note
        if merchant_note:
            payload["merchant_note"] = merchant_note

        return self.request("POST", "refund", json_data=payload)

    def list_refunds(
        self,
        transaction: str,
        currency: str,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        per_page: Optional[int] = None,
        page: Optional[int] = None,
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """List refunds available on your integration.

        Args:
            transaction: The transaction ID of the refunded transaction
            currency: Any of the supported currency codes
            from_date (Optional[str]): A timestamp from which to start listing refunds (e.g. '2016-09-21')
            to_date (Optional[str]): A timestamp at which to stop listing refunds (e.g. '2016-09-21')
            per_page (Optional[int]): Number of records per page (default: 50)
            page (Optional[int]): Page number to retrieve (default: 1)

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.

        Raises:
            APIError: If per_page or page parameters are invalid
        """
        self._validate_required_params(transaction=transaction, currency=currency)

        payload = {"transaction": transaction, "currency": currency}

        if transaction:
            payload["transaction"] = transaction
        if currency:
            payload["currency"] = currency
        if from_date:
            payload["from"] = from_date
        if to_date:
            payload["to"] = to_date
        if per_page is not None:
            if per_page <= 0:
                raise APIError("per_page must be greater than 0")
            payload["perPage"] = per_page
        if page is not None:
            if page <= 0:
                raise APIError("page must be greater than 0")
            payload["page"] = page

        return self.request("GET", "refund", params=payload)

    def fetch(
        self, refund_id: Union[str, int]
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Get details of a refund on your integration.

        Args:
            refund_id (Union[str, int]): The ID of the initiated refund

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.

        Raises:
            APIError: If refund_id is not provided
        """
        self._validate_required_params(refund_id=refund_id)

        return self.request("GET", f"refund/{refund_id}")
