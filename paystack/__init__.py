"""
Paystack Client - A Python wrapper for the Paystack API
"""

from .client import PaystackClient
from .core import BaseClient
from .exceptions import (
    APIError,
    AuthenticationError,
    InvalidResponseError,
    NetworkError,
    NotFoundError,
    PaystackError,
    RateLimitError,
    ServerError,
    TransactionFailureError,
    ValidationError,
    create_error_from_response,
)
from .webhook import WHITELISTED_IPS, Event, Webhook, WebhookEvent

__version__ = "2"
__author__ = "Joseph Ezekiel"
__email__ = "theolujay@gmail.com"
__description__ = "A modern Python client for Paystack API"

__all__ = [
    "PaystackClient",
    "BaseClient",
    "Webhook",
    "WebhookEvent",
    "Event",
    "WHITELISTED_IPS",
    "PaystackError",
    "APIError",
    "AuthenticationError",
    "ValidationError",
    "NotFoundError",
    "RateLimitError",
    "ServerError",
    "NetworkError",
    "InvalidResponseError",
    "TransactionFailureError",
    "create_error_from_response",
    "__version__",
    "__author__",
    "__email__",
    "__description__",
]
