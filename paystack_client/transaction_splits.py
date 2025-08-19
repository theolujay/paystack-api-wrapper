"""
The Transaction Splits API enables merchants split the settlement for a transaction across their payout account, and one or more subaccounts.
"""

from typing import Optional, List, Dict, Any, Tuple

from .core import BaseClient


class TransactionSplitsAPI(BaseClient):
    """
    The Transaction Splits API enables merchants split the settlement for a transaction across their payout account, and one or more subaccounts.
    """

    def __init__(self, secret_key: Optional[str] = None):
        super().__init__(secret_key)

    def create_split(
        self,
        name: str,
        type: str,
        currency: str,
        subaccounts: List[Dict[str, Any]],
        bearer_type: str,
        bearer_subaccount: Optional[str] = None,
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Create a split payment on your integration

        Args:
            name: Name of the transaction split
            type: The type of transaction split you want to create. You can use one of the following: percentage | flat
            currency: Any of the supported currency
            subaccounts: A list of object containing subaccount code and number of shares: [{subaccount: ‘ACT_xxxxxxxxxx’, share: xxx},{...}]
            bearer_type: Any of subaccount | account | all-proportional | all
            bearer_subaccount: Subaccount code

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        payload = {
            "name": name,
            "type": type,
            "currency": currency,
            "subaccounts": subaccounts,
            "bearer_type": bearer_type,
        }
        if bearer_subaccount:
            payload["bearer_subaccount"] = bearer_subaccount

        return self.request("POST", "split", json_data=payload)

    def list_splits(
        self,
        name: Optional[str] = None,
        active: Optional[bool] = None,
        sort_by: Optional[str] = None,
        per_page: Optional[int] = None,
        page: Optional[int] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        List the transaction splits available on your integration

        Args:
            name: The name of the split
            active: Any of true or false
            sort_by: Sort by name, defaults to createdAt date
            per_page: Number of splits per page. If not specify we use a default value of 50.
            page: Page number to view. If not specify we use a default value of 1.
            from_date: A timestamp from which to start listing splits e.g. 2019-09-24T00:00:05.000Z, 2019-09-21
            to_date: A timestamp at which to stop listing splits e.g. 2019-09-24T00:00:05.000Z, 2019-09-21

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        params = {}
        if name:
            params["name"] = name
        if active is not None:
            params["active"] = active
        if sort_by:
            params["sort_by"] = sort_by
        if per_page:
            params["perPage"] = per_page
        if page:
            params["page"] = page
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date

        return self.request("GET", "split", params=params)

    def fetch_split(self, split_id: str) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Get details of a split on your integration

        Args:
            split_id: The id of the split

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        return self.request("GET", f"split/{split_id}")

    def update_split(
        self,
        split_id: str,
        name: str,
        active: bool,
        bearer_type: Optional[str] = None,
        bearer_subaccount: Optional[str] = None,
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Update a transaction split details on your integration

        Args:
            split_id: Split ID
            name: Name of the transaction split
            active: True or False
            bearer_type: Any of the following values: subaccount | account | all-proportional | all
            bearer_subaccount: Subaccount code of a subaccount in the split group. This should be specified only if the bearer_type is subaccount

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        payload = {
            "name": name,
            "active": active,
        }
        if bearer_type:
            payload["bearer_type"] = bearer_type
        if bearer_subaccount:
            payload["bearer_subaccount"] = bearer_subaccount

        return self.request("PUT", f"split/{split_id}", json_data=payload)

    def add_update_subaccount_split(
        self, split_id: str, subaccount: str, share: int
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Add a Subaccount to a Transaction Split, or update the share of an existing Subaccount in a Transaction Split

        Args:
            split_id: Split Id
            subaccount: This is the sub account code
            share: This is the transaction share for the subaccount

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        payload = {
            "subaccount": subaccount,
            "share": share,
        }
        return self.request(
            "POST", f"split/{split_id}/subaccount/add", json_data=payload
        )

    def remove_subaccount_from_split(
        self, split_id: str, subaccount: str
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Remove a subaccount from a transaction split

        Args:
            split_id: Split Id
            subaccount: This is the sub account code

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        payload = {"subaccount": subaccount}
        return self.request(
            "POST", f"split/{split_id}/subaccount/remove", json_data=payload
        )
