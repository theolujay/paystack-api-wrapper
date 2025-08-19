import re

from ..exceptions import ValidationError


def validate_email(email):
    """
    Validate an email address.

    Args:
        email (str): The email address to validate.

    Raises:
            ValidationError: If email format is invalid
    """
    if not email or not isinstance(email, str) or len(email) > 254:
        raise ValidationError(
            message="Email is required",
            field_errors={"email": "Email address is required"},
        )

    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    if not re.match(pattern, email):
        raise ValidationError(
            message="Invalid email format",
            field_errors={"email": "Please provide a valid email address"},
        )
