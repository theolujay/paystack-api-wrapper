# Paystack Python Client

[![PyPI Version](https://img.shields.io/pypi/v/paystack-client)](https://pypi.org/project/paystack-client/)
[![Python Versions](https://img.shields.io/pypi/pyversions/paystack-client)](https://pypi.org/project/paystack-client/)
[![License](https://img.shields.io/pypi/l/paystack-client)](https://github.com/theolujay/paystack_client/blob/main/LICENSE)
[![Build Status](https://img.shields.io/github/actions/workflow/status/theolujay/paystack_client/ci.yml?branch=main)](https://github.com/theolujay/paystack_client/actions)
[![Coverage Status](https://img.shields.io/codecov/c/github/theolujay/paystack_client)](https://codecov.io/gh/theolujay/paystack_client)

A modern, intuitive, and robust Python wrapper for the [Paystack API](https://paystack.com/docs/api/). This library is designed to make integrating Paystack into your Python applications simple and convenient, with a focus on code quality, clarity, and robust error handling.

## Features

*   **Complete API Coverage**: Provides access to all Paystack API endpoints.
*   **Intuitive Design**: A clean, object-oriented structure that's easy to understand and use.
*   **Type-Hinted**: Fully type-hinted for better editor support (like autocompletion) and static analysis.
*   **Robust Error Handling**: Raises specific, custom exceptions for different API errors (e.g., `ValidationError`, `AuthenticationError`), all inheriting from a base `PaystackError`.
*   **Consistent Responses**: All API methods return a consistent `(data, meta)` tuple.
*   **Minimal Dependencies**: Only requires `requests` for HTTP communication and `python-dotenv` for environment variable management.

## Installation

You can install the library using pip:

```bash
pip install paystack-client
```

## Usage

### Initializing the Client

First, instantiate the `PaystackClient` with your secret key. It's highly recommended to store your secret key as an environment variable (e.g., `PAYSTACK_SECRET_KEY`) and load it using `python-dotenv` or similar methods, rather than hardcoding it.

```python
import os
from paystack_client import PaystackClient
from paystack_client.exceptions import APIError # Import specific exceptions

# Load your secret key from an environment variable
# Ensure PAYSTACK_SECRET_KEY is set in your environment or a .env file
secret_key = os.getenv("PAYSTACK_SECRET_KEY")

if not secret_key:
    raise ValueError("PAYSTACK_SECRET_KEY environment variable not set.")

client = PaystackClient(secret_key=secret_key)
```

### Basic Example: Initializing a Transaction

All API resources are available as properties on the `client` object. For example, to access the Transactions API, you use `client.transactions`.

```python
try:
    # Initialize a transaction
    data, meta = client.transactions.initialize(
        email="customer@example.com",
        amount=50000,  # Amount in the subunit (kobo for NGN)
        currency="NGN"
    )
    
    # The primary response data is in the 'data' variable
    print(data)
    # Expected output (example):
    # {'authorization_url': 'https://checkout.paystack.com/...', 'access_code': '...', 'reference': '...'}

except APIError as e:
    print(f"An error occurred: {e.message}")
    if e.status_code:
        print(f"HTTP Status Code: {e.status_code}")
```

### Handling Responses

Every successful API call returns a `(data, meta)` tuple. This structure provides a consistent way to access the API response.

*   `data`: Contains the primary data from the API call. This can be a `dict` (for single objects) or a `list` of `dict`s (for lists).
*   `meta`: For paginated results, this `dict` contains pagination details like `total`, `page`, `perPage`, etc. If the response is not paginated, `meta` will be an empty dictionary.

**Example with a paginated response (e.g., listing customers):**

```python
from paystack_client.paystack_client.exceptions import APIError

try:
    # List the first 5 customers
    customers_data, customers_meta = client.customers.list_customers(per_page=5)

    if customers_meta: # Check if meta is not empty, indicating pagination
        print(f"Total Customers: {customers_meta.get('total')}")
        print(f"Current Page: {customers_meta.get('page')} of {customers_meta.get('pageCount')}")

    for customer in customers_data:
        print(f"- {customer.get('first_name')} {customer.get('last_name')} ({customer.get('email')})")

except APIError as e:
    print(f"An error occurred: {e.message}")
```

### Robust Error Handling

The library provides a comprehensive set of custom exceptions, all inheriting from `paystack_client.paystack_client.exceptions.APIError`. This allows for granular error handling based on the type of issue encountered.

Key exception classes:

*   `APIError`: Base exception for all Paystack API related errors.
*   `AuthenticationError`: Raised for invalid or missing API keys.
*   `NetworkError`: Raised for network connectivity issues (e.g., timeouts, connection refused).
*   `InvalidResponseError`: Raised when the API returns an unexpected or malformed response.
*   `ValidationError`: Raised when input parameters fail validation (either client-side or API-side).
*   `TransactionFailureError`: Specifically for transactions that fail on Paystack's end, even if the HTTP status is 200.

You should wrap your API calls in `try...except` blocks to handle these exceptions gracefully.

```python
from paystack_client.paystack_client.exceptions import (
    APIError,
    AuthenticationError,
    ValidationError,
    NetworkError,
    TransactionFailureError
)

try:
    # Example of an invalid call that might raise an error
    data, meta = client.transactions.verify(reference="an-invalid-reference-that-does-not-exist")
    print(data)

except AuthenticationError as e:
    print(f"Authentication Error: {e.message}")
    # Handle invalid secret key
except ValidationError as e:
    print(f"Validation Error: {e.message}")
    if e.field_errors:
        print(f"Field Errors: {e.field_errors}")
    # Handle invalid input parameters
except NetworkError as e:
    print(f"Network Error: {e.message}")
    # Handle connectivity issues
except TransactionFailureError as e:
    print(f"Transaction Failed: {e.message}")
    print(f"Gateway Response: {e.gateway_response}")
    # Handle failed transactions
except APIError as e:
    print(f"Generic API Error: {e.message}")
    if e.status_code:
        print(f"HTTP Status Code: {e.status_code}")
    # Catch any other API-related errors
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    # Catch any other unexpected Python errors
```

## Available APIs

The client provides access to the following Paystack API resources. Each resource corresponds to a property on the `PaystackClient` instance:

-   `apple_pay`
-   `bulk_charges`
-   `charge`
-   `customers`
-   `dedicated_virtual_accounts`
-   `direct_debit`
-   `disputes`
-   `integration`
-   `miscellaneous`
-   `payment_pages`
-   `payment_requests`
-   `plans`
-   `products`
-   `refunds`
-   `settlements`
-   `subaccounts`
-   `subscriptions`
-   `terminal`
-   `transactions`
-   `transaction_splits`
-   `transfers`
-   `transfers_control`
-   `transfer_recipients`
-   `verification`
-   `virtual_terminal`

## Contributing

Contributions are welcome! If you find a bug or have a feature request, please open an issue. If you want to contribute code, please open a pull request.

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature-name`).
3.  Make your changes and commit them (`git commit -m 'Add some feature'`).
4.  Push to the branch (`git push origin feature/your-feature-name`).
5.  Open a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
