"""The Customers API to create and manage customers."""

from typing import Optional

from .core import BaseClient
from .exceptions import APIError
from .utils.helpers import validate_email
from .utils.validators import (
    _validate_amount_and_email,
    _validate_charge_authorization
)

class Customer(BaseClient):
    
    def __init__(self, secret_key=None):
        super().__init__(secret_key)
    
    def create(self, email: str = None, first_name: Optional[str] = None, last_name: Optional[str] = None, phone: Optional[str] = None, **kwargs) -> dict:
        """
        Create a customer on your integration
        The first_name, last_name and phone are optional parameters. However, when creating a customer that would be assigned a Dedicated Virtual Account and your business category falls under Betting, Financial services, and General Service, then these parameters become compulsory."""
        validate_email(email)
        if not first_name:
            raise APIError("First name is required")
        if not last_name:
            raise APIError("Last name is required")
        if not phone:
            raise APIError("Phone number is required")
        payload = {
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "phone": phone,
            **kwargs
        }
        return self.request("POST", "customer", json=payload)
    
    def list(self):
        """
        List customers available on your integration.
        
        Returns:
            A tuple containing the list of customers and metadata.
        """
        return self.request("GET", "customer")
    
    def fetch(self, email_or_code: str = None) -> dict:
        """Get details of a customer on your integration."""
        if not email_or_code:
            raise APIError("Email or code is required")
        return self.request("GET", f"customer/{email_or_code}")
    
    def update(self, code: str = None, **kwargs) -> dict:
        """Update a customer's details on your integration"""
        if not code:
            raise APIError("Code is required")
        payload = kwargs
        return self.request("PUT", f"customer/{code}", json=payload)

    def validate(self, customer_code: str = None, **kwargs) -> str:
        """Validate a customer's identity"""
        if not customer_code:
            raise APIError("Customer code is required")
        payload = kwargs
        return self.request("POST", f"customer/{customer_code}/identification", json=payload)
    
    def whitelist_blacklist(self, customer: str = None, action: str = None) -> dict:
        """Whitelist or blacklist a customer on your integration"""
        if not customer:
            raise APIError("Customer is required")
        if not action:
            raise APIError("Action is required")
        payload = {
            "customer": customer,
            "risk_action": action
        }
        return self.request("POST", "customer/set_risk_action", json=payload)
    
    def initialize_authorization(self, email: str = None, channel: str = None, callback_url: str = None):
        """Initiate a request to create a reusable authorization code for recurring transactions."""
        validate_email(email)
        payload = {
            "email": email,
            "channel": channel,
            "callback_url": callback_url
        }
        return self.request("POST", "customer/authorization/initialize", json=payload)
    
    def verify_authorization(self, reference: str) -> dict:
        """Check the status of an authorization request."""
        if not reference:
            raise APIError("Reference is required")
        return self.request("GET", f"customer/authorization/verify/{reference}")
    
    def initialize_direct_debit(self, id: str = None, **kwargs) -> dict:
        """
        Initialize the process of linking an account to a customer for Direct Debit transactions.
        """
        if not id:
            raise APIError("ID is required")
        payload = kwargs
        return  self.request("POST", f"customer/{id}/initialize-direct-debit", payload)
    
    def direct_debit_activation_charge(self, id: str = None, **kwargs) -> str:
        """
        Trigger an activation charge on an inactive mandate on behalf of your customer.

        Args:
            id (str): The ID of the customer.
            **kwargs: Additional keyword arguments.

        Returns:
            dict: Response data from the Paystack API.
        """
        if not id:
            raise APIError("ID is required")
        payload = kwargs
        return self.request("POST", f"customer/{id}/directdebit-activation-charge", payload)
    
    def fetch_mandate_authorizations(self, id: str = None) -> dict:
        """Get the list of direct debit mandates associated with a customer.
        Args:
            id (str): The ID of the customer.
            
        Returns:
            A tuple containing the list of mandates and metadata.
        """
        
        if not id:
            raise APIError("ID is required")
        return self.request("GET", f"customer/{id}/directdebit-mandate-authorizations")
    
    def deactivate_authorization(self, authorization_code: str = None) -> str:
        """Deactivate an authorization for any payment channel."""
        if not authorization_code:
            raise APIError("Authorization code is required")
        payload = {
            "authorization_code": authorization_code
        }
        return self.request("POST", f"customer/authorization/deactivate", payload)
    
    