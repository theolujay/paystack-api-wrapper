"""
The Payment Pages API provides a quick and secure way to collect payment for products.
"""

from typing import Optional, List, Dict, Any, Tuple

from .core import BaseClient


class PaymentPagesAPI(BaseClient):
    """
    The Payment Pages API provides a quick and secure way to collect payment for products.
    """

    def __init__(self, secret_key: Optional[str] = None):
        super().__init__(secret_key)

    def create_payment_page(
        self,
        name: str,
        description: Optional[str] = None,
        amount: Optional[int] = None,
        currency: Optional[str] = None,
        slug: Optional[str] = None,
        type: Optional[str] = None,
        plan: Optional[str] = None,
        fixed_amount: Optional[bool] = None,
        split_code: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        redirect_url: Optional[str] = None,
        success_message: Optional[str] = None,
        notification_email: Optional[str] = None,
        collect_phone: Optional[bool] = None,
        custom_fields: Optional[List[Dict[str, Any]]] = None,
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Create a payment page on your integration

        Args:
            name: Name of page
            description: A description for this page
            amount: Amount should be in the subunit of the supported currency
            currency: The transaction currency. Defaults to your integration currency.
            slug: URL slug you would like to be associated with this page. Page will be accessible at https://paystack.com/pay/[slug]
            type: The type of payment page to create. Options are payment, subscription, product, and plan. Defaults to payment if no type is specified.
            plan: The ID of the plan to subscribe customers on this payment page to when type is set to subscription.
            fixed_amount: Specifies whether to collect a fixed amount on the payment page. If true, amount must be passed.
            split_code: The split code of the transaction split. e.g. SPL_98WF13Eb3w
            metadata: Extra data to configure the payment page including subaccount, logo image, transaction charge
            redirect_url: If you would like Paystack to redirect someplace upon successful payment, specify the URL here.
            success_message: A success message to display to the customer after a successful transaction
            notification_email: An email address that will receive transaction notifications for this payment page
            collect_phone: Specify whether to collect phone numbers on the payment page
            custom_fields: If you would like to accept custom fields, specify them here.

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        payload = {"name": name}
        if description:
            payload["description"] = description
        if amount:
            payload["amount"] = amount
        if currency:
            payload["currency"] = currency
        if slug:
            payload["slug"] = slug
        if type:
            payload["type"] = type
        if plan:
            payload["plan"] = plan
        if fixed_amount is not None:
            payload["fixed_amount"] = fixed_amount
        if split_code:
            payload["split_code"] = split_code
        if metadata:
            payload["metadata"] = metadata
        if redirect_url:
            payload["redirect_url"] = redirect_url
        if success_message:
            payload["success_message"] = success_message
        if notification_email:
            payload["notification_email"] = notification_email
        if collect_phone is not None:
            payload["collect_phone"] = collect_phone
        if custom_fields:
            payload["custom_fields"] = custom_fields

        return self.request("POST", "page", json_data=payload)

    def list_payment_pages(
        self,
        per_page: Optional[int] = None,
        page: Optional[int] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        List payment pages available on your integration

        Args:
            per_page: Specify how many records you want to retrieve per page. If not specify we use a default value of 50.
            page: Specify exactly what page you want to retrieve. If not specify we use a default value of 1.
            from_date: A timestamp from which to start listing page e.g. 2016-09-24T00:00:05.000Z, 2016-09-21
            to_date: A timestamp at which to stop listing page e.g. 2016-09-24T00:00:05.000Z, 2016-09-21

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        params = {}
        if per_page:
            params["perPage"] = per_page
        if page:
            params["page"] = page
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date

        return self.request("GET", "page", params=params)

    def fetch_payment_page(
        self, id_or_slug: str
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Get details of a payment page on your integration

        Args:
            id_or_slug: The page ID or slug you want to fetch

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        return self.request("GET", f"page/{id_or_slug}")

    def update_payment_page(
        self,
        id_or_slug: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        amount: Optional[int] = None,
        active: Optional[bool] = None,
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Update a payment page details on your integration

        Args:
            id_or_slug: Page ID or slug
            name: Name of page
            description: A description for this page
            amount: Default amount you want to accept using this page. If none is set, customer is free to provide any amount of their choice. The latter scenario is useful for accepting donations
            active: Set to false to deactivate page url

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        payload = {}
        if name:
            payload["name"] = name
        if description:
            payload["description"] = description
        if amount:
            payload["amount"] = amount
        if active is not None:
            payload["active"] = active

        return self.request("PUT", f"page/{id_or_slug}", json_data=payload)

    def check_slug_availability(
        self, slug: str
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Check the availability of a slug for a payment page

        Args:
            slug: URL slug to be confirmed

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        return self.request("GET", f"page/check_slug_availability/{slug}")

    def add_products(
        self, page_id: int, product_ids: List[int]
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Add products to a payment page

        Args:
            page_id: Id of the payment page
            product_ids: Ids of all the products

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        payload = {"product": product_ids}
        return self.request("POST", f"page/{page_id}/product", json_data=payload)
