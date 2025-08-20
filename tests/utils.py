import pytest

from paystack import AuthenticationError


def assert_api_error_contains(callable_method, expected_keyword, *args, **kwargs):
    with pytest.raises(AuthenticationError) as excinfo:
        callable_method(*args, **kwargs)
    assert str(expected_keyword).lower() in str(excinfo.value).lower()