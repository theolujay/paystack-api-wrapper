# Paystack Python Client: Full Usage Guide

This guide provides a detailed walkthrough of the `paystack-client` library, covering initialization, making API calls, handling responses, robust error management, and other advanced topics.

For a brief overview, see the main [README.md](../README.md).

## 1. Client Initialization

First, instantiate the `PaystackClient` with your secret key. It is strongly recommended to store your secret key as an environment variable (e.g., `PAYSTACK_SECRET_KEY`) rather than hardcoding it in your application.

```python
import os
from paystack_client import PaystackClient

# Best practice: load your secret key from environment variables
secret_key = os.getenv("PAYSTACK_SECRET_KEY")

if not secret_key:
    raise ValueError("PAYSTACK_SECRET_KEY environment variable not set.")

# Create the client instance
client = PaystackClient(secret_key=secret_key)
```

The `client` object is your gateway to all Paystack APIs.

## 2. Making API Calls

All API resources are available as properties on the `client` object. The structure is intuitive and follows the pattern: `client.<resource>.<method>()`.

For example, to access the **Transactions API**, you use `client.transactions`. To access the **Customers API**, you use `client.customers`.

### Example: Creating a Customer

```python
from paystack_client.exceptions import APIError

try:
    data, meta = client.customers.create(
        email="customer@example.com",
        first_name="John",
        last_name="Doe",
        phone="+2348012345678"
    )
    print("Customer created successfully:", data)
    # Expected output: {'integration': 100032, 'domain': 'test', 'customer_code': 'CUS_123abc', ...}

except APIError as e:
    print(f"An error occurred: {e.message}")
```

### Example: Fetching a Transaction

```python
from paystack_client.exceptions import APIError

try:
    # Replace with a real transaction ID from your integration
    transaction_id = 123456789
    data, meta = client.transactions.fetch(transaction_id=transaction_id)
    
    print("Transaction details:", data)
    # Expected output: {'id': 123456789, 'status': 'success', 'amount': 50000, ...}

except APIError as e:
    print(f"An error occurred: {e.message}")
```

## 3. Handling Responses

Every successful API call returns a `(data, meta)` tuple. This provides a consistent and predictable way to handle responses.

-   `data`: Contains the primary data from the API call. This is usually a `dict` for single resources (like fetching one customer) or a `list` of `dict`s for collections (like listing customers).
-   `meta`: Contains metadata about the response. For paginated results, this `dict` holds pagination details. For non-paginated results, it's an empty dictionary `{}`.

### Example: Non-Paginated Response

When you fetch a single item, `meta` is empty.

```python
# Fetching a single plan
data, meta = client.plans.fetch(id_or_code="PLN_abcdef123")

print("Plan Data:", data)
# Plan Data: {'name': 'Monthly Plan', 'plan_code': 'PLN_abcdef123', ...}

print("Metadata:", meta)
# Metadata: {}
```

### Example: Paginated Response

When you list resources, `meta` contains pagination information.

```python
# List the first 5 customers
data, meta = client.customers.list(per_page=5)

print(f"Total Customers: {meta.get('total')}")
print(f"Current Page: {meta.get('page')}")
print(f"Customers on this page: {len(data)}")

# Total Customers: 150
# Current Page: 1
# Customers on this page: 5
```

## 4. Comprehensive Error Handling

The library raises specific, custom exceptions for different types of API and client-side errors. All exceptions inherit from a base `PaystackError`, so you can catch it to handle any error from the library.

Here is the hierarchy of exceptions, found in `paystack_client.exceptions`:

