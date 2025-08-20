import pytest
import responses
from paystack_client import ValidationError
from paystack_client.exceptions import APIError


@responses.activate
def test_create_customer(customers_client):
    payload = {
        "email": "customer@example.com",
        "first_name": "John",
        "last_name": "Doe",
    }
    mock_response = {
        "status": True,
        "message": "Customer created",
        "data": {"email": payload["email"], "customer_code": "CUS_test"},
    }
    responses.add(
        responses.POST,
        f"{customers_client.base_url}/customer",
        json=mock_response,
        status=200,
    )

    data, meta = customers_client.create(**payload)

    assert data["email"] == payload["email"]
    assert data["customer_code"] == "CUS_test"
    assert meta == {}


@responses.activate
def test_create_customer_with_metadata(customers_client):
    payload = {
        "email": "customer_meta@example.com",
        "metadata": {"age": 30, "city": "Lagos"},
    }
    mock_response = {
        "status": True,
        "message": "Customer created",
        "data": {"email": payload["email"], "customer_code": "CUS_meta"},
    }
    responses.add(
        responses.POST,
        f"{customers_client.base_url}/customer",
        json=mock_response,
        status=200,
    )

    data, meta = customers_client.create(**payload)

    assert data["email"] == payload["email"]
    assert data["customer_code"] == "CUS_meta"
    assert meta == {}


@responses.activate
def test_create_customer_with_required_fields_validation(customers_client):
    payload = {
        "email": "customer@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "phone": "08012345678",
    }
    mock_response = {
        "status": True,
        "message": "Customer created",
        "data": {"email": payload["email"], "customer_code": "CUS_test"},
    }
    responses.add(
        responses.POST,
        f"{customers_client.base_url}/customer",
        json=mock_response,
        status=200,
    )

    data, meta = customers_client.create(**payload, validate_required_fields=True)

    assert data["email"] == payload["email"]
    assert data["customer_code"] == "CUS_test"
    assert meta == {}


@responses.activate
def test_create_customer_with_required_fields_validation_missing_fields(customers_client):
    payload = {
        "email": "customer@example.com",
        "first_name": "John",
        # Missing last_name and phone
    }
    with pytest.raises(ValidationError, match="Missing required parameters: last_name, phone"):
        customers_client.create(**payload, validate_required_fields=True)


@responses.activate
def test_create_customer_invalid_email(customers_client):
    payload = {
        "email": "invalid-email",
        "first_name": "John",
        "last_name": "Doe",
    }
    with pytest.raises(ValidationError):
        customers_client.create(**payload)


@responses.activate
def test_list_customers(customers_client):
    mock_response = {
        "status": True,
        "message": "Customers retrieved",
        "data": [
            {"email": "customer1@example.com"},
            {"email": "customer2@example.com"},
        ],
    }
    responses.add(
        responses.GET,
        f"{customers_client.base_url}/customer",
        json=mock_response,
        status=200,
    )

    data, meta = customers_client.list_customers()

    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["email"] == "customer1@example.com"
    assert meta == {}


@responses.activate
def test_list_customers_with_all_params(customers_client):
    mock_response = {
        "status": True,
        "message": "Customers retrieved",
        "data": [{"email": "customer1@example.com"}],
    }
    responses.add(
        responses.GET,
        f"{customers_client.base_url}/customer?perPage=1&page=1&from=2023-01-01&to=2023-01-31",
        json=mock_response,
        status=200,
    )

    data, meta = customers_client.list_customers(
        per_page=1, page=1, from_date="2023-01-01", to_date="2023-01-31"
    )

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["email"] == "customer1@example.com"
    assert meta == {}


@responses.activate
def test_fetch_customer(customers_client):
    email_or_code = "customer@example.com"
    mock_response = {
        "status": True,
        "message": "Customer retrieved",
        "data": {"email": email_or_code, "customer_code": "CUS_test"},
    }
    responses.add(
        responses.GET,
        f"{customers_client.base_url}/customer/{email_or_code}",
        json=mock_response,
        status=200,
    )

    data, meta = customers_client.fetch(email_or_code=email_or_code)

    assert data["email"] == email_or_code
    assert data["customer_code"] == "CUS_test"
    assert meta == {}


