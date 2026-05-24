# Webhooks

Webhooks allow you to receive real-time notifications from Paystack when events occur in your account (e.g., a successful charge, a failed transfer, or a new dispute).

The `paystack-api-wrapper` library provides a dedicated `Webhook` utility to help you verify and parse these events securely.

## Overview

When Paystack sends a webhook to your server:
1.  It is a `POST` request.
2.  It contains a JSON payload.
3.  It includes a `x-paystack-signature` header for security.

## Using the Webhook Utility

The `Webhook` class simplifies signature verification and event parsing.

### 1. Verification and Parsing

You should always verify the signature to ensure the request actually came from Paystack.

```python
from paystack import Webhook, Event
from paystack.exceptions import AuthenticationError, ValidationError

# Initialize with your secret key
webhook = Webhook(secret_key="sk_test_...")

# In your web framework's request handler (e.g., Flask, Django, FastAPI)
payload = request.body  # Raw request body (bytes or string)
signature = request.headers.get("x-paystack-signature")

try:
    # This verifies the signature AND parses the payload
    event = webhook.verify_payload(payload, signature)

    print(f"Received event: {event.event}")
    
    if event.event == Event.CHARGE_SUCCESS:
        customer_email = event.data.get("customer", {}).get("email")
        amount = event.data.get("amount")
        print(f"Payment of {amount} successful from {customer_email}")

except AuthenticationError:
    # Signature verification failed - request is suspicious!
    return "Unauthorized", 401
except ValidationError as e:
    # Payload was malformed
    return str(e), 400
```

### 2. IP Whitelisting (Optional)

In addition to signature verification, you can check if the request originated from Paystack's known IP addresses.

```python
client_ip = request.remote_addr  # Get the requester's IP

if not Webhook.verify_ip(client_ip):
    return "Forbidden", 403
```

Paystack's whitelisted IPs are:
- `52.31.139.75`
- `52.49.173.169`
- `52.214.14.220`

## Supported Events

The `Event` class provides constants for common Paystack event types to avoid typos in your code.

| Constant | Event String |
| :--- | :--- |
| `Event.CHARGE_SUCCESS` | `charge.success` |
| `Event.TRANSFER_SUCCESS` | `transfer.success` |
| `Event.TRANSFER_FAILED` | `transfer.failed` |
| `Event.SUBSCRIPTION_CREATE` | `subscription.create` |
| `Event.INVOICE_UPDATE` | `invoice.update` |
| ... and many more | See `paystack.webhook.Event` |

## Best Practices

1.  **Acknowledge Quickly**: Return a `200 OK` response to Paystack immediately. If your processing logic takes a long time, handle it in a background task (e.g., Celery, RQ).
2.  **Use Raw Body**: Always use the **raw** request body for signature verification. Some frameworks parse the body into a dictionary automatically, but slight changes in formatting (like whitespace) will cause signature verification to fail.
3.  **Idempotency**: Webhooks can occasionally be sent more than once. Ensure your event handling logic is idempotent (i.e., processing the same event twice doesn't cause issues).
4.  **Security**: Never hardcode your secret key. Use environment variables.

For more details on specific event payloads, refer to the [official Paystack Webhooks documentation](https://paystack.com/docs/payments/webhooks/).
