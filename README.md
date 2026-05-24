# Paystack API Wrapper

[![PyPI Version](https://img.shields.io/pypi/v/paystack-api-wrapper.svg)](https://pypi.org/project/paystack-api-wrapper/) [![Python Versions](https://img.shields.io/pypi/pyversions/paystack-api-wrapper.svg)](https://pypi.org/project/paystack-api-wrapper/) [![Build](https://github.com/theolujay/paystack-api-wrapper/actions/workflows/tests.yml/badge.svg)](https://github.com/theolujay/paystack-api-wrapper/actions) [![Coverage](https://codecov.io/gh/theolujay/paystack-api-wrapper/branch/main/graph/badge.svg)](https://codecov.io/gh/theolujay/paystack-api-wrapper) [![License](https://img.shields.io/github/license/theolujay/paystack-api-wrapper.svg)](https://github.com/theolujay/paystack-api-wrapper/blob/main/LICENSE)

A clean, modern, and test-driven Python client for the [Paystack API](https://paystack.com/docs/api/).

Built to eliminate boilerplate, this library provides a high-level, type-safe interface for integrating payments into your Python applications with confidence.

## Features

- **Full API Coverage**: Supports all Paystack endpoints from transactions to terminals.
- **Predictable Responses**: Every call returns a structured `(data, meta)` tuple.
- **Robust Error Handling**: Specific exceptions for validation, authentication, and network errors.
- **Type-Safe**: Fully typed with type hints for a better developer experience.
- **Secure Webhooks**: Built-in utilities for signature verification and IP whitelisting.

---

## Installation

```bash
pip install paystack-api-wrapper
```

---

## Quick Start

```python
import os
from paystack import PaystackClient, APIError

# Initialize client
client = PaystackClient(secret_key=os.getenv("PAYSTACK_SECRET_KEY"))

try:
    # Initialize a transaction
    data, meta = client.transactions.initialize(
        email="customer@example.com",
        amount=50000,  # in kobo
    )
    print(f"Checkout URL: {data['authorization_url']}")

except APIError as e:
    print(f"Paystack error: {e.message}")
```

---

## Documentation

- [**Full Usage Guide**](./docs/USAGE.md) - Deep dive into initialization, pagination, and error handling.
- [**API Reference**](./docs/API_REFERENCE.md) - Complete list of available resources and methods.
- [**Webhooks Guide**](./docs/WEBHOOKS.md) - Securely handling real-time notifications.

---

## Supported APIs

The client exposes all Paystack resources as intuitive properties:

`apple_pay`, `bulk_charges`, `charge`, `customers`, `dedicated_virtual_accounts`, `direct_debit`, `disputes`, `integration`, `miscellaneous`, `payment_pages`, `payment_requests`, `plans`, `products`, `refunds`, `settlements`, `subaccounts`, `subscriptions`, `terminal`, `transactions`, `transaction_splits`, `transfers`, `transfers_control`, `transfer_recipients`, `verification`, `virtual_terminal`.

---

## Contributing

Contributions are welcome! Please see the [Contributing Guide](./CONTRIBUTING.md) to get started.

---

## License

MIT © [Joseph Ezekiel](https://github.com/theolujay) – see [LICENSE](./LICENSE) for details.