@responses.activate
def test_update_customer(customers_client):
    code = "CUS_test"
    payload = {
        "first_name": "Jane",
    }
    mock_response = {
        "status": True,
        "message": "Customer updated",
        "data": {"customer_code": code, "first_name": "Jane"},
    }
    responses.add(
        responses.PUT,
        f"{customers_client.base_url}/customer/{code}",
        json=mock_response,
        status=200,
    )

    data, meta = customers_client.update(code=code, **payload)

    assert data["customer_code"] == code
    assert data["first_name"] == "Jane"
    assert meta == {}


@responses.activate
def test_update_customer_with_all_optional_params(customers_client):
    code = "CUS_test_all"
    payload = {
        "first_name": "Jane",
        "last_name": "Doe",
        "phone": "09012345678",
        "metadata": {"age": 35},
    }
    mock_response = {
        "status": True,
        "message": "Customer updated",
        "data": {"customer_code": code, "first_name": "Jane"},
    }
    responses.add(
        responses.PUT,
        f"{customers_client.base_url}/customer/{code}",
        json=mock_response,
        status=200,
    )

    data, meta = customers_client.update(code=code, **payload)

    assert data["customer_code"] == code
    assert data["first_name"] == "Jane"
    assert meta == {}


@responses.activate
def test_update_customer_with_last_name(customers_client):
    code = "CUS_test_last_name"
    payload = {
        "last_name": "Doe",
    }
    mock_response = {
        "status": True,
        "message": "Customer updated",
        "data": {"customer_code": code, "last_name": "Doe"},
    }
    responses.add(
        responses.PUT,
        f"{customers_client.base_url}/customer/{code}",
        json=mock_response,
        status=200,
    )

    data, meta = customers_client.update(code=code, **payload)

    assert data["customer_code"] == code
    assert data["last_name"] == "Doe"
    assert meta == {}


@responses.activate
def test_update_customer_with_phone(customers_client):
    code = "CUS_test_phone"
    payload = {
        "phone": "09012345678",
    }
    mock_response = {
        "status": True,
        "message": "Customer updated",
        "data": {"customer_code": code, "phone": "09012345678"},
    }
    responses.add(
        responses.PUT,
        f"{customers_client.base_url}/customer/{code}",
        json=mock_response,
        status=200,
    )

    data, meta = customers_client.update(code=code, **payload)

    assert data["customer_code"] == code
    assert data["phone"] == "09012345678"
    assert meta == {}


@responses.activate
def test_update_customer_only_first_name(customers_client):
    code = "CUS_test_only_first_name"
    payload = {
        "first_name": "OnlyFirst",
    }
    mock_response = {
        "status": True,
        "message": "Customer updated",
        "data": {"customer_code": code, "first_name": "OnlyFirst"},
    }
    responses.add(
        responses.PUT,
        f"{customers_client.base_url}/customer/{code}",
        json=mock_response,
        status=200,
    )

    data, meta = customers_client.update(code=code, **payload)

    assert data["customer_code"] == code
    assert data["first_name"] == "OnlyFirst"
    assert meta == {}


@responses.activate
def test_update_customer_only_last_name(customers_client):
    code = "CUS_test_only_last_name"
    payload = {
        "last_name": "OnlyLast",
    }
    mock_response = {
        "status": True,
        "message": "Customer updated",
        "data": {"customer_code": code, "last_name": "OnlyLast"},
    }
    responses.add(
        responses.PUT,
        f"{customers_client.base_url}/customer/{code}",
        json=mock_response,
        status=200,
    )

    data, meta = customers_client.update(code=code, **payload)

    assert data["customer_code"] == code
    assert data["last_name"] == "OnlyLast"
    assert meta == {}


@responses.activate
def test_update_customer_only_phone(customers_client):
    code = "CUS_test_only_phone"
    payload = {
        "phone": "09011112222",
    }
    mock_response = {
        "status": True,
        "message": "Customer updated",
        "data": {"customer_code": code, "phone": "09011112222"},
    }
    responses.add(
        responses.PUT,
        f"{customers_client.base_url}/customer/{code}",
        json=mock_response,
        status=200,
    )

    data, meta = customers_client.update(code=code, **payload)

    assert data["customer_code"] == code
    assert data["phone"] == "09011112222"
    assert meta == {}


