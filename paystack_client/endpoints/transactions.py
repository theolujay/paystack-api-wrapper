from typing import Optional, Dict, Any, Union, Tuple

import requests
from ..core import BaseClient
from ..exceptions import APIError, ValidationError
from ..utils.validators import _validate_amount_and_email, _validate_charge_authorization


class TransactionsAPI(BaseClient):
    """Transaction API client for processing payments and managing transactions."""

    def __init__(self, secret_key: str, session: requests.Session = None, base_url: str = None):
        super().__init__(secret_key, session=session, base_url=base_url)

    def initialize(
        self,
        email: str,
        amount: Union[int, str],
        currency: str = "NGN",
        reference: Optional[str] = None,
        callback_url: Optional[str] = None,
        plan: Optional[str] = None,
        invoice_limit: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None,
        channels: Optional[list] = None,
        split_code: Optional[str] = None,
        subaccount: Optional[str] = None,
        transaction_charge: Optional[int] = None,
        bearer: Optional[str] = None,
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Initialize a transaction for payment.

        Args:
            email (str): Customer's email address
            amount (Union[int, str]): Amount in subunit of the supported currency
            currency (str): Currency code (default: "NGN")
            reference (Optional[str]): Unique transaction reference
            callback_url (Optional[str]): URL to redirect after payment
            plan (Optional[str]): Plan code if this is a subscription payment
            invoice_limit (Optional[int]): Number of invoices to generate
            metadata (Optional[Dict]): Stringified JSON object of custom data
            channels (Optional[list]): Payment channels to enable e.g. ['card', 'bank']
            split_code (Optional[str]): Split payment configuration code
            subaccount (Optional[str]): Subaccount code for split payments
            transaction_charge (Optional[int]): Transaction charge in kobo
            bearer (Optional[str]): Who bears Paystack charges ('account' or 'subaccount')

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.

        Raises:
            APIError: If email or amount is invalid
        """
        self._validate_email(email)
        self._validate_amount(amount, currency)

        payload = {"email": email, "amount": (amount), "currency": currency}
        if reference:
            payload["reference"] = reference
        if callback_url:
            payload["callback_url"] = callback_url
        if plan:
            payload["plan"] = plan
        if invoice_limit is not None:
            payload["invoice_limit"] = invoice_limit
        if metadata is not None:
            # Convert metadata dict to JSON string as per API requirements
            import json

            payload["metadata"] = json.dumps(metadata)
        if channels:
            payload["channels"] = channels
        if split_code:
            payload["split_code"] = split_code
        if subaccount:
            payload["subaccount"] = subaccount
        if transaction_charge is not None:
            payload["transaction_charge"] = transaction_charge
        if bearer:
            payload["bearer"] = bearer

        return self.request("POST", "transaction/initialize", json_data=payload)

    def verify(self, reference: str) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Verify a transaction status.

        Args:
            reference (str): Transaction reference to verify

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.

        Raises:
            APIError: If reference is not provided
        """
        self._validate_required_params(reference=reference)
        return self.request("GET", f"transaction/verify/{reference}")

    def list_transactions(
        self,
        per_page: Optional[int] = None,
        page: Optional[int] = None,
        customer: Optional[int] = None,
        terminal_id: Optional[str] = None,
        status: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        amount: Optional[Union[int, str]] = None,
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """List transactions with optional filtering.

        Args:
            per_page (Optional[int]): Number of records per page (default: 50)
            page (Optional[int]): Page number to retrieve (default: 1)
            customer (Optional[int]): Customer ID to filter by
            terminal_id (Optional[str]): Terminal ID for the transactions you want to retrieve
            status (Optional[str]): Transaction status ('failed', 'success', 'abandoned')
            from_date (Optional[str]): Start date filter (e.g. '2016-09-24T00:00:05.000Z')
            to_date (Optional[str]): End date filter (e.g. '2016-09-24T00:00:05.000Z')
            amount (Optional[Union[int, str]]): Amount to filter by

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        params = {}

        if per_page is not None:
            params["perPage"] = per_page
        if page is not None:
            params["page"] = page
        if customer is not None:
            params["customer"] = customer
        if terminal_id:
            params["terminalid"] = terminal_id
        if status:
            if status not in ["failed", "success", "abandoned"]:
                raise APIError(
                    "status must be one of: 'failed', 'success', 'abandoned'"
                )
            params["status"] = status
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date
        if amount is not None:
            params["amount"] = str(amount)

        return self.request("GET", "transaction", params=params)

    def fetch(self, transaction_id: int) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Fetch details of a single transaction.

        Args:
            transaction_id (Union[int, str]): The ID of the transaction to fetch

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.

        Raises:
            APIError: If transaction_id is not provided
        """
        self._validate_required_params(transaction_id=transaction_id)
        return self.request("GET", f"transaction/{transaction_id}")

    def charge_authorization(
        self,
        email: str,
        amount: Union[int, str],
        authorization_code: str,
        currency: str = "NGN",
        reference: Optional[str] = None,
        channels: Optional[list] = None,
        subaccount: Optional[str] = None,
        transaction_charge: Optional[int] = None,
        bearer: Optional[str] = None,
        queue: Optional[bool] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Charge a customer's authorization (for recurring payments).

        Args:
            email (str): Customer's email address
            amount (Union[int, str]): Amount to charge in kobo
            authorization_code (str): Authorization code from previous transaction
            currency (str): Currency code (default: "NGN")
            reference (Optional[str]): Unique transaction reference
            channels (Optional[list]): Payment channels to use
            subaccount (Optional[str]): Subaccount code for split payments
            transaction_charge (Optional[int]): Transaction charge in kobo
            bearer (Optional[str]): Who bears Paystack charges
            queue (Optional[bool]): Whether to queue transaction if auth is unavailable
            metadata (Optional[Dict]): Additional data to store

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.

        Raises:
            APIError: If required parameters are invalid
        """
        self._validate_email(email)
        self._validate_amount(amount, currency)

        payload = {
            "email": email,
            "amount": amount,
            "authorization_code": authorization_code,
            "currency": currency,
        }
        if reference:
            payload["reference"] = reference
        if channels:
            payload["channels"] = channels
        if subaccount:
            payload["subaccount"] = subaccount
        if transaction_charge is not None:
            payload["transaction_charge"] = transaction_charge
        if bearer:
            payload["bearer"] = bearer
        if queue is not None:
            payload["queue"] = queue
        if metadata:
            import json

            payload["metadata"] = json.dumps(metadata)

        return self.request(
            "POST", "transaction/charge_authorization", json_data=payload
        )

    def view_timeline(
        self, id_or_reference: Union[int, str]
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """View the timeline/history of a transaction.

        Args:
            id_or_reference (Union[int, str]): Transaction ID or reference

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.

        Raises:
            APIError: If id_or_reference is not provided
        """
        self._validate_required_params(id_or_reference=id_or_reference)
        return self.request("GET", f"transaction/timeline/{id_or_reference}")

    def get_totals(
        self,
        per_page: Optional[int] = None,
        page: Optional[int] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Get transaction totals for your integration.

        Args:
            per_page (Optional[int]): Number of records per page
            page (Optional[int]): Page number to retrieve
            from_date (Optional[str]): Start date for totals calculation
            to_date (Optional[str]): End date for totals calculation

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        params = {}

        if per_page is not None:
            params["perPage"] = per_page
        if page is not None:
            params["page"] = page
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date

        return self.request("GET", "transaction/totals", params=params)

    def export_transactions(
        self,
        per_page: Optional[int] = None,
        page: Optional[int] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        customer: Optional[int] = None,
        status: Optional[str] = None,
        currency: Optional[str] = None,
        amount: Optional[Union[int, str]] = None,
        settled: Optional[bool] = None,
        settlement: Optional[int] = None,
        payment_page: Optional[int] = None,
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Export transactions as CSV.

        Args:
            per_page (Optional[int]): Number of records per page
            page (Optional[int]): Page number to retrieve
            from_date (Optional[str]): Start date filter
            to_date (Optional[str]): End date filter
            customer (Optional[int]): Customer ID to filter by
            status (Optional[str]): Transaction status filter
            currency (Optional[str]): Currency filter
            amount (Optional[Union[int, str]]): Amount filter
            settled (Optional[bool]): Filter by settlement status
            settlement (Optional[int]): Settlement ID filter
            payment_page (Optional[int]): Payment page ID filter

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        query = {}

        if per_page is not None:
            query["perPage"] = per_page
        if page is not None:
            query["page"] = page
        if from_date:
            query["from"] = from_date
        if to_date:
            query["to"] = to_date
        if customer is not None:
            query["customer"] = customer
        if status:
            query["status"] = status
        if currency:
            query["currency"] = currency
        if amount is not None:
            query["amount"] = str(amount)
        if settled is not None:
            query["settled"] = str(settled).lower()
        if settlement is not None:
            query["settlement"] = settlement
        if payment_page is not None:
            query["payment_page"] = payment_page

        return self.request("GET", "transaction/export", params=query)

    def partial_debit(
        self,
        authorization_code: str,
        currency: str,
        amount: Union[int, str],
        email: str,
        reference: Optional[str] = None,
        at_least: Optional[Union[int, str]] = None,
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Perform a partial debit transaction.

        This allows you to charge a customer but if the amount on their card/account
        is less than what you're trying to charge, it charges the available amount.

        Args:
            authorization_code (str): Authorization code from previous transaction
            currency (str): Currency code (NGN or GHS for partial debits)
            amount (Union[int, str]): Preferred amount to charge in kobo
            email (str): Customer's email address (attached to the authorization code)
            reference (Optional[str]): Unique transaction reference
            at_least (Optional[Union[int, str]]): Minimum acceptable amount in kobo

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.

        Raises:
            APIError: If required parameters are missing or invalid
        """
        self._validate_email(email)
        self._validate_required_params(currency=currency)
        self._validate_amount(amount, currency)

        # Validate currency for partial debit
        if currency not in ["NGN", "GHS"]:
            raise ValidationError("currency must be 'NGN' or 'GHS' for partial debit")

        payload = {
            "authorization_code": authorization_code,
            "currency": currency,
            "amount": str(amount),
            "email": email,
        }

        # Add optional fields
        if reference:
            payload["reference"] = reference
        if at_least is not None:
            payload["at_least"] = str(at_least)

        return self.request("POST", "transaction/partial_debit", json_data=payload)
