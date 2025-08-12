

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
    
    def list(self):
        """
        List transactions.

        Returns:
            dict: Response data from the Paystack API.
        """
        response = self.request("GET", "transaction")
        return response