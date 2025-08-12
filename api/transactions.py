

from .core import BaseClient
from .exceptions import APIError
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
            elif amount_int < 10000:
                raise APIError("Amount must be at least 100 naira")
            elif amount_int > 1000000000:
                raise APIError("Amount must be less than 10 million naira")
        except ValueError:
            raise APIError("Amount must be a valid number string without comma or decimal")
        
        payload = {
            "email": email,
            "amount": str(amount),
            **kwargs
        }
        
        response = self.request("POST", "transaction/initialize", json=payload)
        return response
    
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
        
        response = self.request("GET", f"transaction/verify/{reference}")
        return response
    
    def list(self) -> tuple:
        """
        List transactions.

        Returns:
            dict: Response data from the Paystack API.
        """
        response = self.request("GET", "transaction")
        return response
    
    def fetch(self, transaction_id: int) -> dict:
        """
        
        """
        if not transaction_id:
            raise APIError("Transaction ID is required")
        
        response = self.request("GET", f"transaction/{transaction_id}")
        return response
        
    def charge_authorization(self, email: str = None, amount: str = None, authorization_code: str = None, **kwargs):
        if not email:
            raise APIError("Email is required")
        if not amount:
            raise APIError("Amount is required")
        if not validate_email(email):
            raise APIError("Invalid email format")
        if not authorization_code:
            raise APIError("Authorization code is required")
        try:
            amount_int = int(amount)
            if amount_int <= 0:
                raise APIError("Amount must be a positive number")
            elif amount_int < 10000:
                raise APIError("Amount must be at least 100 naira")
            elif amount_int > 1000000000:
                raise APIError("Amount must be less than 10 million naira")
        except ValueError:
            raise APIError("Amount must be a valid number string without comma or decimal")
        
        payload = {
            "email": email,
            "amount": amount,
            "authorization_code": authorization_code
        }
        return self.request("POST", "transaction/charge_authorization", data=payload)
    
    def view_timeline(self, id_or_reference: str) -> dict:
        if not id_or_reference:
            raise APIError("ID or reference is required")
        return self.request("GET", f"transaction/timeline/{id_or_reference}")
    
    def totals(self) -> dict:
        return self.request("GET", "transaction/totals")
    
    def export(self) -> dict:
        return self.request("GET", "transaction/export")
            
    def partial_debit(self, payload=None, **kwargs):
        if payload is None:
            payload = kwargs
        elif not isinstance(payload, dict):
            raise APIError("Payload must be a dictionary")

        authorization_code = payload.get("authorization_code")
        currency = payload.get("currency")
        amount = payload.get("amount")
        email = payload.get("email")

        if not authorization_code:
            raise APIError("Authorization code is required")
        if not currency:
            raise APIError("Currency is required")
        if not amount:
            raise APIError("Amount is required")
        if not email:
            raise APIError("Email is required")
        if not validate_email(email):
            raise APIError("Invalid email format")

        try:
            amount_int = int(amount)
        except ValueError:
            raise APIError("Amount must be a valid number string without comma or decimal")

        if amount_int <= 0:
            raise APIError("Amount must be a positive number")
        elif amount_int < 10000:
            raise APIError("Amount must be at least ₦100 (10000 kobo)")
        elif amount_int > 1000000000:
            raise APIError("Amount must be less than ₦10,000,000 (1 billion kobo)")

        payload["amount"] = amount_int

        return self.request("POST", "transaction/partial_debit", json=payload)
