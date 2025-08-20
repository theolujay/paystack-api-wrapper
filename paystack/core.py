import os
import re
import requests
from typing import Optional, Dict, Any, Tuple, Union
from requests.exceptions import JSONDecodeError

from .exceptions import (
    APIError,
    ValidationError,
    AuthenticationError,
    NetworkError,
    InvalidResponseError,
    TransactionFailureError,
    create_error_from_response,
)


class BaseClient:
    """Base client for interacting with the Paystack API.

    This class handles authentication, request formatting, response parsing,
    and error handling for all Paystack API endpoints.
    """

    def __init__(
        self,
        secret_key: str,
        base_url: str = "https://api.paystack.co/",
        session: requests.Session = None,
        timeout: int = 10,
    ):
        self.secret_key = secret_key
        if not self.secret_key.startswith(("sk_test", "sk_live")):
            raise AuthenticationError(
                "Invalid Paystack secret key format. Key should start with 'sk_test_' or 'sk_live_'"
            )
        self.base_url = base_url
        self.timeout = timeout
        self.session = session or requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {self.secret_key}",
                "Content-Type": "application/json",
                "User-Agent": "paystack-client/1.0.0",
            }
        )

    def request(
        self,
        method: str,
        endpoint: str,
        json_data: Optional[Dict] = None,
        params: Optional[Dict] = None,
        private: bool = True,
        idempotency_key: Optional[str] = None,
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Send an HTTP request to Paystack API with proper headers and error handling.

        Args:
            method (str): HTTP method (GET, POST, PUT, DELETE).
            endpoint (str): API endpoint path, e.g. "transaction/initialize".
            json_data (Optional[Dict]): JSON payload for POST/PUT requests.
            params (Optional[Dict]): Query parameters for the request.
            private (bool): Whether to send Authorization header.
            idempotency_key (Optional[str]): Idempotency key for POST requests.

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.

        Raises:
            PaystackError: Various subclasses depending on the error type.
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

            request_id = response.headers.get(
                "x-amzn-requestid"
            ) or response.headers.get("cf-ray")

            try:
                resp_json = response.json()
            except (ValueError, JSONDecodeError) as e:
                raise InvalidResponseError(
                    f"Invalid JSON response: {e}",
                    status_code=response.status_code,
                    request_id=request_id,
                ) from e

            # Handle HTTP status codes
            if response.status_code in [200, 201]:
                return self._handle_success_response(
                    resp_json, response.status_code, request_id
                )
            else:
                # Use the factory function to create appropriate exception
                # For RateLimitError, pass the original response object to access headers
                if response.status_code == 429:
                    raise create_error_from_response(
                        response=response,  # Pass the original response object
                        status_code=response.status_code,
                        request_id=request_id,
                    )
                else:
                    raise create_error_from_response(
                        response=resp_json,
                        status_code=response.status_code,
                        request_id=request_id,
                    )
        except requests.exceptions.ConnectTimeout:
            raise NetworkError("Connection timed out - check your internet connection")
        except requests.exceptions.ReadTimeout:
            raise NetworkError(f"Request timed out after {self.timeout} seconds")
        except requests.exceptions.ConnectionError as e:
            raise NetworkError(f"Connection error: {e}")
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Request failed: {e}")

    def _handle_success_response(
        self, resp_json: Dict, status_code: int, request_id: Optional[str]
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Handle successful HTTP responses (200, 201).

        Important: Paystack returns Http 200 even for failed operations!
        We need to check th 'status' field in the response.
        """
        if not isinstance(resp_json, dict):
            raise InvalidResponseError(
                f"Expected JSON object, got {type(resp_json)}",
                status_code=status_code,
                request_id=request_id,
            )

        if "status" not in resp_json or "message" not in resp_json:
            raise InvalidResponseError(
                "Invalid Paystack response structure: missing 'status' or 'message'",
                status_code=status_code,
                request_id=request_id,
                response=resp_json,
            )

        # Check if Paystack reported an error (even with HTTP 200)
        paystack_status = resp_json.get("status", False)
        if paystack_status is False:
            error_message = resp_json.get("message", "Unknown API error")
            field_errors = None
            if "errors" in resp_json and isinstance(resp_json["errors"], dict):
                field_errors = resp_json["errors"]
                raise ValidationError(
                    message=error_message,
                    field_errors=field_errors,
                    status_code=status_code,
                    response=resp_json,
                    request_id=request_id,
                )

            # Generic API error with HTTP 200 but status: false
            raise APIError(
                message=f"API request failed: {error_message}",
                status_code=status_code,
                response=resp_json,
                request_id=request_id,
            )
        # Check for failed transactions (HTTP 200, status: true, but transaction failed)
        data = resp_json.get("data")
        if isinstance(data, dict):
            transaction_status = data.get("status")
            if transaction_status in ["failed", "abandoned", "cancelled"]:
                gateway_response = data.get("gateway_response", "Transaction failed")
                raise TransactionFailureError(
                    message=f"Transaction failed: {transaction_status}",
                    status_code=status_code,
                    response=resp_json,
                    request_id=request_id,
                    gateway_response=gateway_response,
                )

        # Extract response components
        meta = resp_json.get("meta", {})

        return data, meta

    def _build_url(self, endpoint: str) -> str:
        """Build full URL from endpoint."""
        endpoint = endpoint.lstrip("/")  # Remove leading slash if present
        return f"{self.base_url}/{endpoint}"

    def _validate_required_params(self, *args, **kwargs):
        """
        Validate that required parameters are provided and not empty.

        Raises ValidationError for missing required parameters.
        """
        missing_params = []

        # Ensure no positional arguments are passed
        if args:
            raise TypeError("Positional arguments are not allowed for this method.")

        for param_name, param_value in kwargs.items():
            if param_value is None or (
                isinstance(param_value, str) and not param_value.strip()
            ):
                missing_params.append(param_name)

        if missing_params:
            raise ValidationError(
                message=f"Missing required parameters: {', '.join(missing_params)}",
                field_errors={
                    param: "This field is required" for param in missing_params
                },
            )

    def _validate_amount(self, amount: Union[int, str], currency: str = "NGN"):
        """
        Validate transaction amounts according to Paystack rules.

        Args:
            amount: Amount in the smallest currency unit (kobo for NGN)
            currency: Currency code

        Raises:
            ValidationError: If amount is invalid
        """
        try:
            amount_int = int(amount)
        except (ValueError, TypeError):
            raise ValidationError(
                message="Amount must be a valid integer or string representation of an integer",
                field_errors={"amount": "Must be a valid integer value"},
            )

        # Minimum amounts by currency (in smallest unit)
        min_amounts = {
            "NGN": 100,  # ₦1.00 in kobo
            "USD": 50,  # $0.50 in cents
            "GHS": 100,  # GH₵1.00 in pesewas
        }

        min_amount = min_amounts.get(currency, 100)
        if amount_int < min_amount:
            raise ValidationError(
                message=f"Amount too small for {currency}",
                field_errors={
                    "amount": f"Minimum amount is {min_amount} {currency} subunits"
                },
            )

    def _validate_email(self, email: str):
        """
        Email validation for Paystack requirements

        Args:
            email (str): The email address to validate.

        Raises:
                ValidationError: If email format is invalid
        """
        if not email or not isinstance(email, str) or len(email) > 254:
            raise ValidationError(
                message="Email is required",
                field_errors={"email": "Email address is required"},
            )

        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

        if not re.match(pattern, email):
            raise ValidationError(
                message="Invalid email format",
                field_errors={"email": "Please provide a valid email address"},
            )

    def __repr__(self):
        masked_key = (
            f"{self.secret_key[:7]}***{self.secret_key[-4:]}"
            if self.secret_key
            else "None"
        )
        return f"BaseClient(secret_key={masked_key}, base_url='{self.base_url}')"
