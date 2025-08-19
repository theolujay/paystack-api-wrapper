# Paystack Python Client

[![PyPI Version](https://img.shields.io/pypi/v/paystack-client)](https://pypi.org/project/paystack-client/)
[![Python Versions](https://img.shields.io/pypi/pyversions/paystack-client)](https://pypi.org/project/paystack-client/)
[![License](https://img.shields.io/pypi/l/paystack-client)](https://github.com/theolujay/paystack-client/blob/main/LICENSE)
[![Build Status](https://img.shields.io/github/actions/workflow/status/theolujay/paystack-client/ci.yml?branch=main)](https://github.com/theolujay/paystack-client/actions)
[![Coverage Status](https://img.shields.io/codecov/c/github/theolujay/paystack-client)](https://codecov.io/gh/theolujay/paystack-client)

A modern, intuitive, and robust Python wrapper for the [Paystack API](https://paystack.com/docs/api/). This library is designed to make integrating Paystack into your Python applications simple and convenient, with a focus on code quality, clarity, and robust error handling.

## Features

*   **Complete API Coverage**: Provides access to all Paystack API endpoints.
*   **Intuitive Design**: A clean, object-oriented structure that's easy to understand and use.
*   **Type-Hinted**: Fully type-hinted for better editor support (like autocompletion) and static analysis.
*   **Robust Error Handling**: Raises a custom `APIError` for all API-related issues, providing clear feedback.
*   **Standardized Responses**: Wraps all API responses in a consistent `PaystackResponse` object.
*   **Minimal Dependencies**: Only requires `requests` for HTTP communication and `python-dotenv` for environment variable management.

## Installation

You can install the library using pip:

```bash
pip install paystack-client
```

## Usage

### Initializing the Client

First, instantiate the `PaystackClient` with your secret key. It's highly recommended to store your secret key as an environment variable and not hardcode it in your application.

```python
import os
from paystack_client import PaystackClient
from paystack_client.api.exceptions import APIError

# Load your secret key from an environment variable
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
    response = client.transactions.initialize(
        email="customer@example.com",
        amount=50000,  # Amount in the subunit (kobo for NGN)
        currency="NGN"
    )
    
    # The actual data is in the `data` attribute
    print(response.data)
    # Expected output:
    # {'authorization_url': '...', 'access_code': '...', 'reference': '...'}

except APIError as e:
    print(f"An error occurred: {e}")
```

### Handling Responses

Every successful API call returns a `PaystackResponse` object. This object standardizes the structure of the response from Paystack.

*   `response.data`: Contains the primary data from the API call. This can be a `dict` (for single objects) or a `list` of `dict`s (for lists).
*   `response.message`: A descriptive message from the API (e.g., "Customers retrieved").
*   `response.meta`: For paginated results, this `dict` contains pagination details like `total`, `page`, `perPage`, etc.
*   `response.is_paginated`: A boolean property that is `True` if the response contains pagination metadata.

**Example with a paginated response:**

```python
try:
    # List the first 5 customers
    response = client.customers.list_customers(per_page=5)

    if response.is_paginated:
        print(f"Total Customers: {response.meta['total']}")
        print(f"Current Page: {response.meta['page']} of {response.meta['pageCount']}")

    for customer in response.data:
        print(f"- {customer['first_name']} {customer['last_name']} ({customer['email']})")

except APIError as e:
    print(f"An error occurred: {e}")
```

### Error Handling

The library raises a custom `APIError` for any issues encountered while communicating with the Paystack API. This includes network errors, invalid authentication, or bad requests. You should wrap your API calls in a `try...except` block to handle these exceptions gracefully.

The `APIError` exception has the following properties:
*   `e.message`: The error message.
*   `e.status_code`: The HTTP status code of the response, if available.

```python
try:
    # This will fail because the reference is invalid
    client.transactions.verify(reference="an-invalid-reference")
except APIError as e:
    print(f"API Error: {e.message}")
    print(f"HTTP Status Code: {e.status_code}")
```

## Available APIs

The client provides access to the following Paystack API resources. Each resource corresponds to a property on the `PaystackClient` instance.

- `apple_pay`
- `bulk_charges`
- `charge`
- `customers`
- `dedicated_virtual_accounts`
- `direct_debit`
- `disputes`
- `integration`
- `miscellaneous`
- `payment_pages`
- `payment_requests`
- `plans`
- `products`
- `refunds`
- `settlements`
- `subaccounts`
- `subscriptions`
- `terminal`
- `transactions`
- `transaction_splits`
- `transfers`
- `transfers_control`
- `transfer_recipients`
- `verification`
- `virtual_terminal`

## Contributing

Contributions are welcome! If you find a bug or have a feature request, please open an issue. If you want to contribute code, please open a pull request.

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature-name`).
3.  Make your changes and commit them (`git commit -m 'Add some feature'`).
4.  Push to the branch (`git push origin feature/your-feature-name`).
5.  Open a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.