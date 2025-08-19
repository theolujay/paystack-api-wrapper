"""The Customers API to create and manage customers."""

from typing import Optional, Dict, Any

from .core import BaseClient, PaystackResponse
from .exceptions import ValidationError
from .utils.helpers import validate_email

class CustomersAPI(BaseClient):
    """Customer API client for creating and managing customers."""
    
    def __init__(self, secret_key: Optional[str] = None):
        super().__init__(secret_key)
    
    def create(self, 
               email: str, 
               first_name: Optional[str] = None, 
               last_name: Optional[str] = None, 
               phone: Optional[str] = None,
               metadata: Optional[Dict[str, Any]] = None,
               validate_required_fields: bool = False) -> PaystackResponse:
        """Create a customer on your integration.
        
        Args:
            email (str): Customer's email address
            first_name (Optional[str]): Customer's first name
            last_name (Optional[str]): Customer's last name  
            phone (Optional[str]): Customer's phone number
            metadata (Optional[Dict]): Additional key/value pairs to store
            validate_required_fields (bool): If True, enforces first_name, last_name, 
                and phone as required (needed for Dedicated Virtual Accounts in certain 
                business categories: Betting, Financial services, General Service)
        
        Returns:
            PaystackResponse: Contains customer data including customer_code
            
        Raises:
            APIError: If required parameters are missing or invalid
        """
        validate_email(email)
        if validate_required_fields:
            self._validate_required_params(
                first_name=first_name,
                last_name=last_name, 
                phone=phone
            )
        
        payload = {"email": email}
        
        # Add optinoal fields if provided
        if first_name:
            payload["first_name"] = first_name
        if last_name:
            payload["last_name"] = last_name
        if phone:
            payload["phone"] = phone
        if metadata:
            payload["metadata"] = metadata
            
        return self.request("POST", "customer", json_data=payload)
    
    def list_customers(self,
                       per_page: Optional[int] = None,
                       page: Optional[int] = None,
                       from_date: Optional[str] = None,
                       to_date: Optional[str] = None) -> PaystackResponse:
        """List customers available on your integration.
        
        Args:
            per_page (Optional[int]): Number of records per page (default: 50)
            page (Optional[int]): Page number to retrieve (default: 1)
            from_date (Optional[str]): Start date filter (e.g. '2016-09-24T00:00:05.000Z')
            to_date (Optional[str]): End date filter (e.g. '2016-09-24T00:00:05.000Z')
        
        Returns:
            PaystackResponse: Contains list of customers and pagination metadata
        """
        params = {}
        
        if per_page is not None:
            params["perPage"] = per_page
        if page is not None:
            params["page"] = page
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date
            
        return self.request("GET", "customer", params=params)
    
    def fetch(self, email_or_code: str) -> PaystackResponse:
        """Get details of a customer on your integration.
        
        Args:
            email_or_code (str): Customer's email address or customer_code
        
        Returns:
            PaystackResponse: Contains detailed customer information including
                            transactions, subscriptions, and authorizations
        """
        self._validate_required_params(email_or_code=email_or_code)
        return self.request("GET", f"customer/{email_or_code}")
    
    def update(self, 
               code: str,
               first_name: Optional[str] = None,
               last_name: Optional[str] = None,
               phone: Optional[str] = None,
               metadata: Optional[Dict[str, Any]] = None) -> PaystackResponse:
        """Update a customer's details on your integration"""
        """Update a customer's details on your integration.
        
        Args:
            code (str): Customer's code
            first_name (Optional[str]): Customer's first name
            last_name (Optional[str]): Customer's last name
            phone (Optional[str]): Customer's phone number
            metadata (Optional[Dict]): Additional key/value pairs to store
            
        Returns:
            PaystackResponse: Contains updated customer data
        """
        self._validate_required_params(code=code)
        
        payload = {}
        if first_name is not None:
            payload["first_name"] = first_name
        if last_name is not None:
            payload["last_name"] = last_name
        if phone is not None:
            payload["phone"] = phone
        if metadata is not None:
            payload["metadata"] = metadata
            
        if not payload:
            raise ValidationError("At least one field must be provided for update")
            
        return self.request("PUT", f"customer/{code}", json_data=payload)

    def validate_identity(self, 
                         customer_code: str,
                         country: str,
                         identification_type: str,
                         first_name: str,
                         last_name: str,
                         **kwargs) -> PaystackResponse:
        """Validate a customer's identity.
        
        Args:
            customer_code (str): Customer's code
            country (str): 2-letter country code of identification issuer
            identification_type (str): Type of identification (e.g. 'bank_account')
            first_name (str): Customer's first name
            last_name (str): Customer's last name
            **kwargs: Additional fields like bvn, bank_code, account_number, etc.
            
        Returns:
            PaystackResponse: Validation status response
        """
        self._validate_required_params(
            customer_code=customer_code,
            country=country,
            identification_type=identification_type,
            first_name=first_name,
            last_name=last_name
        )
        
        payload = {
            "country": country,
            "type": identification_type,
            "first_name": first_name,
            "last_name": last_name,
            **kwargs
        }
        
        return self.request("POST", f"customer/{customer_code}/identification", json_data=payload)
    
    def set_risk_action(self, 
                       customer: str, 
                       risk_action: str) -> PaystackResponse:
        """Whitelist or blacklist a customer on your integration.
        
        Args:
            customer (str): Customer's code or email address
            risk_action (str): Risk action - 'default', 'allow' (whitelist), or 'deny' (blacklist)
            
        Returns:
            PaystackResponse: Updated customer data with new risk action
        """
        self._validate_required_params(customer=customer, risk_action=risk_action)
        
        if risk_action not in ["default", "allow", "deny"]:
            raise ValidationError(
                "risk_action must be one of: 'default', 'allow', 'deny'",
                field_errors={"risk_action": "Must be 'default', 'allow', or 'deny'"}
            )
        payload = {
            "customer": customer,
            "risk_action": risk_action
        }
        
        return self.request("POST", "customer/set_risk_action", json_data=payload)
    
    def initialize_authorization(self, 
                               email: str,
                               channel: str = "direct_debit",
                               callback_url: Optional[str] = None,
                               account: Optional[Dict] = None,
                               address: Optional[Dict] = None) -> PaystackResponse:
        """Initiate a request to create a reusable authorization code for recurring transactions.
        
        Args:
            email (str): Customer's email address
            channel (str): Authorization channel (currently only 'direct_debit' is supported)
            callback_url (Optional[str]): URL to redirect customer to after authorization
            account (Optional[Dict]): Customer's account details
            address (Optional[Dict]): Customer's address information
            
        Returns:
            PaystackResponse: Contains redirect_url, access_code, and reference
        """
        validate_email(email)
        
        payload = {
            "email": email,
            "channel": channel
        }
        
        if callback_url:
            payload["callback_url"] = callback_url
        if account:
            payload["account"] = account
        if address:
            payload["address"] = address
            
        return self.request("POST", "customer/authorization/initialize", json_data=payload)
    
    def verify_authorization(self, reference: str) -> PaystackResponse:
        """Check the status of an authorization request.
        
        Args:
            reference (str): The reference returned in the initialization response
            
        Returns:
            PaystackResponse: Contains authorization details and status
        """
        self._validate_required_params(reference=reference)
        return self.request("GET", f"customer/authorization/verify/{reference}")
    
    def initialize_direct_debit(self, 
                               customer_id: str,
                               account: Dict[str, str],
                               address: Dict[str, str]) -> PaystackResponse:
        """Initialize the process of linking an account to a customer for Direct Debit transactions.
        
        Args:
            customer_id (str): The ID of the customer
            account (Dict): Customer's account details (number, bank_code)
            address (Dict): Customer's address (street, city, state)
            
        Returns:
            PaystackResponse: Contains redirect_url, access_code, and reference
        """
        self._validate_required_params(customer_id=customer_id)
        
        if not account or "number" not in account or "bank_code" not in account:
            raise ValidationError(
                "account must contain 'number' and 'bank_code'",
                field_errors={"account": "Must contain 'number' and 'bank_code'"}
            )
        if not address or "street" not in address or "city" not in address or "state" not in address:
            raise ValidationError(
                "address must contain 'street', 'city', and 'state'",
                field_errors={"address": "Must contain 'street', 'city', and 'state'"}
            )
        
        payload = {
            "account": account,
            "address": address
        }
        
        return self.request("POST", f"customer/{customer_id}/initialize-direct-debit", json_data=payload)
    
    def direct_debit_activation_charge(self, 
                                     customer_id: str,
                                     authorization_id: int) -> PaystackResponse:
        """Trigger an activation charge on an inactive mandate on behalf of your customer.
        
        Args:
            customer_id (str): The ID of the customer
            authorization_id (int): The authorization ID from the initiation response
            
        Returns:
            PaystackResponse: Activation charge status
        """
        self._validate_required_params(customer_id=customer_id, authorization_id=authorization_id)
        
        payload = {"authorization_id": authorization_id}
        
        # Note: This should be PUT method as per API docs
        return self.request("PUT", f"customer/{customer_id}/directdebit-activation-charge", json_data=payload)
    
    def fetch_mandate_authorizations(self, customer_id: str) -> PaystackResponse:
        """Get the list of direct debit mandates associated with a customer.
        
        Args:
            customer_id (str): The ID of the customer
            
        Returns:
            PaystackResponse: List of mandate authorizations with pagination metadata
        """
        self._validate_required_params(customer_id=customer_id)
        return self.request("GET", f"customer/{customer_id}/directdebit-mandate-authorizations")
    
    def deactivate_authorization(self, authorization_code: str) -> PaystackResponse:
        """Deactivate an authorization for any payment channel.
        
        Args:
            authorization_code (str): Authorization code to be deactivated
            
        Returns:
            PaystackResponse: Deactivation confirmation
        """
        self._validate_required_params(authorization_code=authorization_code)
        
        payload = {"authorization_code": authorization_code}
        return self.request("POST", "customer/authorization/deactivate", json_data=payload)
    
    