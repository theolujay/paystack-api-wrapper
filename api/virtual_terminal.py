"""
The Virtual Terminal API allows you to accept in-person payments without a POS device.
"""
from typing import Optional, List, Dict, Any

from .core import BaseClient, PaystackResponse


class VirtualTerminalAPI(BaseClient):
    """
    The Virtual Terminal API allows you to accept in-person payments without a POS device.
    """

    def __init__(self, secret_key: Optional[str] = None):
        super().__init__(secret_key)

    def create_virtual_terminal(self, name: str, destinations: List[Dict[str, Any]], metadata: Optional[List[Dict[str, Any]]] = None, currency: Optional[List[str]] = None, custom_fields: Optional[List[Dict[str, Any]]] = None) -> PaystackResponse:
        """
        Create a Virtual Terminal on your integration

        Args:
            name: Name of the Virtual Terminal
            destinations: An array of objects containing the notification recipients for payments to the Virtual Terminal. Each object includes a target parameter for the Whatsapp phone number to send notifications to, and a name parameter for a descriptive label.
            metadata: Stringified JSON object of custom data. Kindly check the Metadata page for more information
            currency: The transaction currency for the Virtual Terminal. Defaults to your integration currency
            custom_fields: An array of objects representing custom fields to display on the form. Each object contains a display_name parameter, representing what will be displayed on the Virtual Terminal page, and variable_name parameter for referencing the custom field programmatically

        Returns:
            PaystackResponse: The response from the API
        """
        payload = {
            "name": name,
            "destinations": destinations,
        }
        if metadata:
            payload["metadata"] = metadata
        if currency:
            payload["currency"] = currency
        if custom_fields:
            payload["custom_fields"] = custom_fields

        return self.request("POST", "virtual_terminal", json_data=payload)

    def list_virtual_terminals(self, status: Optional[str] = None, per_page: Optional[int] = None, search: Optional[str] = None, next_cursor: Optional[str] = None, previous_cursor: Optional[str] = None) -> PaystackResponse:
        """
        List Virtual Terminals on your integration

        Args:
            status: Filter by status ('active' or 'inactive')
            per_page: Number of records per page
            search: Search query string
            next_cursor: Cursor for next page
            previous_cursor: Cursor for previous page

        Returns:
            PaystackResponse: The response from the API
        """
        params = {}
        if status:
            params["status"] = status
        if per_page:
            params["perPage"] = per_page
        if search:
            params["search"] = search
        if next_cursor:
            params["next"] = next_cursor
        if previous_cursor:
            params["previous"] = previous_cursor

        return self.request("GET", "virtual_terminal", params=params)

    def fetch_virtual_terminal(self, code: str) -> PaystackResponse:
        """
        Fetch a Virtual Terminal on your integration

        Args:
            code: Code of the Virtual Terminal

        Returns:
            PaystackResponse: The response from the API
        """
        return self.request("GET", f"virtual_terminal/{code}")

    def update_virtual_terminal(self, code: str, name: str) -> PaystackResponse:
        """
        Update a Virtual Terminal on your integration

        Args:
            code: Code of the Virtual Terminal to update
            name: Name of the Virtual Terminal

        Returns:
            PaystackResponse: The response from the API
        """
        payload = {"name": name}
        return self.request("PUT", f"virtual_terminal/{code}", json_data=payload)

    def deactivate_virtual_terminal(self, code: str) -> PaystackResponse:
        """
        Deactivate a Virtual Terminal on your integration

        Args:
            code: Code of the Virtual Terminal to deactivate

        Returns:
            PaystackResponse: The response from the API
        """
        return self.request("PUT", f"virtual_terminal/{code}/deactivate")

    def assign_destination_to_virtual_terminal(self, code: str, destinations: List[Dict[str, Any]]) -> PaystackResponse:
        """
        Add a destination (WhatsApp number) to a Virtual Terminal on your integration

        Args:
            code: Code of the Virtual Terminal
            destinations: An array of objects containing the notification recipients for payments to the Virtual Terminal. Each object includes a target parameter for the Whatsapp phone number to send notifications to, and a name parameter for a descriptive label.

        Returns:
            PaystackResponse: The response from the API
        """
        payload = {"destinations": destinations}
        return self.request("POST", f"virtual_terminal/{code}/destination/assign", json_data=payload)

    def unassign_destination_from_virtual_terminal(self, code: str, targets: List[str]) -> PaystackResponse:
        """
        Unassign a destination (WhatsApp Number) summary of transactions from a Virtual Terminal on your integration

        Args:
            code: Code of the Virtual Terminal
            targets: Array of destination targets to unassign

        Returns:
            PaystackResponse: The response from the API
        """
        payload = {"targets": targets}
        return self.request("POST", f"virtual_terminal/{code}/destination/unassign", json_data=payload)

    def add_split_code_to_virtual_terminal(self, code: str, split_code: str) -> PaystackResponse:
        """
        Add a split code to a Virtual Terminal on your integration

        Args:
            code: Code of the Virtual Terminal
            split_code: Split code to be added to the Virtual Terminal

        Returns:
            PaystackResponse: The response from the API
        """
        payload = {"split_code": split_code}
        return self.request("PUT", f"virtual_terminal/{code}/split_code", json_data=payload)

    def remove_split_code_from_virtual_terminal(self, code: str, split_code: str) -> PaystackResponse:
        """
        Remove a split code from a Virtual Terminal on your integration

        Args:
            code: Code of the Virtual Terminal
            split_code: Split code to be removed from the Virtual Terminal

        Returns:
            PaystackResponse: The response from the API
        """
        payload = {"split_code": split_code}
        return self.request("DELETE", f"virtual_terminal/{code}/split_code", json_data=payload)
