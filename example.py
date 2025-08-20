import os

from paystack_client import PaystackClient
from paystack_client.exceptions import APIError, ValidationError

secret_key = os.getenv("PAYSTACK_SECRET_KEY")

if not secret_key:
    raise ValueError("PAYSTACK_SECRET_KEY environment variable not set.")

print("PAYSTACK_SECRET_KEY is set. Great job, Olujay!")

client = PaystackClient(secret_key=secret_key)

try:
    data, meta = client.transactions.initialize(
        email="customer@example.com",
        amount=50000,
        currency="NGN"
    )
    
    print("Transaction initialized successfully:")
    print(data)
    
except APIError as e:
    print(f"An API error occurred: {e.message}")
    if e.status_code:
        print(f"HTTP Status Code: {e.status_code}")
        
except ValidationError as e:
    print(f"A validation error occurred: {e}")
    
except Exception as e:
    print(f"An unexpected error occurred: {e}")