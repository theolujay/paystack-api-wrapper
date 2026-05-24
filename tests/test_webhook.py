import json
import hmac
import hashlib

import pytest

from paystack import (
    Webhook,
    WebhookEvent,
    Event,
    WHITELISTED_IPS,
    AuthenticationError,
    ValidationError,
)


SECRET_KEY = "sk_test_abcdefghijklmnopqrstuvwxyz1234567890"

SAMPLE_PAYLOAD = {
    "event": "charge.success",
    "data": {
        "id": 12345,
        "reference": "REF_987654",
        "amount": 50000,
        "status": "success",
        "customer": {"email": "customer@example.com"},
    },
}


def _sign(payload: dict, key: str = SECRET_KEY) -> str:
    raw = json.dumps(payload, separators=(",", ":"))
    return hmac.new(key.encode(), raw.encode(), hashlib.sha512).hexdigest()


# ── Webhook initialisation ─────────────────────────────────────────


def test_webhook_init_with_key():
    w = Webhook(secret_key=SECRET_KEY)
    assert w.secret_key == SECRET_KEY


def test_webhook_init_without_key():
    w = Webhook()
    assert w.secret_key is None


def test_webhook_repr_with_key():
    w = Webhook(secret_key=SECRET_KEY)
    assert repr(w) == "Webhook(secret_key=<set>)"


def test_webhook_repr_without_key():
    w = Webhook()
    assert repr(w) == "Webhook(secret_key=<not set>)"


# ── Signature verification ─────────────────────────────────────────


def test_verify_signature_valid():
    w = Webhook(secret_key=SECRET_KEY)
    signature = _sign(SAMPLE_PAYLOAD)
    assert w.verify_signature(SAMPLE_PAYLOAD, signature) is True


def test_verify_signature_invalid():
    w = Webhook(secret_key=SECRET_KEY)
    assert w.verify_signature(SAMPLE_PAYLOAD, "bad_signature") is False


def test_verify_signature_with_string_body():
    w = Webhook(secret_key=SECRET_KEY)
    body = json.dumps(SAMPLE_PAYLOAD, separators=(",", ":"))
    signature = _sign(SAMPLE_PAYLOAD)
    assert w.verify_signature(body, signature) is True


def test_verify_signature_with_bytes_body():
    w = Webhook(secret_key=SECRET_KEY)
    body = json.dumps(SAMPLE_PAYLOAD, separators=(",", ":")).encode()
    signature = _sign(SAMPLE_PAYLOAD)
    assert w.verify_signature(body, signature) is True


def test_verify_signature_key_from_instance():
    w = Webhook(secret_key=SECRET_KEY)
    signature = _sign(SAMPLE_PAYLOAD)
    assert w.verify_signature(SAMPLE_PAYLOAD, signature) is True


def test_verify_signature_key_from_parameter():
    w = Webhook()
    signature = _sign(SAMPLE_PAYLOAD)
    assert (
        w.verify_signature(SAMPLE_PAYLOAD, signature, secret_key=SECRET_KEY)
        is True
    )


def test_verify_signature_missing_key():
    w = Webhook()
    with pytest.raises(AuthenticationError, match="Secret key is required"):
        w.verify_signature(SAMPLE_PAYLOAD, "sig")


def test_verify_signature_raises_on_missing_key_with_secret_key_in_param():
    """No error -> the secret_key kwarg shadows the missing instance key."""
    w = Webhook()
    signature = _sign(SAMPLE_PAYLOAD)
    assert (
        w.verify_signature(SAMPLE_PAYLOAD, signature, secret_key=SECRET_KEY)
        is True
    )


# ── IP whitelist ───────────────────────────────────────────────────


def test_verify_ip_whitelisted():
    for ip in WHITELISTED_IPS:
        assert Webhook.verify_ip(ip) is True


def test_verify_ip_not_whitelisted():
    assert Webhook.verify_ip("203.0.113.1") is False


def test_verify_ip_empty_string():
    assert Webhook.verify_ip("") is False


def test_whitelisted_ips_contents():
    assert WHITELISTED_IPS == [
        "52.31.139.75",
        "52.49.173.169",
        "52.214.14.220",
    ]


# ── Event parsing ──────────────────────────────────────────────────


def test_parse_event_from_dict():
    w = Webhook()
    event = w.parse_event(SAMPLE_PAYLOAD)
    assert isinstance(event, WebhookEvent)
    assert event.event == "charge.success"
    assert event.data["reference"] == "REF_987654"
    assert event.raw_payload == SAMPLE_PAYLOAD


