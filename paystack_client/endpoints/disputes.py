"""
The Disputes API allows you manage transaction disputes.
"""

import requests
from typing import Optional, Dict, Any, Tuple, Union

from ..core import BaseClient


class DisputesAPI(BaseClient):
    """
    The Disputes API allows you manage transaction disputes.
    """

    def __init__(self, secret_key: str, session: requests.Session = None, base_url: str = None):
        super().__init__(secret_key, session=session, base_url=base_url)

    def list_disputes(
        self,
        from_date: str,
        to_date: str,
        per_page: Optional[int] = None,
        page: Optional[int] = None,
        transaction_id: Optional[str] = None,
        status: Optional[str] = None,
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        List disputes filed against you.

        Args:
            per_page: Specify how many records you want to retrieve per page. If not specify we use a default value of 50.
            page: Specify exactly what dispute you want to page. If not specify we use a default value of 1.
            from_date: A timestamp from which to start listing dispute e.g. 2016-09-21
            to_date: A timestamp at which to stop listing dispute e.g. 2016-09-21
            transaction_id: Transaction Id
            status: Dispute Status. Acceptable values: { awaiting-merchant-feedback | awaiting-bank-feedback | pending | resolved }

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        self._validate_required_params(from_date=from_date, to_date=to_date)
        payload = {
            "from": from_date,
            "to": to_date,
        }
        if per_page:
            payload["perPage"] = per_page
        if page:
            payload["page"] = page
        if from_date:
            payload["from"] = from_date
        if to_date:
            payload["to"] = to_date
        if transaction_id:
            payload["transaction"] = transaction_id
        if status:
            payload["status"] = status

        return self.request("GET", "dispute", params=payload)

    def fetch_dispute(self, dispute_id: str) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Get more details about a dispute.

        Args:
            dispute_id: The dispute ID you want to fetch

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        return self.request("GET", f"dispute/{dispute_id}")

    def list_transaction_disputes(
        self, transaction_id: str
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        This endpoint retrieves disputes for a particular transaction

        Args:
            transaction_id: The transaction ID you want to fetch

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        return self.request("GET", f"dispute/transaction/{transaction_id}")

    def update_dispute(
        self,
        dispute_id: str,
        refund_amount: Union[int, str],
        uploaded_filename: Optional[str] = None,
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Update details of a dispute on your integration

        Args:
            dispute_id: Dispute ID
            refund_amount: The amount to refund, in the subunit of the supported currency
            uploaded_filename: filename of attachment returned via response from upload url(GET /dispute/:id/upload_url)

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        self._validate_required_params(dispute_id=dispute_id, refund_amount=refund_amount)
        payload = {"refund_amount": refund_amount}
        if uploaded_filename:
            payload["uploaded_filename"] = uploaded_filename

        return self.request("PUT", f"dispute/{dispute_id}", json_data=payload)

    def add_evidence(
        self,
        dispute_id: str,
        customer_email: str,
        customer_name: str,
        customer_phone: str,
        service_details: str,
        delivery_address: Optional[str] = None,
        delivery_date: Optional[str] = None,
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Provide evidence for a dispute

        Args:
            dispute_id: Dispute ID
            customer_email: Customer email
            customer_name: Customer name
            customer_phone: Customer phone
            service_details: Details of service involved
            delivery_address: Delivery Address
            delivery_date: ISO 8601 representation of delivery date (YYYY-MM-DD)

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        self._validate_required_params(
            customer_email=customer_email, customer_name=customer_name, customer_phone=customer_phone, service_details=service_details
        )
        payload = {
            "customer_email": customer_email,
            "customer_name": customer_name,
            "customer_phone": customer_phone,
            "service_details": service_details,
        }
        if delivery_address:
            payload["delivery_address"] = delivery_address
        if delivery_date:
            payload["delivery_date"] = delivery_date

        return self.request("POST", f"dispute/{dispute_id}/evidence", json_data=payload)

    def get_upload_url(
        self, dispute_id: str, upload_filename: str
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        This endpoint retrieves disputes for a particular transaction

        Args:
            dispute_id: Dispute Id
            upload_filename: The file name, with its extension, that you want to upload. e.g filename.pdf

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        self._validate_required_params(dispute_id=dispute_id, upload_filename=upload_filename)
        params = {"upload_filename": upload_filename}
        return self.request("GET", f"dispute/{dispute_id}/upload_url", params=params)

    def resolve_dispute(
        self,
        dispute_id: str,
        resolution: str,
        message: str,
        refund_amount: Union[int, str],
        uploaded_filename: str,
        evidence: Optional[int] = None,
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Resolve a dispute on your integration

        Args:
            dispute_id: Dispute ID
            resolution: Dispute resolution. Accepted values: { merchant-accepted | declined }.
            message: Reason for resolving
            refund_amount: the amount to refund, in the subunit of the supported currency
            uploaded_filename: filename of attachment returned via response from upload url(GET /dispute/:id/upload_url)
            evidence: Evidence Id for fraud claims

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        self._validate_required_params(
            dispute_id=dispute_id, resolution=resolution, message=message, refund_amount=refund_amount, uploaded_filename=uploaded_filename
        )
        payload = {
            "resolution": resolution,
            "message": message,
            "refund_amount": refund_amount,
            "uploaded_filename": uploaded_filename,
        }
        if evidence:
            payload["evidence"] = evidence

        return self.request("PUT", f"dispute/{dispute_id}/resolve", json_data=payload)

    def export_disputes(
        self,
        from_date: str,
        to_date: str,
        per_page: Optional[int] = None,
        page: Optional[int] = None,
        transaction_id: Optional[str] = None,
        status: Optional[str] = None,
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Export disputes available on your integration

        Args:
            per_page: Specify how many records you want to retrieve per page. If not specify we use a default value of 50.
            page: Specify exactly what dispute you want to page. If not specify we use a default value of 1.
            from_date: A timestamp from which to start listing dispute e.g. 2016-09-21
            to_date: A timestamp at which to stop listing dispute e.g. 2016-09-21
            transaction_id: Transaction Id
            status: Dispute Status. Acceptable values: { awaiting-merchant-feedback | awaiting-bank-feedback | pending | resolved }

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        payload = {
            "from": from_date,
            "to": to_date,
        }
        if per_page:
            payload["perPage"] = per_page
        if page:
            payload["page"] = page
        if transaction_id:
            payload["transaction"] = transaction_id
        if status:
            payload["status"] = status

        return self.request("GET", "dispute/export", params=payload)
