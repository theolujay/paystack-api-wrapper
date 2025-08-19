"""
Paystack API Exception Classes

This module provides a hierarchy of exceptions that make it easier for developers
to handle different types of errors when using the Paystack API.
"""

from typing import Optional, Dict, Any, Union
import json


class PaystackError(Exception):
    """
    Base exception class for all Paystack-related errors.

    This is the parent class that all other Paystack exceptions inherit from.
    You can catch this to handle any Paystack-related error.

    Note: Paystack always returns HTTP 200 for charge/verify requests, even if
    the transaction failed. Check the 'status' field in the response data to
    determine actual success/failure.
    """

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response: Optional[Dict[str, Any]] = None,
        request_id: Optional[str] = None,
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response = response or {}
        self.request_id = request_id

    def __str__(self) -> str:
        parts = ["PaystackError"]
        if self.status_code:
            parts.append(f"HTTP {self.status_code}")
        if self.request_id:
            parts.append(f"Request ID: {self.request_id}")
        parts.append(self.message)
        return " - ".join(parts)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"message='{self.message}', "
            f"status_code={self.status_code}, "
            f"request_id='{self.request_id}'"
            f")"
        )


class APIError(PaystackError):
    """
    General API error for HTTP-related issues.

    This covers most API errors like network issues, timeouts, etc.
    """

    pass


class AuthenticationError(PaystackError):
    """
    Raised when API key is invalid or missing.

    HTTP Status: 401 - The request was not authorized. This can be triggered
    by passing an invalid secret key in the authorization header or the lack of one.

    Common causes:
    - Invalid secret key (wrong key or typo)
    - Missing Authorization header
    - Using test key in production or vice versa
    - Expired or revoked API key

    Important: Double-check your API key and ensure you're using the right
    environment (test vs live).
    """

    pass


class ValidationError(PaystackError):
    """
    Raised when request data is invalid.

    HTTP Status: 400 - A validation or client side error occurred and
    the request was not fulfilled.

    Common causes:
    - Missing required fields
    - Invalid data format
    - Invalid email format
    - Amount too small/large
    - Invalid currency code
    - Malformed request body
    """

    def __init__(
        self, message: str, field_errors: Optional[Dict[str, str]] = None, **kwargs
    ):
        super().__init__(message, **kwargs)
        self.field_errors = field_errors or {}

    def __str__(self) -> str:
        base_str = super().__str__()
        if self.field_errors:
            field_details = ", ".join(
                [f"{field}: {error}" for field, error in self.field_errors.items()]
            )
            return f"{base_str} | Field errors: {field_details}"
        return base_str


class NotFoundError(PaystackError):
    """
    Raised when a requested resource doesn't exist.

    HTTP Status: 404 - Request could not be fulfilled as the
    request resource does not exist.

    Common causes:
    - Transaction reference not found
    - Customer code not found
    - Invalid endpoint URL
    - Resource was deleted
    - Wrong resource ID format
    """

    pass


class RateLimitError(PaystackError):
    """
    Raised when API rate limits are exceeded.

    HTTP Status: 429
    The response usually includes retry-after information.
    """

    def __init__(self, message: str, retry_after: Optional[int] = None, **kwargs):
        super().__init__(message, **kwargs)
        self.retry_after = retry_after  # Seconds to wait before retrying

    def __str__(self) -> str:
        base_str = super().__str__()
        if self.retry_after:
            return f"{base_str} | Retry after: {self.retry_after} seconds"
        return base_str


class ServerError(PaystackError):
    """
    Raised for server-side errors (5xx status codes).

    HTTP Status: 5xx - Request could not be fulfilled due to an error
    on Paystack's end. This shouldn't happen so please report as soon
    as you encounter any instance of this.

    These errors are on Paystack's side and should be reported to their
    support team. Usually temporary and can be retried with backoff.

    When this happens:
    1. Retry the request after a delay
    2. Report to Paystack support if it persists
    3. Log the full error details including request_id
    """

    pass


class NetworkError(PaystackError):
    """
    Raised for network-related issues.

    Common causes:
    - Connection timeout
    - DNS resolution failure
    - No internet connection
    """

    pass


class InvalidResponseError(PaystackError):
    """
    Raised when API returns unexpected response format.

    Common causes:
    - Malformed JSON
    - Missing expected fields in response
    - API version mismatch
    """

    pass


class TransactionFailureError(PaystackError):
    """
    Raised when a transaction fails but Paystack returns HTTP 200.

    Important: Paystack always returns HTTP 200 for charge and verify requests,
    even when the transaction fails. This exception is raised when:
    - response.status_code == 200
    - response.data.status == False or 'failed'

    Common causes:
    - Insufficient funds
    - Invalid card details
    - Card declined by bank
    - Transaction timeout
    - Risk management decline

    Check the 'gateway_response' field for bank's response message.
    """

    def __init__(self, message: str, gateway_response: Optional[str] = None, **kwargs):
        super().__init__(message, **kwargs)
        self.gateway_response = gateway_response

    def __str__(self) -> str:
        base_str = super().__str__()
        if self.gateway_response:
            return f"{base_str} | Gateway response: {self.gateway_response}"
        return base_str


def create_error_from_response(
    response, status_code: int, request_id: Optional[str] = None
) -> PaystackError:
    """
    Factory function to create appropriate exception from API response.

    This function handles Paystack's unique behavior where charge/verify
    requests always return HTTP 200, even for failed transactions.

    Args:
        response: HTTP response object or response data dict
        status_code: HTTP status code
        request_id: Request ID from response headers

    Returns:
        Appropriate PaystackError subclass instance
    """

    # Try to extract error message and data from response
    field_errors = None
    try:
        if hasattr(response, "json"):
            data = response.json()
        elif isinstance(response, dict):
            data = response
        else:
            data = {}

        message = data.get("message", f"HTTP {status_code} error")

        # Extract field-specific errors for validation errors
        if "errors" in data and isinstance(data["errors"], dict):
            field_errors = data["errors"]

    except (json.JSONDecodeError, AttributeError):
        message = f"HTTP {status_code} error"
        data = {}

    # Create appropriate exception based on status code
    kwargs = {
        "message": message,
        "status_code": status_code,
        "response": data,
        "request_id": request_id,
    }

    if status_code == 400:
        return ValidationError(field_errors=field_errors, **kwargs)
    elif status_code == 401:
        return AuthenticationError(**kwargs)
    elif status_code == 404:
        return NotFoundError(**kwargs)
    elif status_code == 429:
        # Extract retry-after from response if available
        retry_after = None
        if hasattr(response, "headers"):
            retry_after = response.headers.get("Retry-After")
            if retry_after:
                try:
                    retry_after = int(retry_after)
                except ValueError:
                    retry_after = None
        return RateLimitError(retry_after=retry_after, **kwargs)
    elif 500 <= status_code <= 599:
        return ServerError(**kwargs)
    else:
        return APIError(**kwargs)
