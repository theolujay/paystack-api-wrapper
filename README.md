# Paystack Python Client

[![PyPI Version](https://img.shields.io/pypi/v/paystack-client.svg)](https://pypi.org/project/paystack-client/)
[![Python Versions](https://img.shields.io/pypi/pyversions/paystack-client)](https://pypi.org/project/paystack-client/)
[![License](https://img.shields.io/pypi/l/paystack-client)](./LICENSE)
[![Build Status](https://img.shields.io/github/actions/workflow/status/theolujay/paystack_client/ci.yml?branch=main)](https://github.com/theolujay/paystack_client/actions)
[![Coverage Status](https://img.shields.io/codecov/c/github/theolujay/paystack_client)](https://codecov.io/gh/theolujay/paystack_client)

**A clean, intuitive, and reliable Python wrapper for the Paystack API.**

This client covers **all Paystack endpoints** as-is, making integration into your Python apps straightforward. It’s built with a focus on **clarity, consistency, and robust error handling**—so you spend less time fighting boilerplate and more time shipping.

📖 See the [Paystack API docs](https://paystack.com/docs/api/) for reference, and explore the [Usage Guide](./docs/USAGE.md) for practical examples.

---

## Installation

```bash
pip install paystack-client
```

---

## Quick Start

1. **Initialize the client with your secret key**

   (Best practice: store your secret key as an environment variable `PAYSTACK_SECRET_KEY`.)

   ```python
   import os
   from paystack_client import PaystackClient, APIError

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

## 📄 License

MIT © [Joseph Ezekiel](https://github.com/theolujay) – see [LICENSE](./LICENSE) for details.
