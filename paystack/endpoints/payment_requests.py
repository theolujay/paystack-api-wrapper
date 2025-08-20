"""
The Payment Requests API allows you manage requests for payment of goods and services.
"""

import requests
from typing import Optional, List, Dict, Any, Tuple

from ..core import BaseClient


class PaymentRequestsAPI(BaseClient):
    """
    The Payment Requests API allows you manage requests for payment of goods and services.
    """

    def __init__(
        self, secret_key: str, session: requests.Session = None, base_url: str = None
    ):
        super().__init__(secret_key, session=session, base_url=base_url)

    def create_payment_request(
        self,
        customer: str,
        amount: Optional[int] = None,
        due_date: Optional[str] = None,
        description: Optional[str] = None,
        line_items: Optional[List[Dict[str, Any]]] = None,
        tax: Optional[List[Dict[str, Any]]] = None,
        currency: Optional[str] = None,
        send_notification: Optional[bool] = None,
        draft: Optional[bool] = None,
        has_invoice: Optional[bool] = None,
        invoice_number: Optional[int] = None,
        split_code: Optional[str] = None,
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Create a payment request for a transaction on your integration

        Args:
            customer: Customer id or code
            amount: Payment request amount. It should be used when line items and tax values aren't specified.
            due_date: ISO 8601 representation of request due date
            description: A short description of the payment request
            line_items: Array of line items int the format [{"name":"item 1", "amount":2000, "quantity": 1}]
            tax: Array of taxes to be charged in the format [{"name":"VAT", "amount":2000}]
            currency: Specify the currency of the payment request. Defaults to NGN.
            send_notification: Indicates whether Paystack sends an email notification to customer. Defaults to true
            draft: Indicate if request should be saved as draft. Defaults to false and overrides send_notification
            has_invoice: Set to true to create a draft payment request (adds an auto incrementing payment request number if none is provided) even if there are no line_items or tax passed
            invoice_number: Numeric value of the payment request. Payment Requests will start from 1 and auto increment from there. This field is to help override whatever value Paystack decides. Auto increment for subsequent payment requests continue from this point.
            split_code: The split code of the transaction split. e.g. SPL_98WF13Eb3w

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        payload = {"customer": customer}
        if amount:
            payload["amount"] = amount
        if due_date:
            payload["due_date"] = due_date
        if description:
            payload["description"] = description
        if line_items:
            payload["line_items"] = line_items
        if tax:
            payload["tax"] = tax
        if currency:
            payload["currency"] = currency
        if send_notification is not None:
            payload["send_notification"] = send_notification
        if draft is not None:
            payload["draft"] = draft
        if has_invoice is not None:
            payload["has_invoice"] = has_invoice
        if invoice_number:
            payload["invoice_number"] = invoice_number
        if split_code:
            payload["split_code"] = split_code

        return self.request("POST", "paymentrequest", json_data=payload)

    def list_payment_requests(
        self,
        per_page: Optional[int] = None,
        page: Optional[int] = None,
        customer: Optional[str] = None,
        status: Optional[str] = None,
        currency: Optional[str] = None,
        include_archive: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        List the payment requests available on your integration

        Args:
            per_page: Specify how many records you want to retrieve per page. If not specify we use a default value of 50.
            page: Specify the page you want to fetch payment requests from. If not specify we use a default value of 1.
            customer: Filter by customer ID
            status: Filter by payment request status
            currency: Filter by currency
            include_archive: Show archived payment requests
            from_date: A timestamp from which to start listing payment requests e.g. 2016-09-24T00:00:05.000Z, 2016-09-21
            to_date: A timestamp at which to stop listing payment requests e.g. 2016-09-24T00:00:05.000Z, 2016-09-21

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
        if status:
            params["status"] = status
        if currency:
            params["currency"] = currency
        if include_archive:
            params["include_archive"] = include_archive
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date

        return self.request("GET", "paymentrequest", params=params)

    def fetch_payment_request(
        self, id_or_code: str
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Get details of a payment request on your integration

        Args:
            id_or_code: The payment request ID or code you want to fetch

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        return self.request("GET", f"paymentrequest/{id_or_code}")

    def verify_payment_request(
        self, code: str
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Verify details of a payment request on your integration

        Args:
            code: Payment Request code

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        return self.request("GET", f"paymentrequest/verify/{code}")

    def send_notification(self, code: str) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Send notification of a payment request to your customers

        Args:
            code: Payment Request code

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        return self.request("POST", f"paymentrequest/notify/{code}")

    def payment_request_total(self) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Get payment requests metric

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        return self.request("GET", "paymentrequest/totals")

    def finalize_payment_request(
        self, code: str, send_notification: Optional[bool] = None
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Finalize a draft payment request

        Args:
            code: Payment Request code
            send_notification: Indicates whether Paystack sends an email notification to customer. Defaults to true

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        payload = {}
        if send_notification is not None:
            payload["send_notification"] = send_notification

        return self.request(
            "POST", f"paymentrequest/finalize/{code}", json_data=payload
        )

    def update_payment_request(
        self,
        id_or_code: str,
        customer: Optional[str] = None,
        amount: Optional[int] = None,
        due_date: Optional[str] = None,
        description: Optional[str] = None,
        line_items: Optional[List[Dict[str, Any]]] = None,
        tax: Optional[List[Dict[str, Any]]] = None,
        currency: Optional[str] = None,
        send_notification: Optional[bool] = None,
        draft: Optional[bool] = None,
        invoice_number: Optional[int] = None,
        split_code: Optional[str] = None,
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Update a payment request details on your integration

        Args:
            id_or_code: Payment Request ID or slug
            customer: Customer id or code
            amount: Payment request amount. Only useful if line items and tax values are ignored. endpoint will throw a friendly warning if neither is available.
            due_date: ISO 8601 representation of request due date
            description: A short description of the payment request
            line_items: Array of line items int the format [{"name":"item 1", "amount":2000}]
            tax: Array of taxes to be charged in the format [{"name":"VAT", "amount":2000}]
            currency: Specify the currency of the payment request. Defaults to NGN.
            send_notification: Indicates whether Paystack sends an email notification to customer. Defaults to true
            draft: Indicate if request should be saved as draft. Defaults to false and overrides send_notification
            invoice_number: Numeric value of the payment request. Payment Requests will start from 1 and auto increment from there. This field is to help override whatever value Paystack decides. Auto increment for subsequent payment requests continue from this point.
            split_code: The split code of the transaction split. e.g. SPL_98WF13Eb3w

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        payload = {}
        if customer:
            payload["customer"] = customer
        if amount:
            payload["amount"] = amount
        if due_date:
            payload["due_date"] = due_date
        if description:
            payload["description"] = description
        if line_items:
            payload["line_items"] = line_items
        if tax:
            payload["tax"] = tax
        if currency:
            payload["currency"] = currency
        if send_notification is not None:
            payload["send_notification"] = send_notification
        if draft is not None:
            payload["draft"] = draft
        if invoice_number:
            payload["invoice_number"] = invoice_number
        if split_code:
            payload["split_code"] = split_code

        return self.request("PUT", f"paymentrequest/{id_or_code}", json_data=payload)

    def archive_payment_request(
        self, code: str
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Used to archive a payment request. A payment request will no longer be fetched on list or returned on verify

        Args:
            code: Payment Request code

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        return self.request("POST", f"paymentrequest/archive/{code}")