@responses.activate
def test_update_customer_no_fields(customers_client):
    code = "CUS_test"
    with pytest.raises(ValidationError):
        customers_client.update(code=code)


@responses.activate
def test_validate_identity(customers_client):
    payload = {
        "customer_code": "CUS_test",
        "country": "NG",
        "identification_type": "bank_account",
        "first_name": "John",
        "last_name": "Doe",
        "bvn": "12345678901",
    }
    mock_response = {
        "status": True,
        "message": "Identity validated",
        "data": {"customer_code": payload["customer_code"]},
    }
    responses.add(
        responses.POST,
        f"{customers_client.base_url}/customer/{payload['customer_code']}/identification",
        json=mock_response,
        status=200,
    )

    data, meta = customers_client.validate_identity(**payload)

    assert data["customer_code"] == payload["customer_code"]
    assert meta == {}


@responses.activate
def test_set_risk_action(customers_client):
    payload = {
        "customer": "customer@example.com",
        "risk_action": "deny",
    }
    mock_response = {
        "status": True,
        "message": "Risk action set",
        "data": {
            "customer": payload["customer"],
            "risk_action": payload["risk_action"],
        },
    }
    responses.add(
        responses.POST,
        f"{customers_client.base_url}/customer/set_risk_action",
        json=mock_response,
        status=200,
    )

    data, meta = customers_client.set_risk_action(**payload)

    assert data["customer"] == payload["customer"]
    assert data["risk_action"] == payload["risk_action"]
    assert meta == {}


@responses.activate
def test_set_risk_action_invalid_action(customers_client):
    payload = {
        "customer": "customer@example.com",
        "risk_action": "invalid",
    }
    with pytest.raises(ValidationError):
        customers_client.set_risk_action(**payload)


@responses.activate
def test_initialize_authorization(customers_client):
    payload = {
        "email": "customer@example.com",
        "channel": "direct_debit",
    }
    mock_response = {
        "status": True,
        "message": "Authorization initialized",
        "data": {
            "authorization_url": "http://example.com/auth",
            "reference": "auth_ref",
        },
    }
    responses.add(
        responses.POST,
        f"{customers_client.base_url}/customer/authorization/initialize",
        json=mock_response,
        status=200,
    )

    data, meta = customers_client.initialize_authorization(**payload)

    assert data["reference"] == "auth_ref"
    assert meta == {}


@responses.activate
def test_initialize_authorization_invalid_email(customers_client):
    payload = {
        "email": "invalid-email",
        "channel": "direct_debit",
    }
    with pytest.raises(ValidationError):
        customers_client.initialize_authorization(**payload)


@responses.activate
def test_verify_authorization(customers_client):
    reference = "auth_ref"
    mock_response = {
        "status": True,
        "message": "Authorization verified",
        "data": {"reference": reference, "status": "success"},
    }
    responses.add(
        responses.GET,
        f"{customers_client.base_url}/customer/authorization/verify/{reference}",
        json=mock_response,
        status=200,
    )

    data, meta = customers_client.verify_authorization(reference=reference)

    assert data["reference"] == reference
    assert data["status"] == "success"
    assert meta == {}


@responses.activate
def test_initialize_direct_debit(customers_client):
    payload = {
        "customer_id": "CUS_test",
        "account": {"number": "0123456789", "bank_code": "044"},
        "address": {"street": "123 Main St", "city": "Lagos", "state": "Lagos"},
    }
    mock_response = {
        "status": True,
        "message": "Direct debit initialized",
        "data": {"customer_id": payload["customer_id"]},
    }
    responses.add(
        responses.POST,
        f"{customers_client.base_url}/customer/{payload['customer_id']}/initialize-direct-debit",
        json=mock_response,
        status=200,
    )

    data, meta = customers_client.initialize_direct_debit(**payload)

    assert data["customer_id"] == payload["customer_id"]
    assert meta == {}


