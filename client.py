from .api.core import BaseClient
from .api.transactions import TransactionsAPI
from .api.customers import CustomersAPI
from .api.charge import ChargeAPI
from .api.plans import PlansAPI
from .api.products import ProductsAPI
from .api.refunds import RefundsAPI
from .api.settlements import SettlementsAPI
from .api.subaccounts import SubaccountsAPI
from .api.subscriptions import SubscriptionsAPI
from .api.transfers import TransfersAPI
from .api.transfers_control import TransfersControlAPI
from .api.transfers_recipients import TransferRecipientsAPI
from .api.verification import VerificationAPI
from .api.disputes import DisputesAPI
from .api.payment_pages import PaymentPagesAPI
from .api.payment_requests import PaymentRequestsAPI
from .api.bulk_charges import BulkChargesAPI
from .api.dedicated_virtual_accounts import DedicatedVirtualAccountsAPI
from .api.direct_debit import DirectDebitAPI
from .api.apple_pay import ApplePayAPI
from .api.terminal import TerminalAPI
from .api.virtual_terminal import VirtualTerminalAPI
from .api.transaction_splits import TransactionSplitsAPI
from .api.integration import IntegrationAPI
from .api.miscellaneous import MiscellaneousAPI

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
        self.dedicated_virtual_accounts = DedicatedVirtualAccountsAPI(secret_key, base_url)
        self.direct_debit = DirectDebitAPI(secret_key, base_url)
        self.apple_pay = ApplePayAPI(secret_key, base_url)
        self.terminal = TerminalAPI(secret_key, base_url)
        self.virtual_terminal = VirtualTerminalAPI(secret_key, base_url)
        self.transaction_splits = TransactionSplitsAPI(secret_key, base_url)
        self.integration = IntegrationAPI(secret_key, base_url)
        self.miscellaneous = MiscellaneousAPI(secret_key, base_url)
    
    def __repr__(self):
        return f"PaystackClient(base_url='{self.base_url}')"