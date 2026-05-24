# API Reference

This document lists all the API resources available on the `PaystackClient` and their corresponding endpoints. Each resource follows the Paystack API structure.

## Client Initialization

```python
from paystack import PaystackClient

client = PaystackClient(secret_key="sk_test_...")
```

---

## Available Resources

The following resources are available as properties on the `client` object:

### Transactions
`client.transactions`
- `initialize(...)`: Initialize a transaction.
- `verify(reference)`: Verify a transaction.
- `list(...)`: List transactions.
- `fetch(id_or_code)`: Get details of a transaction.
- `charge_authorization(...)`: Charge a saved card.
- `timeline(id_or_code)`: View transaction timeline.
- `totals(...)`: Get transaction totals.
- `export(...)`: Export transactions.
- `partial_debit(...)`: Partially debit a customer.

### Customers
`client.customers`
- `create(...)`: Create a customer.
- `list(...)`: List customers.
- `fetch(email_or_code)`: Get customer details.
- `update(code, ...)`: Update a customer.
- `validate(code, ...)`: Validate a customer's identity.
- `whitelist(code, ...)`: Whitelist or blacklist a customer.
- `deactivate_authorization(authorization_code)`: Deactivate a customer's card authorization.

### Plans & Subscriptions
`client.plans`
- `create(...)`, `list()`, `fetch(id_or_code)`, `update(id_or_code, ...)`

`client.subscriptions`
- `create(...)`, `list()`, `fetch(id_or_code)`, `enable(code, token)`, `disable(code, token)`, `generate_link(code)`

### Transfers
`client.transfers`
- `initiate(...)`, `finalize(transfer_code, otp)`, `list()`, `fetch(id_or_code)`, `verify(reference)`

`client.transfer_recipients`
- `create(...)`, `bulk_create(batch)`, `list()`, `fetch(id_or_code)`, `update(id_or_code, ...)`, `delete(id_or_code)`

`client.transfers_control`
- `check_balance()`, `fetch_balance_ledger()`, `resend_otp(transfer_code, reason)`, `disable_otp()`, `finalize_disable_otp(otp)`, `enable_otp()`

### Payment Tools
`client.payment_pages`
- `create(...)`, `list()`, `fetch(id_or_code)`, `update(id_or_code, ...)`, `check_slug_availability(slug)`, `add_products(id, products)`

`client.payment_requests`
- `create(...)`, `list()`, `fetch(id_or_code)`, `update(id_or_code, ...)`, `verify(code)`, `send_notification(code)`, `totals()`, `finalize(code)`, `archive(code)`

`client.products`
- `create(...)`, `list()`, `fetch(id_or_code)`, `update(id_or_code, ...)`

### Specialized APIs
- `client.apple_pay`: Register domains for Apple Pay.
- `client.bulk_charges`: Initiate and manage bulk charges.
- `client.charge`: Create direct charges via various channels (Mobile Money, Bank, etc.).
- `client.dedicated_virtual_accounts`: Manage dedicated virtual accounts for customers.
- `client.disputes`: Manage transaction disputes.
- `client.refunds`: Initiate and manage refunds.
- `client.settlements`: Fetch settlement records.
- `client.subaccounts`: Manage subaccounts for split payments.
- `client.terminal`: Manage Paystack Terminal devices.
- `client.verification`: Verify BVN, Bank Account, and Card BIN.
- `client.virtual_terminal`: Manage Virtual Terminals.
- `client.transaction_splits`: Manage transaction split configurations.
- `client.integration`: Manage integration settings (e.g., timeout).
- `client.miscellaneous`: Fetch supported banks, countries, states, etc.

---

## Common Method Signatures

Most `list()` methods support:
- `per_page` (int): Number of results per page (max 50).
- `page` (int): Page number to retrieve.
- `from_date` (str): ISO 8601 timestamp.
- `to_date` (str): ISO 8601 timestamp.

Most `fetch()`, `update()`, and `delete()` methods take an `id_or_code` as the first argument.

For detailed arguments for each method, please refer to the [Paystack API Documentation](https://paystack.com/docs/api/).