@responses.activate
def test_initialize_direct_debit_invalid_account(customers_client):
    payload = {
        "customer_id": "CUS_test",
        "account": {"number": "0123456789"},  # Missing bank_code
        "address": {"street": "123 Main St", "city": "Lagos", "state": "Lagos"},
    }
    with pytest.raises(ValidationError):
        customers_client.initialize_direct_debit(**payload)


@responses.activate
def test_initialize_direct_debit_invalid_account_missing_bank_code(customers_client):
    payload = {
        "customer_id": "CUS_test",
        "account": {"number": "0123456789"},  # Missing bank_code
        "address": {"street": "123 Main St", "city": "Lagos", "state": "Lagos"},
    }
    with pytest.raises(ValidationError, match="account must contain 'number' and 'bank_code'"):
        customers_client.initialize_direct_debit(**payload)


@responses.activate
def test_initialize_direct_debit_invalid_account_missing_number(customers_client):
    payload = {
        "customer_id": "CUS_test",
        "account": {"bank_code": "044"},  # Missing number
        "address": {"street": "123 Main St", "city": "Lagos", "state": "Lagos"},
    }
    with pytest.raises(ValidationError, match="account must contain 'number' and 'bank_code'"):
        customers_client.initialize_direct_debit(**payload)


@responses.activate
def test_initialize_direct_debit_invalid_address_missing_street(customers_client):
    payload = {
        "customer_id": "CUS_test",
        "account": {"number": "0123456789", "bank_code": "044"},
        "address": {"city": "Lagos", "state": "Lagos"},  # Missing street
    }
    with pytest.raises(ValidationError, match="address must contain 'street', 'city', and 'state'"):
        customers_client.initialize_direct_debit(**payload)


@responses.activate
def test_initialize_direct_debit_invalid_address_missing_city(customers_client):
    payload = {
        "customer_id": "CUS_test",
        "account": {"number": "0123456789", "bank_code": "044"},
        "address": {"street": "123 Main St", "state": "Lagos"},  # Missing city
    }
    with pytest.raises(ValidationError, match="address must contain 'street', 'city', and 'state'"):
        customers_client.initialize_direct_debit(**payload)


@responses.activate
def test_initialize_direct_debit_invalid_address_missing_state(customers_client):
    payload = {
        "customer_id": "CUS_test",
        "account": {"number": "0123456789", "bank_code": "044"},
        "address": {"street": "123 Main St", "city": "Lagos"},  # Missing state
    }
    with pytest.raises(ValidationError, match="address must contain 'street', 'city', and 'state'"):
        customers_client.initialize_direct_debit(**payload)


@responses.activate
def test_direct_debit_activation_charge(customers_client):
    customer_id = "CUS_test"
    authorization_id = 12345
    mock_response = {
        "status": True,
        "message": "Activation charge successful",
        "data": {"customer_id": customer_id},
    }
    responses.add(
        responses.PUT,
        f"{customers_client.base_url}/customer/{customer_id}/directdebit-activation-charge",
        json=mock_response,
        status=200,
    )

    data, meta = customers_client.direct_debit_activation_charge(
        customer_id=customer_id, authorization_id=authorization_id
    )

    assert data["customer_id"] == customer_id
    assert meta == {}


@responses.activate
def test_fetch_mandate_authorizations(customers_client):
    customer_id = "CUS_test"
    mock_response = {
        "status": True,
        "message": "Mandate authorizations retrieved",
        "data": [{"id": 1, "status": "active"}],
    }
    responses.add(
        responses.GET,
        f"{customers_client.base_url}/customer/{customer_id}/directdebit-mandate-authorizations",
        json=mock_response,
        status=200,
    )

    data, meta = customers_client.fetch_mandate_authorizations(customer_id=customer_id)

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["status"] == "active"
    assert meta == {}


@responses.activate
def test_deactivate_authorization(customers_client):
    authorization_code = "AUTH_test"
    mock_response = {
        "status": True,
        "message": "Authorization deactivated",
        "data": {"authorization_code": authorization_code},
    }
    responses.add(
        responses.POST,
        f"{customers_client.base_url}/customer/authorization/deactivate",
        json=mock_response,
        status=200,
    )

    data, meta = customers_client.deactivate_authorization(
        authorization_code=authorization_code
    )

    assert data["authorization_code"] == authorization_code
    assert meta == {}
