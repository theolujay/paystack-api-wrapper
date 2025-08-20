from .core import BaseClient
from .endpoints import *


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

    def __init__(self, secret_key: str, base_url: str = "https://api.paystack.co/"):
        """
        Initialize the Paystack client.

        Args:
            secret_key (str): Your Paystack secret key
            base_url (str): API base URL (defaults to production)
        """
        super().__init__(secret_key, base_url=base_url)

        self.transactions = TransactionsAPI(
            secret_key, session=self.session, base_url=self.base_url
        )
        self.customers = CustomersAPI(
            secret_key, session=self.session, base_url=self.base_url
        )
        self.charge = ChargeAPI(
            secret_key, session=self.session, base_url=self.base_url
        )
        self.plans = PlansAPI(secret_key, session=self.session, base_url=self.base_url)
        self.products = ProductsAPI(
            secret_key, session=self.session, base_url=self.base_url
        )
        self.refunds = RefundsAPI(
            secret_key, session=self.session, base_url=self.base_url
        )
        self.settlements = SettlementsAPI(
            secret_key, session=self.session, base_url=self.base_url
        )
        self.subaccounts = SubaccountsAPI(
            secret_key, session=self.session, base_url=self.base_url
        )
        self.subscriptions = SubscriptionsAPI(
            secret_key, session=self.session, base_url=self.base_url
        )
        self.transfers = TransfersAPI(
            secret_key, session=self.session, base_url=self.base_url
        )
        self.transfers_control = TransfersControlAPI(
            secret_key, session=self.session, base_url=self.base_url
        )
        self.transfer_recipients = TransferRecipientsAPI(
            secret_key, session=self.session, base_url=self.base_url
        )
        self.verification = VerificationAPI(
            secret_key, session=self.session, base_url=self.base_url
        )
        self.disputes = DisputesAPI(
            secret_key, session=self.session, base_url=self.base_url
        )
        self.payment_pages = PaymentPagesAPI(
            secret_key, session=self.session, base_url=self.base_url
        )
        self.payment_requests = PaymentRequestsAPI(
            secret_key, session=self.session, base_url=self.base_url
        )
        self.bulk_charges = BulkChargesAPI(
            secret_key, session=self.session, base_url=self.base_url
        )
        self.dedicated_virtual_accounts = DedicatedVirtualAccountsAPI(
            secret_key, session=self.session, base_url=self.base_url
        )
        self.direct_debit = DirectDebitAPI(
            secret_key, session=self.session, base_url=self.base_url
        )
        self.apple_pay = ApplePayAPI(
            secret_key, session=self.session, base_url=self.base_url
        )
        self.terminal = TerminalAPI(
            secret_key, session=self.session, base_url=self.base_url
        )
        self.virtual_terminal = VirtualTerminalAPI(
            secret_key, session=self.session, base_url=self.base_url
        )
        self.transaction_splits = TransactionSplitsAPI(
            secret_key, session=self.session, base_url=self.base_url
        )
        self.integration = IntegrationAPI(
            secret_key, session=self.session, base_url=self.base_url
        )
        self.miscellaneous = MiscellaneousAPI(
            secret_key, session=self.session, base_url=self.base_url
        )

    def __repr__(self):
        return f"PaystackClient(base_url='{self.base_url}')"
