from .paystack_client.core import BaseClient
from .paystack_client.transactions import TransactionsAPI
from .paystack_client.customers import CustomersAPI
from .paystack_client.charge import ChargeAPI
from .paystack_client.plans import PlansAPI
from .paystack_client.products import ProductsAPI
from .paystack_client.refunds import RefundsAPI
from .paystack_client.settlements import SettlementsAPI
from .paystack_client.subaccounts import SubaccountsAPI
from .paystack_client.subscriptions import SubscriptionsAPI
from .paystack_client.transfers import TransfersAPI
from .paystack_client.transfers_control import TransfersControlAPI
from .paystack_client.transfers_recipients import TransferRecipientsAPI
from .paystack_client.verification import VerificationAPI
from .paystack_client.disputes import DisputesAPI
from .paystack_client.payment_pages import PaymentPagesAPI
from .paystack_client.payment_requests import PaymentRequestsAPI
from .paystack_client.bulk_charges import BulkChargesAPI
from .paystack_client.dedicated_virtual_accounts import DedicatedVirtualAccountsAPI
from .paystack_client.direct_debit import DirectDebitAPI
from .paystack_client.apple_pay import ApplePayAPI
from .paystack_client.terminal import TerminalAPI
from .paystack_client.virtual_terminal import VirtualTerminalAPI
from .paystack_client.transaction_splits import TransactionSplitsAPI
from .paystack_client.integration import IntegrationAPI
from .paystack_client.miscellaneous import MiscellaneousAPI


class PaystackClient(BaseClient):
    """
    Main Paystack client that provides access to all API endpoints.

    Usage:
        client = PaystackClient(secret_key="your_secret_key")
        transaction = client.transactions.initialize(
            email="customer@email.com",
            amount=50000  # Amount in kobo
        )
    """

    def __init__(self, secret_key: str, base_url: str = "https://api.paystack.co"):
        """
        Initialize the Paystack client.

        Args:
            secret_key (str): Your Paystack secret key
            base_url (str): API base URL (defaults to production)
        """
        super().__init__(secret_key, base_url)

        self.transactions = TransactionsAPI(secret_key, base_url)
        self.customers = CustomersAPI(secret_key, base_url)
        self.charge = ChargeAPI(secret_key, base_url)
        self.plans = PlansAPI(secret_key, base_url)
        self.products = ProductsAPI(secret_key, base_url)
        self.refunds = RefundsAPI(secret_key, base_url)
        self.settlements = SettlementsAPI(secret_key, base_url)
        self.subaccounts = SubaccountsAPI(secret_key, base_url)
        self.subscriptions = SubscriptionsAPI(secret_key, base_url)
        self.transfers = TransfersAPI(secret_key, base_url)
        self.transfers_control = TransfersControlAPI(secret_key, base_url)
        self.transfer_recipients = TransferRecipientsAPI(secret_key, base_url)
        self.verification = VerificationAPI(secret_key, base_url)
        self.disputes = DisputesAPI(secret_key, base_url)
        self.payment_pages = PaymentPagesAPI(secret_key, base_url)
        self.payment_requests = PaymentRequestsAPI(secret_key, base_url)
        self.bulk_charges = BulkChargesAPI(secret_key, base_url)
        self.dedicated_virtual_accounts = DedicatedVirtualAccountsAPI(
            secret_key, base_url
        )
        self.direct_debit = DirectDebitAPI(secret_key, base_url)
        self.apple_pay = ApplePayAPI(secret_key, base_url)
        self.terminal = TerminalAPI(secret_key, base_url)
        self.virtual_terminal = VirtualTerminalAPI(secret_key, base_url)
        self.transaction_splits = TransactionSplitsAPI(secret_key, base_url)
        self.integration = IntegrationAPI(secret_key, base_url)
        self.miscellaneous = MiscellaneousAPI(secret_key, base_url)

    def __repr__(self):
        return f"PaystackClient(base_url='{self.base_url}')"
