"""
The Subaccounts API allows you create and manage subaccounts on your integration.
"""

import requests
from typing import Optional, Dict, Any, Tuple

from ..core import BaseClient


class SubaccountsAPI(BaseClient):
    """
    The Subaccounts API allows you create and manage subaccounts on your integration.
    """

    def __init__(
        self, secret_key: str, session: requests.Session = None, base_url: str = None
    ):
        super().__init__(secret_key, session=session, base_url=base_url)

    def create_subaccount(
        self,
        business_name: str,
        bank_code: str,
        account_number: str,
        percentage_charge: float,
        description: Optional[str] = None,
        primary_contact_email: Optional[str] = None,
        primary_contact_name: Optional[str] = None,
        primary_contact_phone: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Create a subacount on your integration

        Args:
            business_name: Name of business for subaccount
            bank_code: Bank Code for the bank. You can get the list of Bank Codes by calling the List Banks endpoint.
            account_number: Bank Account Number
            percentage_charge: The percentage the main account receives from each payment made to the subaccount
            description: A description for this subaccount
            primary_contact_email: A contact email for the subaccount
            primary_contact_name: A name for the contact person for this subaccount
            primary_contact_phone: A phone number to call for this subaccount
            metadata: Stringified JSON object. Add a custom_fields attribute which has an array of objects if you would like the fields to be added to your transaction when displayed on the dashboard. Sample: {"custom_fields":[{"display_name":"Cart ID","variable_name": "cart_id","value": "8393"}]}

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        payload = {
            "business_name": business_name,
            "bank_code": bank_code,
            "account_number": account_number,
            "percentage_charge": percentage_charge,
        }
        if description:
            payload["description"] = description
        if primary_contact_email:
            payload["primary_contact_email"] = primary_contact_email
        if primary_contact_name:
            payload["primary_contact_name"] = primary_contact_name
        if primary_contact_phone:
            payload["primary_contact_phone"] = primary_contact_phone
        if metadata:
            payload["metadata"] = metadata

        return self.request("POST", "subaccount", json_data=payload)

    def list_subaccounts(
        self,
        per_page: Optional[int] = None,
        page: Optional[int] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        List subaccounts available on your integration

        Args:
            per_page: Specify how many records you want to retrieve per page. If not specify we use a default value of 50.
            page: Specify exactly what page you want to retrieve. If not specify we use a default value of 1.
            from_date: A timestamp from which to start listing subaccounts e.g. 2016-09-24T00:00:05.000Z, 2016-09-21
            to_date: A timestamp at which to stop listing subaccounts e.g. 2016-09-24T00:00:05.000Z, 2016-09-21

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

        return self.request("GET", "subaccount", params=params)

    def fetch_subaccount(
        self, id_or_code: str
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Get details of a subaccount on your integration

        Args:
            id_or_code: The subaccount ID or code you want to fetch

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        return self.request("GET", f"subaccount/{id_or_code}")

    def update_subaccount(
        self,
        id_or_code: str,
        business_name: Optional[str] = None,
        description: Optional[str] = None,
        bank_code: Optional[str] = None,
        account_number: Optional[str] = None,
        active: Optional[bool] = None,
        percentage_charge: Optional[float] = None,
        primary_contact_email: Optional[str] = None,
        primary_contact_name: Optional[str] = None,
        primary_contact_phone: Optional[str] = None,
        settlement_schedule: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Update a subaccount details on your integration

        Args:
            id_or_code: Subaccount's ID or code
            business_name: Name of business for subaccount
            description: A description for this subaccount
            bank_code: Bank Code for the bank. You can get the list of Bank Codes by calling the List Banks endpoint.
            account_number: Bank Account Number
            active: Activate or deactivate a subaccount. Set value to true to activate subaccount or false to deactivate the subaccount.
            percentage_charge: The default percentage charged when receiving on behalf of this subaccount
            primary_contact_email: A contact email for the subaccount
            primary_contact_name: A name for the contact person for this subaccount
            primary_contact_phone: A phone number to call for this subaccount
            settlement_schedule: Any of auto, weekly, `monthly`, `manual`. Auto means payout is T+1 and manual means payout to the subaccount should only be made when requested. Defaults to auto
            metadata: Stringified JSON object. Add a custom_fields attribute which has an array of objects if you would like the fields to be added to your transaction when displayed on the dashboard. Sample: {"custom_fields":[{"display_name":"Cart ID","variable_name": "cart_id","value": "8393"}]}

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        payload = {}
        if business_name:
            payload["business_name"] = business_name
        if description:
            payload["description"] = description
        if bank_code:
            payload["bank_code"] = bank_code
        if account_number:
            payload["account_number"] = account_number
        if active is not None:
            payload["active"] = active
        if percentage_charge:
            payload["percentage_charge"] = percentage_charge
        if primary_contact_email:
            payload["primary_contact_email"] = primary_contact_email
        if primary_contact_name:
            payload["primary_contact_name"] = primary_contact_name
        if primary_contact_phone:
            payload["primary_contact_phone"] = primary_contact_phone
        if settlement_schedule:
            payload["settlement_schedule"] = settlement_schedule
        if metadata:
            payload["metadata"] = metadata

        return self.request("PUT", f"subaccount/{id_or_code}", json_data=payload)