def test_parse_event_from_json_string():
    w = Webhook()
    body = json.dumps(SAMPLE_PAYLOAD)
    event = w.parse_event(body)
    assert event.event == "charge.success"
    assert event.data["id"] == 12345


def test_parse_event_from_bytes():
    w = Webhook()
    body = json.dumps(SAMPLE_PAYLOAD).encode()
    event = w.parse_event(body)
    assert event.event == "charge.success"


def test_parse_event_missing_event_field():
    w = Webhook()
    with pytest.raises(
        ValidationError, match="missing 'event' field"
    ):
        w.parse_event({"data": {"key": "val"}})


def test_parse_event_missing_data_field():
    w = Webhook()
    with pytest.raises(
        ValidationError, match="missing 'data' field"
    ):
        w.parse_event({"event": "charge.success"})


def test_parse_event_invalid_json():
    w = Webhook()
    with pytest.raises(ValidationError, match="Invalid webhook"):
        w.parse_event("not-json")


def test_parse_event_non_dict():
    w = Webhook()
    with pytest.raises(
        ValidationError, match="must be a JSON object"
    ):
        w.parse_event(["a", "b"])


def test_parse_event_empty_event_field():
    w = Webhook()
    with pytest.raises(
        ValidationError, match="missing 'event' field"
    ):
        w.parse_event({"event": "", "data": {}})


# ── Combined verify_payload ────────────────────────────────────────


def test_verify_payload_valid():
    w = Webhook(secret_key=SECRET_KEY)
    signature = _sign(SAMPLE_PAYLOAD)
    event = w.verify_payload(
        SAMPLE_PAYLOAD, signature=signature
    )
    assert event.event == "charge.success"


def test_verify_payload_invalid_signature():
    w = Webhook(secret_key=SECRET_KEY)
    with pytest.raises(
        AuthenticationError, match="Invalid webhook signature"
    ):
        w.verify_payload(SAMPLE_PAYLOAD, signature="bad_sig")


def test_verify_payload_without_signature_skips_verification():
    """Passing signature=None should skip verification and just parse."""
    w = Webhook()
    event = w.verify_payload(SAMPLE_PAYLOAD, signature=None)
    assert event.event == "charge.success"


def test_verify_payload_missing_key():
    w = Webhook()
    signature = _sign(SAMPLE_PAYLOAD)
    with pytest.raises(AuthenticationError, match="Secret key is required"):
        w.verify_payload(SAMPLE_PAYLOAD, signature=signature)


def test_verify_payload_key_from_parameter():
    w = Webhook()
    signature = _sign(SAMPLE_PAYLOAD)
    event = w.verify_payload(
        SAMPLE_PAYLOAD, signature=signature, secret_key=SECRET_KEY
    )
    assert event.event == "charge.success"


def test_verify_payload_malformed_body_skipping_signature():
    w = Webhook()
    with pytest.raises(ValidationError, match="Invalid webhook"):
        w.verify_payload("not-json", signature=None)


# ── Event constants ────────────────────────────────────────────────


class TestEventConstants:
    def test_charge_success(self):
        assert Event.CHARGE_SUCCESS == "charge.success"

    def test_transfer_success(self):
        assert Event.TRANSFER_SUCCESS == "transfer.success"

    def test_transfer_failed(self):
        assert Event.TRANSFER_FAILED == "transfer.failed"

    def test_transfer_reversed(self):
        assert Event.TRANSFER_REVERSED == "transfer.reversed"

    def test_subscription_create(self):
        assert Event.SUBSCRIPTION_CREATE == "subscription.create"

    def test_subscription_disable(self):
        assert Event.SUBSCRIPTION_DISABLE == "subscription.disable"

    def test_all_events_are_strings(self):
        attrs = [
            v
            for k, v in Event.__dict__.items()
            if not k.startswith("_")
        ]
        assert all(isinstance(a, str) for a in attrs)
        assert len(attrs) > 20


# ── WebhookEvent dataclass ─────────────────────────────────────────


def test_webhook_event_repr():
    event = WebhookEvent(
        event="charge.success",
        data={"id": 1},
        raw_payload={"event": "charge.success", "data": {"id": 1}},
    )
    assert "charge.success" in repr(event)


def test_webhook_event_event_type_property():
    event = WebhookEvent(
        event="transfer.success",
        data={"amount": 5000},
        raw_payload={},
    )
    # event_type is an alias for event
    assert event.event_type == "transfer.success"
    assert event.event_type == event.event
