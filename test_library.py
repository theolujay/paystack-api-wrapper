#!/usr/bin/env python3
"""
Test script for paystack-client library
Run this to verify your library works correctly
"""

def test_import():
    """Test basic imports"""
    print("1. Testing basic import...")
    try:
        import paystack
        print("✓ paystack imported successfully")
        print(f"✓ Available attributes: {dir(paystack)}")
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False
    return True

def test_modules():
    """Test individual module imports"""
    print("\n2. Testing module imports...")
    modules_to_test = [
        'core',
        'customers', 
        'transactions',
        'plans',
        'subscriptions',
        # Add other modules you want to test
    ]
    
    for module in modules_to_test:
        try:
            exec(f"from paystack import {module}")
            print(f"✓ {module} module imported successfully")
        except ImportError as e:
            print(f"✗ {module} module failed: {e}")

def test_client_creation():
    """Test creating a client instance"""
    print("\n3. Testing client creation...")
    try:
        from paystack import PaystackClient
        
        client = PaystackClient("test_sk_dummy_key_for_testing")
        print("✓ Client created successfully")
        print(f"✓ Client type: {type(client)}")

        expected_methods = ['customers', 'transactions', 'plans']
        for method in expected_methods:
            if hasattr(client, method):
                print(f"✓ Client has {method} method")
            else:
                print(f"⚠ Client missing {method} method")
                
    except ImportError as e:
        print(f"✗ Client import failed: {e}")
    except Exception as e:
        print(f"✗ Client creation failed: {e}")

def test_version():
    """Test version information"""
    print("\n4. Testing version...")
    try:
        import paystack
        if hasattr(paystack, '__version__'):
            print(f"✓ Version: {paystack.__version__}")
        else:
            print("⚠ No version information found")
    except Exception as e:
        print(f"✗ Version test failed: {e}")

def main():
    """Run all tests"""
    print("Testing paystack library")
    print("=" * 40)
    
    tests = [
        test_import,
        test_modules,
        test_client_creation,
        test_version
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"✗ Test {test.__name__} crashed: {e}")
            results.append(False)
    
    print("\n" + "=" * 40)
    passed = sum(1 for r in results if r is not False)
    total = len(tests)
    print(f"Summary: {passed}/{total} tests passed")
    
    if all(r is not False for r in results):
        print("🎉 All tests passed! Your library looks good.")
    else:
        print("⚠ Some tests failed. Check the output above.")

if __name__ == "__main__":
    main()
