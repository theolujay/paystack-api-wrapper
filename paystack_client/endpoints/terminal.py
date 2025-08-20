"""
The Terminal API allows you to build delightful in-person payment experiences.
"""

import requests
from typing import Optional, List, Dict, Any, Tuple

from ..core import BaseClient


class TerminalAPI(BaseClient):
    """
    The Terminal API allows you to build delightful in-person payment experiences.
    """

    def __init__(self, secret_key: str, session: requests.Session = None, base_url: str = None):
        super().__init__(secret_key, session=session, base_url=base_url)

    def send_event(
        self, terminal_id: str, type: str, action: str, data: Dict[str, Any]
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Send an event from your application to the Paystack Terminal

        Args:
            terminal_id: The ID of the Terminal the event should be sent to.
            type: The type of event to push. We currently support invoice and transaction
            action: The action the Terminal needs to perform. For the invoice type, the action can either be process or view. For the transaction type, the action can either be process or print.
            data: The paramters needed to perform the specified action. For the invoice type, you need to pass the invoice id and offline reference: {id: invoice_id, reference: offline_reference}. For the transaction type, you can pass the transaction id: {id: transaction_id}

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        payload = {
            "type": type,
            "action": action,
            "data": data,
        }
        return self.request("POST", f"terminal/{terminal_id}/event", json_data=payload)

    def fetch_event_status(
        self, terminal_id: str, event_id: str
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Check the status of an event sent to the Terminal

        Args:
            terminal_id: The ID of the Terminal the event was sent to.
            event_id: The ID of the event that was sent to the Terminal

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        return self.request("GET", f"terminal/{terminal_id}/event/{event_id}")

    def fetch_terminal_status(
        self, terminal_id: str
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Check the availiability of a Terminal before sending an event to it

        Args:
            terminal_id: The ID of the Terminal you want to check

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        return self.request("GET", f"terminal/{terminal_id}/presence")

    def list_terminals(
        self,
        per_page: Optional[int] = None,
        next_cursor: Optional[str] = None,
        previous_cursor: Optional[str] = None,
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        List the Terminals available on your integration

        Args:
            per_page: Specify how many records you want to retrieve per page. If not specify we use a default value of 50.
            next_cursor: A cursor that indicates your place in the list. It can be used to fetch the next page of the list
            previous_cursor: A cursor that indicates your place in the list. It should be used to fetch the previous page of the list after an intial next request

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        params = {}
        if per_page:
            params["perPage"] = per_page
        if next_cursor:
            params["next"] = next_cursor
        if previous_cursor:
            params["previous"] = previous_cursor

        return self.request("GET", "terminal", params=params)

    def fetch_terminal(self, terminal_id: str) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Get the details of a Terminal

        Args:
            terminal_id: The ID of the Terminal the event was sent to.

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        return self.request("GET", f"terminal/{terminal_id}")

    def update_terminal(
        self,
        terminal_id: str,
        name: Optional[str] = None,
        address: Optional[str] = None,
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Update the details of a Terminal

        Args:
            terminal_id: The ID of the Terminal you want to update
            name: Name of the terminal
            address: The address of the Terminal

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        payload = {}
        if name:
            payload["name"] = name
        if address:
            payload["address"] = address

        return self.request("PUT", f"terminal/{terminal_id}", json_data=payload)

    def commission_terminal(
        self, serial_number: str
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Activate your debug device by linking it to your integration

        Args:
            serial_number: Device Serial Number

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        payload = {"serial_number": serial_number}
        return self.request("POST", "terminal/commission_device", json_data=payload)

    def decommission_terminal(
        self, serial_number: str
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Unlink your debug device from your integration

        Args:
            serial_number: Device Serial Number

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        payload = {"serial_number": serial_number}
        return self.request("POST", "terminal/decommission_device", json_data=payload)
