import os
import requests
from typing import Optional, Dict, Any
from requests.exceptions import JSONDecodeError, HTTPError, Timeout

from .exceptions import APIError

class PaystackResponse:
    """Wrapper for Paystack API responses to provide consistent interface."""
    
    def __init__(self, data: Any, meta: Optional[Dict] = None, message: str = ""):
        self.data = data
        self.meta = meta
        self.message = message
        
    @property
    def is_paginated(self) -> bool:
        """Check if this is a paginated response."""
        return self.meta is not None
    
    def __repr__(self):
        return f"PaystackResponse(data={self.data}, meta={self.meta}"
        
class BaseClient:
    """Base client for interacting with the Paystack API."""
    def __init__(self,
                 secret_key: Optional[str] = None,
                 base_url: Optional[str] = None,
                 timeout: int = 10):
        self.secret_key = secret_key or os.environ.get("PAYSTACK_SECRET_KEY")
        self.base_url = base_url or "https://api.paystack.co"
        self.timeout = timeout
        
        if not self.secret_key:
            raise ValueError("Paystack secret key is required. Set PAYSTACK_SERCRET_KEY environment variable or pass secret_key parameter.")
        
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.secret_key}",
            "Content-Type": "application/json",
        })


    def request(self, 
                method: str, 
                endpoint: str, 
                json_data: Optional[Dict] = None,
                params: Optional[Dict] = None,
                private: bool = True, 
                idempotency_key: Optional[str] = None) -> PaystackResponse:
        """Send an HTTP request to Paystack API with proper headers and error handling.

        Args:
            method (str): HTTP method (GET, POST, PUT, DELETE).
            endpoint (str): API endpoint path, e.g. "transaction/initialize".
            json_data (Optional[Dict]): JSON payload for POST/PUT requests.
            params (Optional[Dict]): Query parameters for the request.
            private (bool): Whether to send Authorization header.
            idempotency_key (Optional[str]): Idempotency key for POST requests.

        Returns:
            PaystackResponse: Wrapped response with data, meta, and message.

        Raises:
            APIError: If Paystack reports an error or response structure is invalid.
        """
        url = self._build_url(endpoint)
        headers = self.session.headers.copy()
        
        if not private and "Authorization" in headers:
            headers.pop("Authorization")
        
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key
            
        try:
            response = self.session.request(
                method=method.upper(),
                url=url,
                headers=headers,
                json=json_data,
                params=params,
                timeout=self.timeout,
            )
            response.raise_for_status()
            # resp_json = response.json()
            try:
                resp_json = response.json()
            except (ValueError, JSONDecodeError) as e:
                raise APIError(f"Invalid JSON response: {e}") from e

        except Timeout as e:
            raise APIError(f"Request timed out: {self.timeout}s: {e}") from e
        except HTTPError as e:
            error_msg = f"HTTP error {response.status_code}"
            try:
                error_json = response.json()
                if "message" in error_json:
                    error_msg += f": {error_json['message']}"
            except (ValueError, JSONDecodeError):
                pass
            raise APIError(error_msg) from e
        except requests.RequestException as e:
            raise APIError(f"Request failed: {e}") from e

        # Validate Paystack response structure
        if not isinstance(resp_json, dict):
            raise APIError(f"Expected JSON object, got {type(resp_json)}")
        
        if "status" not in resp_json or "message" not in resp_json:
            raise APIError(f"Invalid Paystack response structure: missing 'status' or 'message'")
    
        # Check if API reported an error
        if not resp_json.get("status", False):
            error_message = resp_json.get("message", "Unknown API error")
            raise APIError(f"Paystack API error: {error_message}")

        # Extract data and meta information
        data = resp_json.get("data")
        meta = resp_json.get("meta")
        message = resp_json.get("message")

        return PaystackResponse(data=data, meta=meta, message=message)

    def _build_url(self, endpoint: str) -> str:
        """Build full URL from endpoint."""
        endpoint = endpoint.lstrip("/") # Remove leading slash if present
        return f"{self.base_url}/{endpoint}"
    
    def _validate_required_params(self, **params):
        """Validate that required parameters are provided and not empty."""
        for param_name, param_value in params.items():
            if param_value is None or (isinstance(param_value, str) and not param_value.strip()):
                raise APIError(f"{param_name} is required and cannot be empty")