from .core import BaseClient
from .exceptions import APIError
from .utils.validators import _validate_amount_and_email, _validate_charge_authorization
from .utils.helpers import validate_email


class Transaction(BaseClient):
    def __init__(self, secret_key=None):
        super().__init__(secret_key)

    def initialize(self, email: str = None, amount: str = None, **kwargs) -> dict:
        """
        Initialize a transaction.

        Args:
            email (str): Customer's email address.
            amount (str): Amount in kobo.
            **kwargs: Additional arguments for the API call.

        Returns:
            dict: Response data from the Paystack API.
        """
        _validate_amount_and_email(email, amount)
        payload = {"email": email, "amount": amount, **kwargs}
        return self.request("POST", "transaction/initialize", json=payload)

    def verify(self, reference: str) -> dict:
        """
        Verify a transaction.

        Args:
            reference (str): Transaction reference.

        Returns:
            dict: Response data from the Paystack API.
        """
        if not reference:
            raise APIError("Reference is required")
        return self.request("GET", f"transaction/verify/{reference}")

    def list(self) -> tuple:
        """
        List transactions.

        Returns:
            A tuple containing the list of transactions and metadata.
        """
        return self.request("GET", "transaction")

    def fetch(self, transaction_id: int) -> dict:
        """
        Fetch a transaction.

        Args:
            transaction_id: The ID of the transaction.

        Returns:
            dict: Response data from the Paystack API.
        """
        if not transaction_id:
            raise APIError("Transaction ID is required")
        return self.request("GET", f"transaction/{transaction_id}")

    def charge_authorization(self, email: str = None, amount: str = None, authorization_code: str = None, **kwargs):
        """Charge an authorization.

        Args:
            email: The customer's email address.
            amount: The amount in kobo.
            authorization_code: The authorization code.
            **kwargs: Additional keyword arguments.

        Returns:
            The response from the API.
        """
        _validate_charge_authorization(email, amount, authorization_code)
        payload = {
            "email": email,
            "amount": amount,
            "authorization_code": authorization_code,
            **kwargs,
        }
        return self.request("POST", "transaction/charge_authorization", json=payload)

    def view_timeline(self, id_or_reference: str) -> dict:
        """View the timeline of a transaction.

        Args:
            id_or_reference: The ID or reference of the transaction.

        Returns:
            The response from the API.
        """
        if not id_or_reference:
            raise APIError("ID or reference is required")
        return self.request("GET", f"transaction/timeline/{id_or_reference}")

    def totals(self) -> dict:
        """Get transaction totals.

        Returns:
            The response from the API.
        """
        return self.request("GET", "transaction/totals")

    def export(self) -> dict:
        """Export transactions.

        Returns:
            The response from the API.
        """
        return self.request("GET", "transaction/export")

    def partial_debit(self, payload=None, **kwargs):
        """Perform a partial debit on a transaction.

        Args:
            payload: A dictionary containing the request payload.
            **kwargs: Additional keyword arguments.

        Returns:
            The response from the API.
        """
        if payload is None:
            payload = kwargs
        elif not isinstance(payload, dict):
            raise APIError("Payload must be a dictionary")

        _validate_charge_authorization(
            payload.get("email"), payload.get("amount"), payload.get("authorization_code")
        )
        if not payload.get("currency"):
            raise APIError("Currency is required")

        return self.request("POST", "transaction/partial_debit", json=payload)
