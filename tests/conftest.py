import pytest
import os
from dotenv import load_dotenv

from api.core import BaseClient
from api.transactions import Transaction


@pytest.fixture(autouse=True)
def load_test_env():
    """Automatically load test environment for all tests"""
    load_dotenv('.env.test')
    
@pytest.fixture
def secret_key():
    return os.getenv("PAYSTACK_SECRET_KEY")

@pytest.fixture
def base_client(secret_key):
    return BaseClient(secret_key=secret_key)

@pytest.fixture
def transaction_client(secret_key):
    return Transaction(secret_key=secret_key)
