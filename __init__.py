"""
Paystack Client - A Python wrapper for the Paystack API

This library provides a simple, intuitive interface for interacting with
the Paystack payment processing API from your Django applications.

Example usage:
    from paystack_client import CustomerAPI, ChargeAPI

    # Create a customer
    customer = CustomerAPI()
    result = customer.create(email="user@example.com", name="John Doe")

    # Create a charge
    charge = ChargeAPI()
    result = charge.initialize(amount=10000, email="user@example.com")
"""

from .paystack_client import *
from .client import PaystackClient

__version__ = "1.0.0"
__author__ = "Joseph Ezekiel"
__email__ = "olujay.dev@gmail.com"
__description__ = "A modern Python client for Paystack API"

__all__ = [
    "__version__",
    "__author__",
    "__email__",
    "__description__",
]

if "__all__" in locals():
    __all__.append("PaystackClient")
else:
    __all__ = ["PaystackClient"]
