import pytest
from unittest.mock import patch
from paystack_client.exceptions import APIError, ValidationError
from paystack_client.utils.validators import _validate_amount_and_email, _validate_charge_authorization

def test_validate_amount_and_email_missing_email():
    with pytest.raises(ValidationError, match="Email is required"):
        _validate_amount_and_email(email="", amount=10000)

def test_validate_amount_and_email_missing_amount():
    with pytest.raises(ValidationError, match="Amount is required"):
        _validate_amount_and_email(email="test@example.com", amount=None)

def test_validate_amount_and_email_invalid_email_format():
    with pytest.raises(ValidationError, match="Invalid email format"):
        _validate_amount_and_email(email="invalid-email", amount=10000)

def test_validate_amount_and_email_non_numeric_amount():
    with pytest.raises(ValidationError, match="Amount must be a valid number string without comma or decimal"):
        _validate_amount_and_email(email="test@example.com", amount="abc")
    with pytest.raises(ValidationError, match="Amount must be a valid number string without comma or decimal"):
        _validate_amount_and_email(email="test@example.com", amount="10,000")

def test_validate_amount_and_email_zero_or_negative_amount():
    with pytest.raises(ValidationError, match="Amount must be a positive number"):
        _validate_amount_and_email(email="test@example.com", amount=0)
    with pytest.raises(ValidationError, match="Amount must be a positive number"):
        _validate_amount_and_email(email="test@example.com", amount=-100)

def test_validate_amount_and_email_valid():
    # Should not raise any exception
    _validate_amount_and_email(email="test@example.com", amount=10000)
    _validate_amount_and_email(email="test@example.com", amount="10000")

def test_validate_charge_authorization_missing_authorization_code():
    with pytest.raises(APIError, match="Authorization code is required"):
        _validate_charge_authorization(email="test@example.com", amount=10000, authorization_code="")

def test_validate_charge_authorization_valid():
    # Should not raise any exception
    _validate_charge_authorization(email="test@example.com", amount=10000, authorization_code="AUTH_testcode")