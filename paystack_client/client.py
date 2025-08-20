from .core import BaseClient
from .transactions import TransactionsAPI
from .customers import CustomersAPI
from .charge import ChargeAPI
from .plans import PlansAPI
from .products import ProductsAPI
from .refunds import RefundsAPI
from .settlements import SettlementsAPI
from .subaccounts import SubaccountsAPI
from .subscriptions import SubscriptionsAPI
from .transfers import TransfersAPI
from .transfers_control import TransfersControlAPI
from .transfers_recipients import TransferRecipientsAPI
from .verification import VerificationAPI
from .disputes import DisputesAPI
from .payment_pages import PaymentPagesAPI
from .payment_requests import PaymentRequestsAPI
from .bulk_charges import BulkChargesAPI
from .dedicated_virtual_accounts import DedicatedVirtualAccountsAPI
from .direct_debit import DirectDebitAPI
from .apple_pay import ApplePayAPI
from .terminal import TerminalAPI
from .virtual_terminal import VirtualTerminalAPI
from .transaction_splits import TransactionSplitsAPI
from .integration import IntegrationAPI
from .miscellaneous import MiscellaneousAPI


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

    def __init__(self, secret_key: str):
        """
        Initialize the Paystack client.

        Args:
            secret_key (str): Your Paystack secret key
            base_url (str): API base URL (defaults to production)
        """
        super().__init__(secret_key)

        self.transactions = TransactionsAPI(secret_key)
        self.customers = CustomersAPI(secret_key)
        self.charge = ChargeAPI(secret_key)
        self.plans = PlansAPI(secret_key)
        self.products = ProductsAPI(secret_key)
        self.refunds = RefundsAPI(secret_key)
        self.settlements = SettlementsAPI(secret_key)
        self.subaccounts = SubaccountsAPI(secret_key)
        self.subscriptions = SubscriptionsAPI(secret_key)
        self.transfers = TransfersAPI(secret_key)
        self.transfers_control = TransfersControlAPI(secret_key)
        self.transfer_recipients = TransferRecipientsAPI(secret_key)
        self.verification = VerificationAPI(secret_key)
        self.disputes = DisputesAPI(secret_key)
        self.payment_pages = PaymentPagesAPI(secret_key)
        self.payment_requests = PaymentRequestsAPI(secret_key)
        self.bulk_charges = BulkChargesAPI(secret_key)
        self.dedicated_virtual_accounts = DedicatedVirtualAccountsAPI(
            secret_key
        )
        self.direct_debit = DirectDebitAPI(secret_key)
        self.apple_pay = ApplePayAPI(secret_key)
        self.terminal = TerminalAPI(secret_key)
        self.virtual_terminal = VirtualTerminalAPI(secret_key)
        self.transaction_splits = TransactionSplitsAPI(secret_key)
        self.integration = IntegrationAPI(secret_key)
        self.miscellaneous = MiscellaneousAPI(secret_key)

    def __repr__(self):
        return f"PaystackClient(base_url='{self.base_url}')"
