import pytest
import os

from paystack_client.core import BaseClient
from paystack_client.client import PaystackClient
from paystack_client.endpoints import *



@pytest.fixture(scope="module")
def secret_key(request):
    """Fixture to provide a dummy secret key for tests and set it as an environment variable."""
    key = "sk_test_abcdefghijklmnopqrstuvwxyz1234567890"
    os.environ["PAYSTACK_SECRET_KEY"] = key

    def teardown():
        del os.environ["PAYSTACK_SECRET_KEY"]

    request.addfinalizer(teardown)
    return key

@pytest.fixture
def client(secret_key):
    return PaystackClient(secret_key=secret_key)




@pytest.fixture
def base_client(secret_key):
    return BaseClient(secret_key=secret_key)


@pytest.fixture
def transaction_client(client):
    return client.transactions


@pytest.fixture
def apple_pay_client(client):
    return client.apple_pay

@pytest.fixture
def bulk_charges_client(client):
    return client.bulk_charges

@pytest.fixture
def charge_client(client):
    return client.charge

@pytest.fixture
def customers_client(client):
    return client.customers

@pytest.fixture
def dedicated_virtual_accounts_client(client):
    return client.dedicated_virtual_accounts

@pytest.fixture
def direct_debit_client(client):
    return client.direct_debit

@pytest.fixture
def disputes_client(client):
    return client.disputes

@pytest.fixture
def integration_client(client):
    return client.integration

@pytest.fixture
def miscellaneous_client(client):
    return client.miscellaneous

@pytest.fixture
def payment_pages_client(client):
    return client.payment_pages

@pytest.fixture
def payment_requests_client(client):
    return client.payment_requests

@pytest.fixture
def plans_client(client):
    return client.plans 

@pytest.fixture
def products_client(client):
    return client.products

@pytest.fixture
def refunds_client(client):
    return client.refunds

@pytest.fixture
def settlements_client(client):
    return client.settlements

@pytest.fixture
def subaccounts_client(client):
    return client.subaccounts

@pytest.fixture
def subscriptions_client(client):
    return client.subscriptions

@pytest.fixture
def terminal_client(client):
    return client.terminal

@pytest.fixture
def transaction_splits_client(client):
    return client.transaction_splits

@pytest.fixture
def transfers_control_client(client):
    return client.transfers_control

@pytest.fixture
def transfer_recipients_client(client):
    return client.transfer_recipients

@pytest.fixture
def transfers_client(client):
    return client.transfers

@pytest.fixture
def verification_client(client):
    return client.verification

@pytest.fixture
def virtual_terminal_client(client):
    return client.virtual_terminal