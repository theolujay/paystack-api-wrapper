import os
import requests
import json
from typing import Optional
from requests.exceptions import JSONDecodeError
from requests.exceptions import HTTPError, Timeout

from .exceptions import APIError

class BaseClient:
    """Base client for interacting with the Paystack API."""
    def __init__(self,
                 secret_key: Optional[str] = None,
                 base_url: Optional[str] = None,
                 timeout: int = 10):
        self.secret_key = secret_key or os.environ.get("PAYSTACK_SECRET_KEY")
        self.base_url = base_url or "https://api.paystack.co"
        self.timeout = timeout
        
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json"
        })
        
        if self.secret_key:
            self.session.headers["Authorization"] = f"Bearer {self.secret_key}"

    def request(self, method: str, endpoint: str, private: bool = True, idempotency_key: Optional[str] = None, **kwargs):
        """Send an HTTP request to Paystack API with proper headers and error handling.

        Args:
            method (str): HTTP method (GET, POST, etc.).
            endpoint (str): API endpoint path, e.g. "transaction/initialize".
            private (bool): Whether to send Authorization header.
            idempotency_key (Optional[str]): Idempotency key for POST requests.
            **kwargs: Additional arguments to requests.request.

        Returns:
            dict: 'data' part of Paystack JSON response.

        Raises:
            APIError: If Paystack reports an error or response structure is invalid.
            requests.HTTPError: For non-2xx HTTP status codes.
        """
        url = self._full_url(endpoint)
        
        if private and not self.secret_key:
            raise ValueError("secret_key missing for required authorization")
        
        headers = self.session.headers.copy()
        
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key
            
        if not private and "Authorization" in headers:
            headers.pop("Authorization")
            
        try:
            response = self.session.request(
                method=method.upper(),
                url=url,
                headers=headers,
                timeout=self.timeout,
                **kwargs
            )
            response.raise_for_status()
            resp_json = response.json()
        except Timeout as e:
            raise APIError(f"Request timed out: {e}") from e
        except HTTPError as e:
            raise APIError(f"HTTP error {response.status_code}: {e}") from e
        except (ValueError, JSONDecodeError, json.JSONDecodeError)as e:
            raise APIError(f"Invalid JSON response: {e}") from e
    
        # Validate Paystack response format
        if "status" not in resp_json or "message" not in resp_json or "data" not in resp_json:
            raise APIError(f"Unexpected response structure from Paystack: {resp_json}")
    
        if not resp_json["status"]:
            raise APIError(f"API error: {resp_json['message']}")

        # Success: also handles pagination with 'data' payload
        if "meta" in resp_json and isinstance(resp_json["data"], list):
            return resp_json["data"], resp_json["meta"]
        # Success: return just the 'data' payload if no pagination
        return resp_json["data"]


    def _full_url(self, endpoint: str) -> str:
        return f"{self.base_url}/{endpoint}"
    
    
    