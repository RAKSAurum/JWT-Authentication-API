"""
JWT Utility Functions Module

This module provides utility functions for JWT token generation, decoding,
and user retrieval. It encapsulates the JWT operations using the PyJWT
library and integrates with Django's timezone and configuration systems.

The utilities handle:
- JWT token generation with user information and expiration
- JWT token decoding with comprehensive error handling
- User retrieval from JWT tokens

Dependencies:
    - PyJWT library for token operations
    - Django settings for JWT configuration
    - Django timezone utilities

Author: [Your Name]
Created: [Date]
Version: 1.0.0
"""

import jwt
import uuid
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User


def generate_jwt_token(user):
    """
    Generate a JWT token for the specified user with unique identifier.
    
    Creates a JWT token containing user information, expiration time,
    and a unique token identifier (JTI). The token is signed using
    the configured secret key and algorithm.
    
    Args:
        user (User): Django User instance for whom to generate the token
        
    Returns:
        str: Encoded JWT token string
        
    Raises:
        Exception: If token generation fails due to encoding errors
        
    Token Payload Structure:
        - user_id: Database ID of the user
        - username: Username of the user
        - exp: Token expiration timestamp
        - iat: Token issued at timestamp
        - jti: Unique token identifier for token revocation support
        
    Example:
        >>> user = User.objects.get(username='testuser')
        >>> token = generate_jwt_token(user)
        >>> print(len(token) > 50)  # JWT tokens are typically long
        True
    """
    # Get current timestamp for token metadata
    now = timezone.now()
    
    # Construct JWT payload with user information and metadata
    payload = {
        'user_id': user.id,              # User database primary key
        'username': user.username,        # Username for identification
        'exp': now + timedelta(seconds=settings.JWT_EXPIRATION_DELTA),  # Expiration time
        'iat': now,                      # Issued at time
        'jti': str(uuid.uuid4()),        # Unique token identifier
    }
    
    # Encode and sign the JWT token
    token = jwt.encode(
        payload, 
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    
    return token


def decode_jwt_token(token):
    """
    Decode and validate a JWT token, returning the payload or error information.
    
    Attempts to decode the provided JWT token using the configured secret key
    and algorithm. Handles various JWT-related exceptions and returns either
    the decoded payload or error information.
    
    Args:
        token (str): JWT token string to decode and validate
        
    Returns:
        dict: Either the decoded token payload or error information
            Success: {'user_id': int, 'username': str, 'exp': timestamp, ...}
            Error: {'error': 'Error description'}
            
    Exception Handling:
        - ExpiredSignatureError: Token has expired
        - InvalidTokenError: Token is malformed or signature is invalid
        - General Exception: Unexpected decoding errors
        
    Example:
        >>> payload = decode_jwt_token(valid_token)
        >>> if 'error' not in payload:
        ...     print(f"User ID: {payload['user_id']}")
        >>> else:
        ...     print(f"Error: {payload['error']}")
    """
    try:
        # Decode JWT token using configured secret and algorithm
        payload = jwt.decode(
            token, 
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
        
    except jwt.ExpiredSignatureError:
        # Handle expired token case
        return {'error': 'Token has expired'}
        
    except jwt.InvalidTokenError:
        # Handle invalid token format or signature
        return {'error': 'Invalid token'}
        
    except Exception as e:
        # Handle any other unexpected errors
        return {'error': f'Token decode error: {str(e)}'}


def get_user_from_token(token):
    """
    Retrieve a User instance from a JWT token.
    
    Decodes the JWT token and attempts to retrieve the corresponding
    User instance from the database. Returns None if the token is
    invalid or the user doesn't exist.
    
    Args:
        token (str): JWT token string containing user information
        
    Returns:
        User: Django User instance if token is valid and user exists
        None: If token is invalid or user doesn't exist in database
        
    Example:
        >>> user = get_user_from_token(token)
        >>> if user:
        ...     print(f"Authenticated user: {user.username}")
        >>> else:
        ...     print("Authentication failed")
    """
    # Decode the JWT token to get payload
    payload = decode_jwt_token(token)
    
    # Return None if token decoding failed
    if 'error' in payload:
        return None
        
    try:
        # Retrieve user from database using user ID from token
        user = User.objects.get(id=payload['user_id'])
        return user
        
    except User.DoesNotExist:
        # Return None if user doesn't exist in database
        return None