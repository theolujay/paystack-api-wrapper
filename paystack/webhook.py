"""
Webhook verification and event handling for Paystack.

Provides utilities for verifying the authenticity of incoming webhook
events from Paystack via HMAC-SHA512 signature validation, IP whitelist
checking, and structured event parsing.
"""

import hashlib
import hmac
import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union

from .exceptions import AuthenticationError, ValidationError

WHITELISTED_IPS: List[str] = [
    "52.31.139.75",
    "52.49.173.169",
    "52.214.14.220",
]


class Event:
    """Constants for Paystack webhook event types."""

    CHARGE_SUCCESS = "charge.success"
    CHARGE_DISPUTE_CREATE = "charge.dispute.create"
    CHARGE_DISPUTE_REMIND = "charge.dispute.remind"
    CHARGE_DISPUTE_RESOLVE = "charge.dispute.resolve"
    CUSTOMER_IDENTIFICATION_FAILED = "customeridentification.failed"
    CUSTOMER_IDENTIFICATION_SUCCESS = "customeridentification.success"
    DEDICATED_ACCOUNT_ASSIGN_FAILED = "dedicatedaccount.assign.failed"
    DEDICATED_ACCOUNT_ASSIGN_SUCCESS = "dedicatedaccount.assign.success"
    INVOICE_CREATE = "invoice.create"
    INVOICE_PAYMENT_FAILED = "invoice.payment_failed"
    INVOICE_UPDATE = "invoice.update"
    PAYMENT_REQUEST_PENDING = "paymentrequest.pending"
    PAYMENT_REQUEST_SUCCESS = "paymentrequest.success"
    REFUND_FAILED = "refund.failed"
    REFUND_PENDING = "refund.pending"
    REFUND_PROCESSED = "refund.processed"
    REFUND_PROCESSING = "refund.processing"
    SUBSCRIPTION_CREATE = "subscription.create"
    SUBSCRIPTION_DISABLE = "subscription.disable"
    SUBSCRIPTION_EXPIRING_CARDS = "subscription.expiring_cards"
    SUBSCRIPTION_NOT_RENEW = "subscription.not_renew"
    TRANSFER_FAILED = "transfer.failed"
    TRANSFER_SUCCESS = "transfer.success"
    TRANSFER_REVERSED = "transfer.reversed"


@dataclass
class WebhookEvent:
    """A validated and parsed webhook event from Paystack.

    Attributes:
        event: The event type string (e.g. ``"charge.success"``).
        data: The event-specific payload data.
        raw_payload: The full decoded JSON payload for reference.
    """

    event: str
    data: Dict[str, Any]
    raw_payload: Dict[str, Any] = field(repr=False)

    @property
    def event_type(self) -> str:
        """Alias for the ``event`` field."""
        return self.event


class Webhook:
    """Verifies and parses incoming Paystack webhook events.

    Use this to validate the authenticity of webhook payloads before
    processing them. Supports both HMAC-SHA512 signature verification
    and optional IP whitelist checking.

    Usage::

        webhook = Webhook(secret_key="sk_test_...")

        # In your webhook view handler:
        event = webhook.verify_payload(
            payload=request.body,
            signature=request.headers.get("x-paystack-signature"),
        )

        if event.event == Event.CHARGE_SUCCESS:
            handle_payment(event.data)
    """

    def __init__(self, secret_key: Optional[str] = None):
        self.secret_key = secret_key

    def verify_signature(
        self,
        payload: Union[str, bytes, Dict[str, Any]],
        signature: str,
        secret_key: Optional[str] = None,
    ) -> bool:
        """Verify an HMAC-SHA512 signature against a webhook payload.

        Args:
            payload: Raw request body (string, bytes, or decoded dict).
            signature: The value of the ``x-paystack-signature`` header.
            secret_key: Paystack secret key. Falls back to the key
                provided at initialisation if omitted.

        Returns:
            ``True`` if the signature is valid, ``False`` otherwise.

        Raises:
            AuthenticationError: If no secret key is available.
        """
        key = secret_key or self.secret_key
        if not key:
            raise AuthenticationError(
                "Secret key is required for signature verification"
            )

        if isinstance(payload, dict):
            payload = json.dumps(payload, separators=(",", ":"))
        if isinstance(payload, str):
            payload = payload.encode("utf-8")

        expected = hmac.new(key.encode("utf-8"), payload, hashlib.sha512).hexdigest()

        return hmac.compare_digest(expected, signature)

    @staticmethod
    def verify_ip(ip_address: str) -> bool:
        """Check whether an IP address is in Paystack's whitelist.

        Paystack only sends webhooks from a small set of known IPs.
        Requests from any other IP should be rejected.

        Args:
            ip_address: The remote IP address to check.

        Returns:
            ``True`` if the IP is whitelisted, ``False`` otherwise.
        """
        return ip_address in WHITELISTED_IPS

    @staticmethod
    def parse_event(
        payload: Union[str, bytes, Dict[str, Any]],
    ) -> WebhookEvent:
        """Parse a raw webhook payload into a structured ``WebhookEvent``.

        Performs basic structural validation but does **not** verify
        the payload's signature. Use :meth:`verify_payload` for a
        combined verification + parse flow.

        Args:
            payload: Raw request body (string, bytes, or decoded dict).

        Returns:
            A :class:`WebhookEvent` with the parsed event data.

        Raises:
            ValidationError: If the payload is malformed or missing
                required fields.
        """
        if isinstance(payload, (str, bytes)):
            try:
                data = json.loads(payload)
            except json.JSONDecodeError as e:
                raise ValidationError(
                    message=f"Invalid webhook payload JSON: {e}",
                )
        else:
            data = payload

        if not isinstance(data, dict):
            raise ValidationError(
                message="Webhook payload must be a JSON object",
            )

        event = data.get("event")
        event_data = data.get("data")

        if not event:
            raise ValidationError(
                message="Webhook payload missing 'event' field",
            )

        if event_data is None:
            raise ValidationError(
                message="Webhook payload missing 'data' field",
            )

        return WebhookEvent(event=event, data=event_data, raw_payload=data)

    def verify_payload(
        self,
        payload: Union[str, bytes, Dict[str, Any]],
        signature: Optional[str] = None,
        secret_key: Optional[str] = None,
    ) -> WebhookEvent:
        """Verify the webhook signature and parse the event payload.

        This is the main entry point for processing incoming webhooks.
        It validates the HMAC-SHA512 signature (if provided) and
        returns a structured :class:`WebhookEvent`.

        Args:
            payload: Raw request body (string, bytes, or decoded dict).
            signature: The value of the ``x-paystack-signature`` header.
                Pass ``None`` to skip signature verification (not
                recommended in production).
            secret_key: Paystack secret key. Falls back to the key
                provided at initialisation if omitted.

        Returns:
            A :class:`WebhookEvent` representing the verified event.

        Raises:
            AuthenticationError: If the signature is invalid or no
                secret key is configured.
            ValidationError: If the payload is malformed.
        """
        if signature is not None:
            if not self.verify_signature(payload, signature, secret_key):
                raise AuthenticationError(
                    message="Invalid webhook signature — payload may not "
                    "originate from Paystack",
                )

        return self.parse_event(payload)

    def __repr__(self) -> str:
        key_label = "<set>" if self.secret_key else "<not set>"
        return f"Webhook(secret_key={key_label})"
