import pytest
import re
from paystack_client.exceptions import ValidationError
from paystack_client.utils.helpers import validate_email

def test_validate_email_valid():
    validate_email("test@example.com")
    # No exception should be raised

def test_validate_email_invalid_format():
    with pytest.raises(ValidationError, match="Invalid email format"):
        validate_email("invalid-email")

def test_validate_email_empty():
    with pytest.raises(ValidationError, match="Email is required"):
        validate_email("")

def test_validate_email_none():
    with pytest.raises(ValidationError, match="Email is required"):
        validate_email(None)

def test_validate_email_not_string():
    with pytest.raises(ValidationError, match="Email is required"):
        validate_email(123)

def test_validate_email_too_long():
    with pytest.raises(ValidationError, match="Email is required"):
        validate_email("a" * 255 + "@example.com")
