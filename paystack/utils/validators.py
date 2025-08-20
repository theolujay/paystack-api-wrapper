"""Validation helpers for Paystack API calls."""

from typing import Union
from ..exceptions import APIError, ValidationError
from .helpers import validate_email


def _validate_amount_and_email(email: str, amount: Union[int, str]):
    """Validate email and amount for a transaction.

    Args:
        email (str): Customer's email address.
        amount (int): Amount in kobo.

    Raises:
        APIError: If email or amount is invalid.
    """
    if not email:
        raise ValidationError("Email is required")
    if amount is None:
        raise ValidationError("Amount is required")

    validate_email(email)

    try:
        amount_int = int(amount)
        if amount_int <= 0:
            raise ValidationError("Amount must be a positive number")
    except (ValueError, TypeError):
        raise ValidationError(
            "Amount must be a valid number string without comma or decimal"
        )


def _validate_charge_authorization(
    email: str, amount: Union[int, str], authorization_code: str
):
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
