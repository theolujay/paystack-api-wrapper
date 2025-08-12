import pytest
import os
from dotenv import load_dotenv

@pytest.fixture(autouse=True)
def load_test_env():
    """Automatically load test environment for all tests"""
    load_dotenv('.env.test')
    
@pytest.fixture
def secret_key():
    return os.getenv("PAYSTACK_SECRET_KEY")

