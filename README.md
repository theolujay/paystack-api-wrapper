# Paystack Python Client

[![PyPI Version](https://img.shields.io/pypi/v/paystack-api-wrapper.svg)](https://pypi.org/project/paystack-api-wrapper/)
[![Python Versions](https://img.shields.io/pypi/pyversions/paystack-api-wrapper.svg)](https://pypi.org/project/paystack-api-wrapper/)
[![License](https://img.shields.io/github/license/theolujay/paystack.svg)](https://github.com/theolujay/paystack/blob/main/LICENSE)
[![Build](https://github.com/theolujay/paystack/actions/workflows/tests.yml/badge.svg)](https://github.com/theolujay/paystack/actions) 
[![Coverage](https://codecov.io/gh/theolujay/paystack/branch/main/graph/badge.svg)](https://codecov.io/gh/theolujay/paystack)

A clean, intuitive, and reliable Python wrapper for the Paystack API.

This library was built to **eliminate repetitive boilerplate** when integrating Paystack into your Python projects, while emphasizing **modern design, robust error handling, and a test-driven foundation**. Covers the full API with clean abstractions, so you can focus on building features—not handling payments.

See the [Paystack API docs](https://paystack.com/docs/api/) for reference, and explore the [Usage Guide](./docs/USAGE.md) for practical examples.

---

## Installation

```bash
pip install paystack-api-wrapper
```

---

## Quick Start

1. **Initialize the client with your secret key**

   (Best practice: store your secret key as an environment variable `PAYSTACK_SECRET_KEY`.)

   ```python
   import os
   from paystack import PaystackClient, APIError

   secret_key = os.getenv("PAYSTACK_SECRET_KEY")
   client = PaystackClient(secret_key=secret_key)
   ```

2. **Make an API call** (e.g., initialize a transaction):

   ```python
   try:
       data, meta = client.transactions.initialize(
           email="customer@example.com",
           amount=50000,  # amount in kobo
           currency="NGN"
       )
       print("Transaction initialized:", data)
       # {'authorization_url': '...', 'access_code': '...', 'reference': '...'}

   except APIError as e:
       print(f"API error: {e.message}")
   ```

See the [**Full Usage Guide**](./docs/USAGE.md) for details on handling responses, pagination, and advanced error management.

---

## Available APIs

The client exposes all major Paystack API resources as properties:

* `apple_pay`
* `bulk_charges`
* `charge`
* `customers`
* `dedicated_virtual_accounts`
* `direct_debit`
* `disputes`
* `integration`
* `miscellaneous`
* `payment_pages`
* `payment_requests`
* `plans`
* `products`
* `refunds`
* `settlements`
* `subaccounts`
* `subscriptions`
* `terminal`
* `transactions`
* `transaction_splits`
* `transfers`
* `transfers_control`
* `transfer_recipients`
* `verification`
* `virtual_terminal`

---

## Contributing

Contributions are welcome! Check out the [contributing guide](./CONTRIBUTING.md) to get started.

---

## License

MIT © [Joseph Ezekiel](https://github.com/theolujay) – see [LICENSE](./LICENSE) for details.