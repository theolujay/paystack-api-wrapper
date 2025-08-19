# charge.py
from typing import Optional, Dict, Any, Union, Tuple
from .core import BaseClient
from .exceptions import ValidationError
from .utils.validators import _validate_amount_and_email, _validate_charge_authorization


class ChargeAPI(BaseClient):
    """Charge API client for processing payments with specific payment channels."""
    
    def __init__(self, secret_key: Optional[str] = None):
        super().__init__(secret_key)

    def create(self,
               email: str,
               amount: Union[int, str],
               split_code: Optional[str] = None,
               subaccount: Optional[str] = None,
               transaction_charge: Optional[int] = None,
               bearer: Optional[str] = None,
               bank: Optional[Dict[str, Any]] = None,
               bank_transfer: Optional[Dict[str, Any]] = None,
               ussd: Optional[Dict[str, Any]] = None,
               mobile_money: Optional[Dict[str, Any]] = None,
               qr: Optional[Dict[str, Any]] = None,
               authorization_code: Optional[str] = None,
               pin: Optional[str] = None,
               metadata: Optional[Dict[str, Any]] = None,
               reference: Optional[str] = None,
               device_id: Optional[str] = None,
               birthday: Optional[str] = None) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Initiate a payment by integrating the payment channel of your choice.

        Args:
            email (str): Customer's email address
            amount (Union[int, str]): Amount in subunit of the supported currency
            split_code (Optional[str]): The split code of a previously created split. e.g. SPL_98WF13Eb3w
            subaccount (Optional[str]): The code for the subaccount that owns the payment. e.g. ACCT_8f4s1eq7ml6rlzj
            transaction_charge (Optional[int]): An amount used to override the split configuration for a single split payment
            bearer (Optional[str]): Who bears Paystack charges ('account' or 'subaccount')
            bank (Optional[Dict]): Bank account to charge (don't send if charging an authorization code)
            bank_transfer (Optional[Dict]): Settings for the Pay with Transfer (PwT) channel
            ussd (Optional[Dict]): USSD type to charge (don't send if charging an authorization code, bank or card)
            mobile_money (Optional[Dict]): Mobile money details (Ghana and Kenya only)
            qr (Optional[Dict]): QR payment details with provider object
            authorization_code (Optional[str]): An authorization code to charge (don't send if charging a bank account)
            pin (Optional[str]): 4-digit PIN (send with a non-reusable authorization code)
            metadata (Optional[Dict]): Additional details for post-payment processes
            reference (Optional[str]): Unique transaction reference. Only -, ., = and alphanumeric characters allowed
            device_id: (Optional[str]): Unique identifier of the device used for payment
            birthday (Optional[str]): Customer's birthday in YYYY-MM-DD format

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.

        Raises:
            ValidationError: If email or amount is invalid, or if conflicting payment methods are provided
        """
        _validate_amount_and_email(email, str(amount))
        
        payload = {
            "email": email,
            "amount": str(amount)
        }
        
        # Add optional fields
        if split_code:
            payload["split_code"] = split_code
        if subaccount:
            payload["subaccount"] = subaccount
        if transaction_charge is not None:
            payload["transaction_charge"] = transaction_charge
        if bearer:
            if bearer not in ["account", "subaccount"]:
                raise ValidationError(
                    "bearer must be either 'account' or 'subaccount'",
                    field_errors={"bearer": "Must be 'account' or 'subaccount'"}
                )
            payload["bearer"] = bearer
        if bank:
            payload["bank"] = bank
        if bank_transfer:
            payload["bank_transfer"] = bank_transfer
        if ussd:
            payload["ussd"] = ussd
        if mobile_money:
            payload["mobile_money"] = mobile_money
        if qr:
            payload["qr"] = qr
        if authorization_code:
            payload["authorization_code"] = authorization_code
        if pin:
            payload["pin"] = pin
        if metadata:
            # Convert metadata dict to JSON string as per API requirements
            import json
            payload["metadata"] = json.dumps(metadata) if isinstance(metadata, dict) else metadata
        if reference:
            payload["reference"] = reference
        if device_id:
            payload["device_id"] = device_id
        if birthday:
            payload["birthday"] = birthday
            
        return self.request("POST", "charge", json_data=payload)

    def submit_pin(self, pin: str, reference: str) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Submit PIN to continue a charge.

        Args:
            pin (str): PIN submitted by user
            reference (str): Reference for transaction that requested pin

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.

        Raises:
            APIError: If pin or reference is not provided
        """
        self._validate_required_params(pin=pin, reference=reference)
        
        payload = {
            "pin": pin,
            "reference": reference
        }
        
        return self.request("POST", "charge/submit_pin", json_data=payload)

    def submit_otp(self, otp: str, reference: str) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Submit OTP to complete a charge.

        Args:
            otp (str): OTP submitted by user
            reference (str): Reference for ongoing transaction

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.

        Raises:
            APIError: If otp or reference is not provided
        """
        self._validate_required_params(otp=otp, reference=reference)
        
        payload = {
            "otp": otp,
            "reference": reference
        }
        
        return self.request("POST", "charge/submit_otp", json_data=payload)

    def submit_phone(self, phone: str, reference: str) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Submit phone number when requested.

        Args:
            phone (str): Phone number submitted by user
            reference (str): Reference for ongoing transaction

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.

        Raises:
            APIError: If phone or reference is not provided
        """
        self._validate_required_params(phone=phone, reference=reference)
        
        payload = {
            "phone": phone,
            "reference": reference
        }
        
        return self.request("POST", "charge/submit_phone", json_data=payload)

    def submit_birthday(self, birthday: str, reference: str) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Submit birthday when requested.

        Args:
            birthday (str): Birthday submitted by user in YYYY-MM-DD format (e.g. '2016-09-21')
            reference (str): Reference for ongoing transaction

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.

        Raises:
            APIError: If birthday or reference is not provided
        """
        self._validate_required_params(birthday=birthday, reference=reference)
        
        payload = {
            "birthday": birthday,
            "reference": reference
        }
        
        return self.request("POST", "charge/submit_birthday", json_data=payload)

    def submit_address(self, 
                      address: str,
                      reference: str,
                      city: str,
                      state: str,
                      zip_code: str) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Submit address to continue a charge.

        Args:
            address (str): Address submitted by user
            reference (str): Reference for ongoing transaction
            city (str): City submitted by user
            state (str): State submitted by user
            zipcode (str): Zipcode submitted by user

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.

        Raises:
            APIError: If any required parameter is not provided
        """
        self._validate_required_params(
            address=address, 
            reference=reference, 
            city=city, 
            state=state, 
            zip_code=zip_code
        )
        
        payload = {
            "address": address,
            "reference": reference,
            "city": city,
            "state": state,
            "zip_code": zip_code
        }
        
        return self.request("POST", "charge/submit_address", json_data=payload)

    def check_pending_charge(self, reference: str) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Check the status of a pending charge.
        
        When you get 'pending' as a charge status or if there was an exception when calling 
        any of the /charge endpoints, wait 10 seconds or more, then make a check to see if 
        its status has changed. Don't call too early as you may get a lot more pending than you should.

        Args:
            reference (str): The reference to check

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.

        Raises:
            APIError: If reference is not provided
        """
        self._validate_required_params(reference=reference)
        return self.request("GET", f"charge/{reference}")