-   `PaystackError` (Base class)
    -   `APIError`: A generic error returned by the Paystack API (e.g., for non-2xx status codes that don't fit other categories).
    -   `AuthenticationError`: (HTTP 401) Raised for invalid or missing API keys.
    -   `ValidationError`: (HTTP 400) Raised when request data is invalid. This can be due to missing required fields, invalid formats (like a bad email), or malformed data. The `field_errors` attribute may contain a dictionary of specific field issues.
    -   `NotFoundError`: (HTTP 404) Raised when a requested resource (like a transaction or customer) doesn't exist.
    -   `RateLimitError`: (HTTP 429) Raised when you exceed API rate limits. The `retry_after` attribute may contain the number of seconds to wait before retrying.
    -   `ServerError`: (HTTP 5xx) Raised for server-side errors on Paystack's end. These are often temporary.
    -   `NetworkError`: Raised for client-side network issues like connection timeouts or DNS failures.
    -   `InvalidResponseError`: Raised if the API returns an unexpected or malformed JSON response.
    -   `TransactionFailureError`: A special case for when a transaction fails but Paystack returns an HTTP 200 status. This happens for charge and verify requests. Check the `gateway_response` attribute for more details from the payment gateway.

### Example: Handling Different Errors

```python
from paystack_client.exceptions import (
    PaystackError,
    AuthenticationError,
    ValidationError,
    NotFoundError,
    TransactionFailureError,
    NetworkError
)

try:
    # An example call that could fail
    data, meta = client.transactions.verify(reference="an-invalid-reference")
    
    # Check for transaction failure even on HTTP 200
    if data.get('status') != 'success':
        # This case is handled by TransactionFailureError, but you can also check manually
        print(f"Transaction was not successful: {data.get('gateway_response')}")

except ValidationError as e:
    print(f"Validation Error: {e.message}")
    if e.field_errors:
        print(f"Field-specific errors: {e.field_errors}")
except AuthenticationError as e:
    print(f"Authentication Error: Please check your API key. Details: {e.message}")
except NotFoundError as e:
    print(f"Resource Not Found: {e.message}")
except TransactionFailureError as e:
    print(f"Transaction Failed: {e.message}")
    if e.gateway_response:
        print(f"Gateway Response: {e.gateway_response}")
except NetworkError as e:
    print(f"Network Error: Could not connect to Paystack. Details: {e.message}")
except PaystackError as e:
    # Catch any other Paystack-specific error
    print(f"A Paystack API error occurred: {e.message}")
    if e.status_code:
        print(f"HTTP Status: {e.status_code}")
except Exception as e:
    # Catch any other unexpected Python error
    print(f"An unexpected error occurred: {e}")
```

## 5. Pagination

For endpoints that return a list of items, you can navigate through pages using the `per_page` and `page` parameters. The `meta` object in the response provides the necessary details to build your pagination logic.

```python
from paystack_client.exceptions import APIError

# Fetch all customers, 50 at a time (Paystack's default and max is 50)
page = 1
has_more = True

while has_more:
    try:
        customers, meta = client.customers.list(per_page=50, page=page)
        
        if not customers:
            # No more customers to fetch
            break
            
        print(f"--- Page {page} ---")
        for customer in customers:
            print(f"Processing customer: {customer['customer_code']}")
            
        # Check if there are more pages
        total_customers = meta.get('total', 0)
        fetched_customers = (page * 50)
        
        if fetched_customers >= total_customers:
            has_more = False
        else:
            page += 1
            
    except APIError as e:
        print(f"Error fetching page {page}: {e.message}")
        break
```

## 6. Client-Side Validation

The library performs basic validation on some required fields before sending a request to the Paystack API. This can help catch simple errors early without making an unnecessary API call. If validation fails, a `ValidationError` is raised.

For example, the `transactions.initialize` method requires a valid email format and a numeric amount.

```python
from paystack_client.exceptions import ValidationError

# Example of invalid email
try:
    client.transactions.initialize(email="not-an-email", amount=5000)
except ValidationError as e:
    print(f"Caught expected error: {e}")
    # Caught expected error: Invalid email address provided.

# Example of invalid amount
try:
    client.transactions.initialize(email="customer@example.com", amount="five-thousand")
except ValidationError as e:
    print(f"Caught expected error: {e}")
    # Caught expected error: Amount must be a valid number.
```
