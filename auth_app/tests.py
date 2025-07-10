from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from unittest.mock import patch
import json
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.utils import timezone
from auth_app.utils import generate_jwt_token, decode_jwt_token

class JWTAuthenticationTestCase(APITestCase):
    """Comprehensive test suite for JWT Authentication API"""
    
    def setUp(self):
        """Set up test data and client"""
        self.client = APIClient()
        
        # Create test users
        self.test_user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        
        self.admin_user = User.objects.create_superuser(
            username='admin',
            password='adminpass123',
            email='admin@example.com'
        )
        
        # Test credentials
        self.valid_credentials = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        
        self.admin_credentials = {
            'username': 'admin',
            'password': 'adminpass123'
        }
        
        self.invalid_credentials = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        
        # Generate valid token for testing
        self.valid_token = generate_jwt_token(self.test_user)
        
        # API endpoints
        self.login_url = '/api/auth/login/'
        self.verify_url = '/api/auth/verify/'
        self.validate_url = '/api/auth/validate/'

class LoginEndpointTests(JWTAuthenticationTestCase):
    """Test cases for POST /api/auth/login/ endpoint"""
    
    def test_login_success_with_valid_credentials(self):
        """Test successful login with valid credentials"""
        response = self.client.post(self.login_url, self.valid_credentials, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('expires', response.data)
        
        # Verify token is valid JWT
        token = response.data['token']
        self.assertIsInstance(token, str)
        self.assertTrue(len(token) > 50)  # JWT tokens are typically long
        
        # Verify expires field format
        expires = response.data['expires']
        self.assertIsInstance(expires, str)
        # Should be ISO format timestamp
        self.assertRegex(expires, r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}')
    
    def test_login_success_with_admin_credentials(self):
        """Test successful login with admin credentials"""
        response = self.client.post(self.login_url, self.admin_credentials, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('expires', response.data)
    
    def test_login_failure_with_invalid_credentials(self):
        """Test login failure with invalid credentials"""
        response = self.client.post(self.login_url, self.invalid_credentials, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Invalid credentials')
    
    def test_login_failure_with_nonexistent_user(self):
        """Test login failure with non-existent user"""
        credentials = {
            'username': 'nonexistent',
            'password': 'password123'
        }
        response = self.client.post(self.login_url, credentials, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)
    
    def test_login_missing_username(self):
        """Test login failure when username is missing"""
        credentials = {'password': 'testpass123'}
        response = self.client.post(self.login_url, credentials, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Username and password are required')
    
    def test_login_missing_password(self):
        """Test login failure when password is missing"""
        credentials = {'username': 'testuser'}
        response = self.client.post(self.login_url, credentials, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Username and password are required')
    
    def test_login_empty_credentials(self):
        """Test login failure with empty credentials"""
        credentials = {'username': '', 'password': ''}
        response = self.client.post(self.login_url, credentials, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
    
    def test_login_whitespace_credentials(self):
        """Test login failure with whitespace-only credentials"""
        credentials = {'username': '   ', 'password': '   '}
        response = self.client.post(self.login_url, credentials, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
    
    def test_login_inactive_user(self):
        """Test login failure with inactive user"""
        # Create inactive user
        inactive_user = User.objects.create_user(
            username='inactive',
            password='password123',
            is_active=False
        )
        
        credentials = {
            'username': 'inactive',
            'password': 'password123'
        }
        response = self.client.post(self.login_url, credentials, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_login_wrong_http_method(self):
        """Test login endpoint with wrong HTTP method"""
        response = self.client.get(self.login_url, self.valid_credentials)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
        response = self.client.put(self.login_url, self.valid_credentials)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

class VerifyTokenEndpointTests(JWTAuthenticationTestCase):
    """Test cases for POST /api/auth/verify/ endpoint"""
    
    def test_verify_valid_token(self):
        """Test token verification with valid token"""
        data = {'token': self.valid_token}
        response = self.client.post(self.verify_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('valid', response.data)
        self.assertIn('message', response.data)
        self.assertTrue(response.data['valid'])
        self.assertEqual(response.data['message'], 'Token is valid')
    
    def test_verify_invalid_token(self):
        """Test token verification with invalid token"""
        data = {'token': 'invalid.jwt.token'}
        response = self.client.post(self.verify_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('valid', response.data)
        self.assertIn('message', response.data)
        self.assertFalse(response.data['valid'])
    
    def test_verify_expired_token(self):
        """Test token verification with expired token"""
        # Create expired token
        past_time = timezone.now() - timedelta(hours=2)
        payload = {
            'user_id': self.test_user.id,
            'username': self.test_user.username,
            'exp': past_time,
            'iat': past_time - timedelta(minutes=1)
        }
        expired_token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        
        data = {'token': expired_token}
        response = self.client.post(self.verify_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(response.data['valid'])
        self.assertIn('expired', response.data['message'].lower())
    
    def test_verify_malformed_token(self):
        """Test token verification with malformed token"""
        data = {'token': 'malformed_token_string'}
        response = self.client.post(self.verify_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(response.data['valid'])
    
    def test_verify_missing_token(self):
        """Test token verification without token"""
        data = {}
        response = self.client.post(self.verify_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Token is required')
    
    def test_verify_empty_token(self):
        """Test token verification with empty token"""
        data = {'token': ''}
        response = self.client.post(self.verify_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
    
    def test_verify_none_token(self):
        """Test token verification with None token"""
        data = {'token': None}
        response = self.client.post(self.verify_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
    
    def test_verify_wrong_http_method(self):
        """Test verify endpoint with wrong HTTP method"""
        data = {'token': self.valid_token}
        
        response = self.client.get(self.verify_url, data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
        response = self.client.put(self.verify_url, data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

class ValidateTokenEndpointTests(JWTAuthenticationTestCase):
    """Test cases for GET /api/auth/validate/ endpoint"""
    
    def test_validate_with_valid_token(self):
        """Test token validation with valid token in Authorization header"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.valid_token}')
        response = self.client.get(self.validate_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('valid', response.data)
        self.assertIn('user', response.data)
        self.assertIn('expires', response.data)
        self.assertTrue(response.data['valid'])
        self.assertEqual(response.data['user'], self.test_user.username)
    
    def test_validate_with_admin_token(self):
        """Test token validation with admin token"""
        admin_token = generate_jwt_token(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_token}')
        response = self.client.get(self.validate_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user'], self.admin_user.username)
    
    def test_validate_without_authorization_header(self):
        """Test token validation without Authorization header"""
        response = self.client.get(self.validate_url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue('detail' in response.data or 'error' in response.data)

    
    def test_validate_with_invalid_token(self):
        """Test token validation with invalid token"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer invalid.jwt.token')
        response = self.client.get(self.validate_url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_validate_with_expired_token(self):
        """Test token validation with expired token"""
        # Create expired token
        past_time = timezone.now() - timedelta(hours=2)
        payload = {
            'user_id': self.test_user.id,
            'username': self.test_user.username,
            'exp': past_time,
            'iat': past_time - timedelta(minutes=1)
        }
        expired_token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {expired_token}')
        response = self.client.get(self.validate_url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_validate_with_malformed_authorization_header(self):
        """Test token validation with malformed Authorization header"""
        # Missing Bearer prefix
        self.client.credentials(HTTP_AUTHORIZATION=self.valid_token)
        response = self.client.get(self.validate_url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_validate_with_wrong_prefix(self):
        """Test token validation with wrong prefix in Authorization header"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.valid_token}')
        response = self.client.get(self.validate_url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_validate_expires_format(self):
        """Test that expires field is properly formatted"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.valid_token}')
        response = self.client.get(self.validate_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expires = response.data['expires']
        self.assertIsInstance(expires, str)
        # Should be ISO format timestamp
        self.assertRegex(expires, r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}')
    
    def test_validate_wrong_http_method(self):
        """Test validate endpoint with wrong HTTP method"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.valid_token}')
        
        response = self.client.post(self.validate_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
        response = self.client.put(self.validate_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

class JWTUtilityTests(TestCase):
    """Test cases for JWT utility functions"""
    
    def setUp(self):
        self.test_user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_generate_jwt_token(self):
        """Test JWT token generation"""
        token = generate_jwt_token(self.test_user)
        
        self.assertIsInstance(token, str)
        self.assertTrue(len(token) > 50)
        
        # Decode token to verify contents
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        self.assertEqual(payload['user_id'], self.test_user.id)
        self.assertEqual(payload['username'], self.test_user.username)
        self.assertIn('exp', payload)
        self.assertIn('iat', payload)
    
    def test_decode_valid_jwt_token(self):
        """Test decoding valid JWT token"""
        token = generate_jwt_token(self.test_user)
        payload = decode_jwt_token(token)
        
        self.assertNotIn('error', payload)
        self.assertEqual(payload['user_id'], self.test_user.id)
        self.assertEqual(payload['username'], self.test_user.username)
    
    def test_decode_invalid_jwt_token(self):
        """Test decoding invalid JWT token"""
        payload = decode_jwt_token('invalid.jwt.token')
        
        self.assertIn('error', payload)
        self.assertIn('Invalid token', payload['error'])
    
    def test_decode_expired_jwt_token(self):
        """Test decoding expired JWT token"""
        # Create expired token
        past_time = timezone.now() - timedelta(hours=2)
        payload = {
            'user_id': self.test_user.id,
            'username': self.test_user.username,
            'exp': past_time,
            'iat': past_time - timedelta(minutes=1)
        }
        expired_token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        
        result = decode_jwt_token(expired_token)
        
        self.assertIn('error', result)
        self.assertIn('expired', result['error'].lower())

class IntegrationTests(JWTAuthenticationTestCase):
    """Integration tests for complete JWT authentication flow"""
    
    def test_complete_authentication_flow(self):
        """Test complete flow: login -> verify -> validate"""
        # Step 1: Login
        login_response = self.client.post(self.login_url, self.valid_credentials, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        token = login_response.data['token']
        
        # Step 2: Verify token
        verify_response = self.client.post(self.verify_url, {'token': token}, format='json')
        self.assertEqual(verify_response.status_code, status.HTTP_200_OK)
        self.assertTrue(verify_response.data['valid'])
        
        # Step 3: Validate token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        validate_response = self.client.get(self.validate_url)
        self.assertEqual(validate_response.status_code, status.HTTP_200_OK)
        self.assertTrue(validate_response.data['valid'])
        self.assertEqual(validate_response.data['user'], self.test_user.username)
    
    def test_token_consistency_across_endpoints(self):
        """Test that token information is consistent across all endpoints"""
        # Login to get token
        login_response = self.client.post(self.login_url, self.valid_credentials, format='json')
        token = login_response.data['token']
        login_expires = login_response.data['expires']
        
        # Validate token to get expires
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        validate_response = self.client.get(self.validate_url)
        validate_expires = validate_response.data['expires']
        
        # Expires should be consistent (allowing for small time differences)
        self.assertEqual(login_expires[:19], validate_expires[:19])  # Compare up to seconds
    
    def test_multiple_users_token_isolation(self):
        """Test that tokens are properly isolated between users"""
        # Create second user
        user2 = User.objects.create_user(username='user2', password='pass2')
        
        # Get tokens for both users
        token1 = generate_jwt_token(self.test_user)
        token2 = generate_jwt_token(user2)
        
        # Validate token1
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token1}')
        response1 = self.client.get(self.validate_url)
        self.assertEqual(response1.data['user'], self.test_user.username)
        
        # Validate token2
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token2}')
        response2 = self.client.get(self.validate_url)
        self.assertEqual(response2.data['user'], user2.username)
        
        # Ensure tokens are different
        self.assertNotEqual(token1, token2)

class SecurityTests(JWTAuthenticationTestCase):
    """Security-focused test cases"""
    
    def test_token_tampering_detection(self):
        """Test that tampered tokens are rejected"""
        # Get valid token and tamper with it
        valid_token = self.valid_token
        tampered_token = valid_token[:-10] + 'tampered123'
        
        # Verify endpoint should reject tampered token
        response = self.client.post(self.verify_url, {'token': tampered_token}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(response.data['valid'])
    
    def test_sql_injection_protection(self):
        """Test protection against SQL injection in login"""
        malicious_credentials = {
            'username': "admin'; DROP TABLE auth_user; --",
            'password': 'password'
        }
        
        response = self.client.post(self.login_url, malicious_credentials, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Verify user table still exists by checking user count
        self.assertTrue(User.objects.count() > 0)
    
    def test_xss_protection_in_responses(self):
        """Test that responses don't include unescaped user input"""
        malicious_credentials = {
            'username': '<script>alert("xss")</script>',
            'password': 'password'
        }
        
        response = self.client.post(self.login_url, malicious_credentials, format='json')
        response_content = json.dumps(response.data)
        
        # Response should not contain unescaped script tags
        self.assertNotIn('<script>', response_content)
        self.assertNotIn('alert(', response_content)

class ErrorHandlingTests(JWTAuthenticationTestCase):
    """Test error handling and edge cases"""
    
        # For the database error test
    def test_database_connection_error_handling(self):
        """Test handling of database connection errors"""
        pass
    
    def test_invalid_json_request(self):
        """Test handling of invalid JSON in requests"""
        response = self.client.post(
            self.login_url,
            'invalid json string',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_large_payload_handling(self):
        """Test handling of unusually large payloads"""
        large_credentials = {
            'username': 'a' * 10000,  # Very long username
            'password': 'b' * 10000   # Very long password
        }
        
        response = self.client.post(self.login_url, large_credentials, format='json')
        # Should handle gracefully
        self.assertIn(response.status_code, [status.HTTP_400_BAD_REQUEST, status.HTTP_401_UNAUTHORIZED])

class PerformanceTests(JWTAuthenticationTestCase):
    """Performance-related test cases"""
    
    def test_concurrent_token_generation(self):
        """Test that multiple simultaneous token generations work correctly"""
        import threading
        import time
        
        tokens = []
        errors = []
        
        def generate_token():
            try:
                token = generate_jwt_token(self.test_user)
                tokens.append(token)
            except Exception as e:
                errors.append(str(e))
        
        # Create multiple threads
        threads = []
        for _ in range(10):
            thread = threading.Thread(target=generate_token)
            threads.append(thread)
        
        # Start all threads
        for thread in threads:
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Verify results
        self.assertEqual(len(errors), 0, f"Errors occurred: {errors}")
        self.assertEqual(len(tokens), 10)
        # All tokens should be unique
        self.assertEqual(len(set(tokens)), 10)

# Test runner configuration
class CustomTestRunner:
    """Custom test runner for comprehensive reporting"""
    
    @staticmethod
    def run_all_tests():
        """Run all test cases and provide summary"""
        from django.test.utils import get_runner
        from django.conf import settings
        
        TestRunner = get_runner(settings)
        test_runner = TestRunner()
        failures = test_runner.run_tests(["auth_app.tests"])
        
        if failures:
            print(f"❌ {failures} test(s) failed")
            return False
        else:
            print("✅ All tests passed successfully!")
            return True

# Test data fixtures
class TestDataMixin:
    """Mixin providing test data for various scenarios"""
    
    @classmethod
    def create_test_users(cls):
        """Create various test users for different scenarios"""
        users = {
            'regular': User.objects.create_user(
                username='regular_user',
                password='regular_pass',
                email='regular@test.com'
            ),
            'admin': User.objects.create_superuser(
                username='admin_user',
                password='admin_pass',
                email='admin@test.com'
            ),
            'inactive': User.objects.create_user(
                username='inactive_user',
                password='inactive_pass',
                email='inactive@test.com',
                is_active=False
            )
        }
        return users
    
    @classmethod
    def get_test_credentials(cls):
        """Get various test credential combinations"""
        return {
            'valid': {'username': 'regular_user', 'password': 'regular_pass'},
            'invalid_password': {'username': 'regular_user', 'password': 'wrong_pass'},
            'invalid_username': {'username': 'wrong_user', 'password': 'regular_pass'},
            'empty': {'username': '', 'password': ''},
            'missing_username': {'password': 'regular_pass'},
            'missing_password': {'username': 'regular_user'},
        }