import pytest
import os
from dotenv import load_dotenv

from paystack_client.core import BaseClient
from paystack_client.exceptions import AuthenticationError
from paystack_client.transactions import TransactionsAPI
from paystack_client.apple_pay import ApplePayAPI
from paystack_client.bulk_charges import BulkChargesAPI
from paystack_client.charge import ChargeAPI
from paystack_client.customers import CustomersAPI
from paystack_client.dedicated_virtual_accounts import DedicatedVirtualAccountsAPI
from paystack_client.direct_debit import DirectDebitAPI
from paystack_client.disputes import DisputesAPI
from paystack_client.integration import IntegrationAPI
from paystack_client.miscellaneous import MiscellaneousAPI
from paystack_client.payment_pages import PaymentPagesAPI
from paystack_client.payment_requests import PaymentRequestsAPI
from paystack_client.plans import PlansAPI
from paystack_client.products import ProductsAPI
from paystack_client.refunds import RefundsAPI
from paystack_client.settlements import SettlementsAPI
from paystack_client.subaccounts import SubaccountsAPI
from paystack_client.subscriptions import SubscriptionsAPI
from paystack_client.terminal import TerminalAPI
from paystack_client.transaction_splits import TransactionSplitsAPI
from paystack_client.transfers_control import TransfersControlAPI
from paystack_client.transfers_recipients import TransferRecipientsAPI
from paystack_client.transfers import TransfersAPI
from paystack_client.verification import VerificationAPI
from paystack_client.virtual_terminal import VirtualTerminalAPI


@pytest.fixture(autouse=True)
def load_test_env():
    """Automatically load test environment for all tests"""
    load_dotenv(".env.test")


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
def base_client(secret_key):
    return BaseClient(secret_key=secret_key)

@pytest.fixture
def transaction_client(secret_key):
    return TransactionsAPI(secret_key=secret_key)

@pytest.fixture
def apple_pay_client(secret_key):
    return ApplePayAPI(secret_key=secret_key)

@pytest.fixture
def bulk_charges_client(secret_key):
    return BulkChargesAPI(secret_key=secret_key)

@pytest.fixture
def charge_client(secret_key):
    return ChargeAPI(secret_key=secret_key)

@pytest.fixture
def customers_client(secret_key):
    return CustomersAPI(secret_key=secret_key)

@pytest.fixture
def dedicated_virtual_accounts_client(secret_key):
    return DedicatedVirtualAccountsAPI(secret_key=secret_key)

@pytest.fixture
def direct_debit_client(secret_key):
    return DirectDebitAPI(secret_key=secret_key)

@pytest.fixture
def disputes_client(secret_key):
    return DisputesAPI(secret_key=secret_key)

@pytest.fixture
def integration_client(secret_key):
    return IntegrationAPI(secret_key=secret_key)

@pytest.fixture
def miscellaneous_client(secret_key):
    return MiscellaneousAPI(secret_key=secret_key)

@pytest.fixture
def payment_pages_client(secret_key):
    return PaymentPagesAPI(secret_key=secret_key)

@pytest.fixture
def payment_requests_client(secret_key):
    return PaymentRequestsAPI(secret_key=secret_key)

@pytest.fixture
def plans_client(secret_key):
    return PlansAPI(secret_key=secret_key)

@pytest.fixture
def products_client(secret_key):
    return ProductsAPI(secret_key=secret_key)

@pytest.fixture
def refunds_client(secret_key):
    return RefundsAPI(secret_key=secret_key)

@pytest.fixture
def settlements_client(secret_key):
    return SettlementsAPI(secret_key=secret_key)

@pytest.fixture
def subaccounts_client(secret_key):
    return SubaccountsAPI(secret_key=secret_key)

@pytest.fixture
def subscriptions_client(secret_key):
    return SubscriptionsAPI(secret_key=secret_key)

@pytest.fixture
def terminal_client(secret_key):
    return TerminalAPI(secret_key=secret_key)

@pytest.fixture
def transaction_splits_client(secret_key):
    return TransactionSplitsAPI(secret_key=secret_key)

@pytest.fixture
def transfers_control_client(secret_key):
    return TransfersControlAPI(secret_key=secret_key)

@pytest.fixture
def transfer_recipients_client(secret_key):
    return TransferRecipientsAPI(secret_key=secret_key)

@pytest.fixture
def transfers_client(secret_key):
    return TransfersAPI(secret_key=secret_key)

@pytest.fixture
def verification_client(secret_key):
    return VerificationAPI(secret_key=secret_key)

@pytest.fixture
def virtual_terminal_client(secret_key):
    return VirtualTerminalAPI(secret_key=secret_key)