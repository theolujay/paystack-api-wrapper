import pytest
from paystack import PaystackClient


def test_paystack_client_initialization():
    client = PaystackClient(secret_key="sk_test_abcdefghijklmnopqrstuvwxyz1234567890")
    assert client.base_url == "https://api.paystack.co/"
    assert hasattr(client, "transactions")
    assert hasattr(client, "customers")
    assert hasattr(client, "charge")
    assert hasattr(client, "plans")
    assert hasattr(client, "products")
    assert hasattr(client, "refunds")
    assert hasattr(client, "settlements")
    assert hasattr(client, "subaccounts")
    assert hasattr(client, "subscriptions")
    assert hasattr(client, "transfers")
    assert hasattr(client, "transfers_control")
    assert hasattr(client, "transfer_recipients")
    assert hasattr(client, "verification")
    assert hasattr(client, "disputes")
    assert hasattr(client, "payment_pages")
    assert hasattr(client, "payment_requests")
    assert hasattr(client, "bulk_charges")
    assert hasattr(client, "dedicated_virtual_accounts")
    assert hasattr(client, "direct_debit")
    assert hasattr(client, "apple_pay")
    assert hasattr(client, "terminal")
    assert hasattr(client, "virtual_terminal")
    assert hasattr(client, "transaction_splits")
    assert hasattr(client, "integration")
    assert hasattr(client, "miscellaneous")

    # Access the integration attribute to ensure it's covered
    assert client.integration is not None


def test_paystack_client_repr():
    client = PaystackClient(secret_key="sk_test_abcdefghijklmnopqrstuvwxyz1234567890")
    assert repr(client) == "PaystackClient(base_url='https://api.paystack.co/')"
