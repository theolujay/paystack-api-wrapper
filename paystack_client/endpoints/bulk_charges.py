"""
The Bulk Charges API allows you create and manage multiple recurring payments from your customers.
"""

import requests
from typing import Optional, List, Dict, Any, Tuple

from ..core import BaseClient


class BulkChargesAPI(BaseClient):
    """
    The Bulk Charges API allows you create and manage multiple recurring payments from your customers.
    """

    def __init__(self, secret_key: str, session: requests.Session = None, base_url: str = None):
        super().__init__(secret_key, session=session, base_url=base_url)

    def initiate_bulk_charge(
        self, charges: List[Dict[str, Any]]
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Send an array of objects with authorization codes and amount, using the supported currency format, so we can process transactions as a batch.

        Args:
            charges: A list of charge object. Each object consists of an authorization, amount and reference

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        self._validate_required_params(charges=charges)
        return self.request("POST", "bulkcharge", json_data=charges)

    def list_bulk_charge_batches(
        self,
        per_page: Optional[int] = None,
        page: Optional[int] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        This lists all bulk charge batches created by the integration. Statuses can be active, paused, or complete

        Args:
            per_page: Specify how many records you want to retrieve per page. If not specify we use a default value of 50.
            page: Specify exactly what transfer you want to page. If not specify we use a default value of 1.
            from_date: A timestamp from which to start listing batches e.g. 2016-09-24T00:00:05.000Z, 2016-09-21
            to_date: A timestamp at which to stop listing batches e.g. 2016-09-24T00:00:05.000Z, 2016-09-21

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

        return self.request("GET", "bulkcharge", params=params)

    def fetch_bulk_charge_batch(
        self, id_or_code: str
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        This endpoint retrieves a specific batch code. It also returns useful information on its progress by way of the total_charges and pending_charges attributes.

        Args:
            id_or_code: An ID or code for the charge whose batches you want to retrieve.

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        self._validate_required_params(id_or_code=id_or_code)
        return self.request("GET", f"bulkcharge/{id_or_code}")

    def fetch_charges_in_batch(
        self,
        id_or_code: str,
        status: Optional[str] = None,
        per_page: Optional[int] = None,
        page: Optional[int] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        This endpoint retrieves the charges associated with a specified batch code. Pagination parameters are available. You can also filter by status. Charge statuses can be pending, success or failed.

        Args:
            id_or_code: An ID or code for the batch whose charges you want to retrieve.
            status: Either one of these values: pending, success or failed
            per_page: Specify how many records you want to retrieve per page. If not specify we use a default value of 50.
            page: Specify exactly what transfer you want to page. If not specify we use a default value of 1.
            from_date: A timestamp from which to start listing charges e.g. 2016-09-24T00:00:05.000Z, 2016-09-21
            to_date: A timestamp at which to stop listing charges e.g. 2016-09-24T00:00:05.000Z, 2016-09-21

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        self._validate_required_params(id_or_code=id_or_code)
        params = {}
        if status:
            params["status"] = status
        if per_page:
            params["perPage"] = per_page
        if page:
            params["page"] = page
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date

        return self.request("GET", f"bulkcharge/{id_or_code}/charges", params=params)

    def pause_bulk_charge_batch(
        self, batch_code: str
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Use this endpoint to pause processing a batch

        Args:
            batch_code: The batch code for the bulk charge you want to pause

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        self._validate_required_params(batch_code=batch_code)
        return self.request("GET", f"bulkcharge/pause/{batch_code}")

    def resume_bulk_charge_batch(
        self, batch_code: str
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Use this endpoint to resume processing a batch

        Args:
            batch_code: The batch code for the bulk charge you want to resume

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        self._validate_required_params(batch_code=batch_code)
        return self.request("GET", f"bulkcharge/resume/{batch_code}")
