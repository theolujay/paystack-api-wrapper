"""
The Products API allows you create and manage inventories on your integration.
"""
from typing import Optional

from .core import BaseClient, PaystackResponse


class ProductsAPI(BaseClient):
    """
    The Products API allows you create and manage inventories on your integration.
    """

    def __init__(self, secret_key: Optional[str] = None):
        super().__init__(secret_key)

    def create_product(self, name: str, description: str, price: int, currency: str, unlimited: Optional[bool] = None, quantity: Optional[int] = None) -> PaystackResponse:
        """
        Create a product on your integration

        Args:
            name: Name of product
            description: A description for this product
            price: Price should be in the subunit of the supported currency
            currency: Currency in which price is set
            unlimited: Set to true if the product has unlimited stock. Leave as false if the product has limited stock
            quantity: Number of products in stock. Use if unlimited is false

        Returns:
            PaystackResponse: The response from the API
        """
        payload = {
            "name": name,
            "description": description,
            "price": price,
            "currency": currency,
        }
        if unlimited is not None:
            payload["unlimited"] = unlimited
        if quantity:
            payload["quantity"] = quantity

        return self.request("POST", "product", json_data=payload)

    def list_products(self, per_page: Optional[int] = None, page: Optional[int] = None, from_date: Optional[str] = None, to_date: Optional[str] = None) -> PaystackResponse:
        """
        List products available on your integration

        Args:
            per_page: Specify how many records you want to retrieve per page. If not specify we use a default value of 50.
            page: Specify exactly what page you want to retrieve. If not specify we use a default value of 1.
            from_date: A timestamp from which to start listing product e.g. 2016-09-24T00:00:05.000Z, 2016-09-21
            to_date: A timestamp at which to stop listing product e.g. 2016-09-24T00:00:05.000Z, 2016-09-21

        Returns:
            PaystackResponse: The response from the API
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

        return self.request("GET", "product", params=params)

    def fetch_product(self, product_id: str) -> PaystackResponse:
        """
        Get details of a product on your integration

        Args:
            product_id: The product ID you want to fetch

        Returns:
            PaystackResponse: The response from the API
        """
        return self.request("GET", f"product/{product_id}")

    def update_product(self, product_id: str, name: Optional[str] = None, description: Optional[str] = None, price: Optional[int] = None, currency: Optional[str] = None, unlimited: Optional[bool] = None, quantity: Optional[int] = None) -> PaystackResponse:
        """
        Update a product details on your integration

        Args:
            product_id: Product ID
            name: Name of product
            description: A description for this product
            price: Price should be in the subunit of the supported currency
            currency: Currency in which price is set
            unlimited: Set to true if the product has unlimited stock. Leave as false if the product has limited stock
            quantity: Number of products in stock. Use if unlimited is false

        Returns:
            PaystackResponse: The response from the API
        """
        payload = {}
        if name:
            payload["name"] = name
        if description:
            payload["description"] = description
        if price:
            payload["price"] = price
        if currency:
            payload["currency"] = currency
        if unlimited is not None:
            payload["unlimited"] = unlimited
        if quantity:
            payload["quantity"] = quantity

        return self.request("PUT", f"product/{product_id}", json_data=payload)
