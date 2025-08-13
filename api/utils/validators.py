"""Validation helpers for Paystack API calls."""

from ..exceptions import APIError
from .helpers import validate_email


def _validate_amount_and_email(email: str, amount: int):
    """Validate email and amount for a transaction.

    Args:
        email (str): Customer's email address.
        amount (int): Amount in kobo.

    Raises:
        APIError: If email or amount is invalid.
    """
    if not email:
        raise APIError("Email is required")
    if not amount:
        raise APIError("Amount is required")
    if not validate_email(email):
        raise APIError("Invalid email format")

    try:
        amount_int = int(amount)
        if amount_int <= 0:
            raise APIError("Amount must be a positive number")
    except (ValueError, TypeError):
        raise APIError("Amount must be a valid number string without comma or decimal")


def _validate_charge_authorization(email: str, amount: int, authorization_code: str):
    """Validate email, amount, and authorization code for a transaction.

    Args:
        email (str): Customer's email address.
        amount (int): Amount in kobo.
        authorization_code (str): Authorization code.

    Raises:
        APIError: If email, amount, or authorization code is invalid.
    """
    _validate_amount_and_email(email, amount)
    if not authorization_code:
        raise APIError("Authorization code is required")
