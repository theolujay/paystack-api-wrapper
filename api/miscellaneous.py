# miscellaneous.py
from typing import Optional, Union, Dict, Any, Tuple
from .core import BaseClient
from .exceptions import APIError


class MiscellaneousAPI(BaseClient):
    """Miscellaneous API client for supporting APIs that provide additional details to other APIs."""

    def __init__(self, secret_key: Optional[str] = None):
        super().__init__(secret_key)

    def list_banks(
        self,
        country: str,
        use_cursor: bool,
        per_page: int,
        pay_with_bank_transfer: Optional[bool] = None,
        pay_with_bank: Optional[bool] = None,
        enabled_for_verification: Optional[bool] = None,
        next_cursor: Optional[str] = None,
        previous: Optional[str] = None,
        gateway: Optional[str] = None,
        type: Optional[str] = None,
        currency: Optional[str] = None,
        include_nip_sort_code: Optional[bool] = None,
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Get a list of all supported banks and their properties.

        Args:
            country: Country to obtain list of supported banks from.
                                   Accepted values: 'ghana', 'kenya', 'nigeria', 'south africa'
            use_cursor: Flag to enable cursor pagination on the endpoint
            per_page: Number of objects per page (default: 50, max: 100)
            pay_with_bank_transfer (Optional[bool]): Filter for banks available for transfer payments
            pay_with_bank (Optional[bool]): Filter for banks customers can pay directly from
            enabled_for_verification (Optional[bool]): Filter banks supported for account verification
                                                     in South Africa (combine with currency or country)
            next_cursor (Optional[str]): Cursor for fetching next page of results
            previous (Optional[str]): Cursor for fetching previous page of results
            gateway (Optional[str]): Gateway type of bank. Options: 'emandate', 'digitalbankmandate'
            type (Optional[str]): Type of financial channel. For Ghana: 'mobile_money' or 'ghipps'
            currency (Optional[str]): One of the supported currency codes
            include_nip_sort_code (Optional[bool]): Flag to return Nigerian banks with NIP institution code

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.

        Raises:
            APIError: If country value is invalid or per_page exceeds limits
        """
        self._validate_required_params(
            country=country, use_cursor=use_cursor, per_page=per_page
        )

        payload = {}

        if country:
            valid_countries = ["ghana", "kenya", "nigeria", "south africa"]
            if country.lower() not in valid_countries:
                raise APIError(f"country must be one of: {', '.join(valid_countries)}")
            payload["country"] = country.lower()

        if per_page is not None:
            if per_page <= 0 or per_page > 100:
                raise APIError("per_page must be between 1 and 100")
            payload["perPage"] = per_page

        if gateway:
            valid_gateways = ["emandate", "digitalbankmandate"]
            if gateway not in valid_gateways:
                raise APIError(f"gateway must be one of: {', '.join(valid_gateways)}")
            payload["gateway"] = gateway

        # Validate type parameter for Ghana if provided
        if type:
            valid_types = ["mobile_money", "ghipps"]
            if type not in valid_types:
                raise APIError(f"type must be one of: {', '.join(valid_types)}")
            payload["type"] = type

        # Add boolean parameters
        if use_cursor is not None:
            payload["use_cursor"] = str(use_cursor).lower()
        if pay_with_bank_transfer is not None:
            payload["pay_with_bank_transfer"] = str(pay_with_bank_transfer).lower()
        if pay_with_bank is not None:
            payload["pay_with_bank"] = str(pay_with_bank).lower()
        if enabled_for_verification is not None:
            payload["enabled_for_verification"] = str(enabled_for_verification).lower()
        if include_nip_sort_code is not None:
            payload["include_nip_sort_code"] = str(include_nip_sort_code).lower()

        # Add cursor parameters
        if next_cursor:
            payload["next"] = next_cursor
        if previous:
            payload["previous"] = previous

        # Add currency parameter
        if currency:
            payload["currency"] = currency

        return self.request("GET", "bank", payload=payload)

    def list_countries(self) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Get a list of countries that Paystack currently supports.

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.

        Note:
            This endpoint has no parameters - it returns all supported countries
        """
        return self.request("GET", "country")

    def list_states(
        self, country: Union[str, int]
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Get a list of states for a country for address verification.

        Args:
            country (Union[str, int]): The country code of the states to list.
                                     This is obtained after a charge request and can be
                                     either a country code string (e.g., 'CA') or integer ID

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.

        Raises:
            APIError: If country parameter is not provided
        """
        # Validate required parameter
        self._validate_required_params(country=country)

        params = {"country": str(country)}

        return self.request("GET", "address_verification/states", params=params)

    def get_nigerian_banks(
        self, include_nip_sort_code: bool = False
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Convenience method to get all Nigerian banks.

        Args:
            include_nip_sort_code (bool): Whether to include NIP institution codes

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        return self.list_banks(
            country="nigeria", include_nip_sort_code=include_nip_sort_code
        )

    def get_ghanaian_mobile_money_providers(
        self,
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Convenience method to get Ghanaian mobile money providers.

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        return self.list_banks(country="ghana", type="mobile_money")

    def get_ghanaian_banks(self) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Convenience method to get Ghanaian banks.

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        return self.list_banks(country="ghana", type="ghipps")

    def get_banks_for_transfer(
        self, country: str
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Convenience method to get banks that support bank transfers.

        Args:
            country (Optional[str]): Country to filter by

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        return self.list_banks(country=country, pay_with_bank_transfer=True)

    def get_banks_for_direct_payment(
        self, country: str
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Convenience method to get banks that support direct payments.

        Args:
            country (Optional[str]): Country to filter by

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        return self.list_banks(country=country, pay_with_bank=True)

    def get_south_african_verification_banks(
        self, currency: Optional[str] = None
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Convenience method to get South African banks that support account verification.

        Args:
            currency (Optional[str]): Currency to filter by

        Returns:
            Tuple[Dict[str, Any], Dict[str, Any]]: A tuple containing the response data and metadata.
        """
        return self.list_banks(
            country="south africa", enabled_for_verification=True, currency=currency
        )
