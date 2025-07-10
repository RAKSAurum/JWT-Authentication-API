"""
Custom JWT Authentication Backend Module

This module implements a custom JWT (JSON Web Token) authentication backend
for Django REST Framework. It provides secure token-based authentication
by validating JWT tokens from the Authorization header.

The authentication class integrates with Django's User model and provides
seamless JWT authentication for API endpoints.

Dependencies:
    - Django REST Framework
    - PyJWT library
    - Custom JWT utilities

Author: [Your Name]
Created: [Date]
Version: 1.0.0
"""

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User
from .utils import decode_jwt_token


class JWTAuthentication(BaseAuthentication):
    """
    Custom JWT authentication class for Django REST Framework.
    
    This class implements JWT token authentication by extracting and validating
    JWT tokens from the Authorization header. It follows the Bearer token
    authentication scheme and integrates with Django's User model.
    
    The authentication process:
    1. Extract Authorization header from request
    2. Parse Bearer token format
    3. Decode and validate JWT token
    4. Retrieve associated user from database
    5. Return authenticated user and token
    
    Attributes:
        None (inherits from BaseAuthentication)
    """
    
    def authenticate(self, request):
        """
        Authenticate a request using JWT token from Authorization header.
        
        Extracts the JWT token from the Authorization header, validates it,
        and returns the authenticated user. The method expects the header
        to follow the "Bearer <token>" format.
        
        Args:
            request (HttpRequest): The incoming HTTP request object containing
                the Authorization header with JWT token
                
        Returns:
            tuple: A tuple of (user, token) if authentication succeeds
            None: If no Authorization header is present (allowing other
                authentication methods to be tried)
                
        Raises:
            AuthenticationFailed: If the token is invalid, expired, malformed,
                or the associated user doesn't exist
                
        Example:
            Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
        """
        # Extract Authorization header from request
        auth_header = request.headers.get('Authorization')
        
        # Return None if no Authorization header (allow other auth methods)
        if not auth_header:
            return None
            
        try:
            # Parse Bearer token format: "Bearer <token>"
            prefix, token = auth_header.split(' ')
            
            # Validate Bearer prefix (case-insensitive)
            if prefix.lower() != 'bearer':
                return None
                
            # Decode and validate JWT token using utility function
            payload = decode_jwt_token(token)
            
            # Check for decoding errors
            if 'error' in payload:
                raise AuthenticationFailed(payload['error'])
                
            # Retrieve user from database using user ID from token payload
            user = User.objects.get(id=payload['user_id'])
            
            # Return authenticated user and token
            return (user, token)
            
        except ValueError:
            # Handle malformed Authorization header format
            raise AuthenticationFailed('Invalid authorization header format')
        except User.DoesNotExist:
            # Handle case where user in token doesn't exist in database
            raise AuthenticationFailed('User not found')
        except Exception as e:
            # Handle any other unexpected errors during authentication
            raise AuthenticationFailed(f'Authentication failed: {str(e)}')
    
    def authenticate_header(self, request):
        """
        Return the WWW-Authenticate header value for 401 responses.
        
        This method is called by Django REST Framework when authentication
        fails and a 401 Unauthorized response needs to be returned. It
        provides the proper WWW-Authenticate header to inform clients
        about the expected authentication scheme.
        
        Args:
            request (HttpRequest): The HTTP request object (unused)
            
        Returns:
            str: The authentication scheme identifier for WWW-Authenticate header
            
        Example:
            WWW-Authenticate: Bearer
        """
        return 'Bearer'