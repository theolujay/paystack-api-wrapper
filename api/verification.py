"""
The Verification API allows you perform KYC processes.
"""
from typing import Optional

from .core import BaseClient, PaystackResponse


class VerificationAPI(BaseClient):
    """
    The Verification API allows you perform KYC processes.
    """

    def __init__(self, secret_key: Optional[str] = None):
        super().__init__(secret_key)

    def resolve_account(self, account_number: str, bank_code: str) -> PaystackResponse:
        """
        Confirm an account belongs to the right customer.

        Args:
            account_number: Account Number
            bank_code: You can get the list of bank codes by calling the List Banks endpoint

        Returns:
            PaystackResponse: The response from the API
        """
        self._validate_required_params(account_number=account_number, bank_code=bank_code)

        params = {
            "account_number": account_number,
            "bank_code": bank_code,
        }
        return self.request("GET", "bank/resolve", params=params)

    def validate_account(self,
                         account_name: str,
                         account_number: str,
                         account_type: str,
                         bank_code: str,
                         country_code: str,
                         document_type: str,
                         document_number: Optional[str] = None) -> PaystackResponse:
        """
        Confirm the authenticity of a customer's account number before sending money.

        Args:
            account_name: Customer's first and last name registered with their bank
            account_number: Customer’s account number
            account_type: This can take one of: [ personal, business ]
            bank_code: The bank code of the customer’s bank. You can fetch the bank codes by using our List Banks endpoint
            country_code: The two digit ISO code of the customer’s bank
            document_type: Customer’s mode of identity. This could be one of: [ identityNumber, passportNumber, businessRegistrationNumber ]
            document_number: Customer’s mode of identity number

        Returns:
            PaystackResponse: The response from the API
        """
        self._validate_required_params(
            account_name=account_name,
            account_number=account_number,
            account_type=account_type,
            bank_code=bank_code,
            country_code=country_code,
            document_type=document_type,
        )

        payload = {
            "account_name": account_name,
            "account_number": account_number,
            "account_type": account_type,
            "bank_code": bank_code,
            "country_code": country_code,
            "document_type": document_type,
        }
        if document_number:
            payload['document_number'] = document_number

        return self.request("POST", "bank/validate", json_data=payload)

    def resolve_card_bin(self, card_bin: str) -> PaystackResponse:
        """
        Get more information about a customer's card.

        Args:
            card_bin: First 6 characters of card

        Returns:
            PaystackResponse: The response from the API
        """
        self._validate_required_params(card_bin=card_bin)

        return self.request("GET", f"decision/bin/{card_bin}")
