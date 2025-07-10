"""
Django REST Framework Views Module for JWT Authentication

This module implements the API endpoints for JWT authentication functionality
including user login, token verification, and token validation. All views
are built using Django REST Framework decorators and provide RESTful
authentication services.

The module provides three main endpoints:
- POST /api/auth/login/ - User authentication and token generation
- POST /api/auth/verify/ - Token verification
- GET /api/auth/validate/ - Token validation with user information

Dependencies:
    - Django REST Framework
    - Django authentication system
    - Custom JWT utilities from utils module
"""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .utils import generate_jwt_token, decode_jwt_token
from datetime import timedelta
from django.utils import timezone
from django.conf import settings


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """
    Authenticate user and generate JWT token.
    
    This endpoint handles user authentication by validating credentials
    and returning a JWT token with expiration information upon successful
    authentication. The endpoint accepts username and password via POST
    request body.
    
    URL: POST /api/auth/login/
    
    Request Body:
        {
            "username": "string",  # Required: User's username
            "password": "string"   # Required: User's password
        }
    
    Response (Success - 200):
        {
            "token": "jwt_token_string",
            "expires": "ISO_datetime_string"
        }
    
    Response (Error - 400):
        {
            "error": "Username and password are required"
        }
    
    Response (Error - 401):
        {
            "error": "Invalid credentials"
        }
    
    Args:
        request (HttpRequest): Django request object containing user credentials
        
    Returns:
        Response: DRF Response object with token data or error message
        
    Security Notes:
        - Uses Django's authenticate() function for secure credential validation
        - Strips whitespace from username to prevent common input errors
        - Returns generic error message to prevent username enumeration
    """
    # Extract and sanitize user credentials from request body
    username = request.data.get('username', '').strip()
    password = request.data.get('password', '')

    # Validate that both username and password are provided
    if not username or not password:
        return Response({
            'error': 'Username and password are required'
        }, status=status.HTTP_400_BAD_REQUEST)

    # Authenticate user using Django's built-in authentication
    user = authenticate(username=username, password=password)
    
    if user:
        # Generate JWT token for authenticated user
        token = generate_jwt_token(user)
        
        # Calculate token expiration time
        expires = timezone.now() + timedelta(seconds=settings.JWT_EXPIRATION_DELTA)

        # Return successful authentication response
        return Response({
            'token': token,
            'expires': expires.isoformat()
        }, status=status.HTTP_200_OK)

    # Return generic error message for invalid credentials
    return Response({
        'error': 'Invalid credentials'
    }, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_token(request):
    """
    Verify the validity of a JWT token.
    
    This endpoint validates a JWT token without requiring authentication.
    It checks token signature, expiration, and format validity. Useful
    for client-side token validation and debugging.
    
    URL: POST /api/auth/verify/
    
    Request Body:
        {
            "token": "jwt_token_string"  # Required: JWT token to verify
        }
    
    Response (Success - 200):
        {
            "valid": true,
            "message": "Token is valid"
        }
    
    Response (Error - 400):
        {
            "error": "Token is required"
        }
    
    Response (Error - 401):
        {
            "valid": false,
            "message": "Token error message"
        }
    
    Args:
        request (HttpRequest): Django request object containing JWT token
        
    Returns:
        Response: DRF Response object with validation status
        
    Use Cases:
        - Client-side token validation before API calls
        - Token debugging and troubleshooting
        - Integration testing of JWT tokens
    """
    # Extract token from request body
    token = request.data.get('token')

    # Validate that token is provided
    if not token:
        return Response({
            'error': 'Token is required'
        }, status=status.HTTP_400_BAD_REQUEST)

    # Decode and validate the JWT token
    payload = decode_jwt_token(token)
    
    # Check if token decoding resulted in an error
    if 'error' in payload:
        return Response({
            'valid': False,
            'message': payload['error']
        }, status=status.HTTP_401_UNAUTHORIZED)

    # Return success response for valid token
    return Response({
        'valid': True,
        'message': 'Token is valid'
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def validate_token(request):
    """
    Validate JWT token and return user information.
    
    This endpoint requires a valid JWT token in the Authorization header
    and returns detailed information about the token including user data
    and expiration time. This endpoint uses the custom JWT authentication
    backend to validate the token.
    
    URL: GET /api/auth/validate/
    
    Headers:
        Authorization: Bearer <jwt_token>  # Required: JWT token
    
    Response (Success - 200):
        {
            "valid": true,
            "user": "username",
            "expires": "ISO_datetime_string"
        }
    
    Response (Error - 401):
        {
            "error": "Authorization header is required"
        }
        OR
        {
            "valid": false,
            "message": "Token error message"
        }
        OR
        {
            "error": "Token validation failed: error_details"
        }
    
    Args:
        request (HttpRequest): Django request object with Authorization header
        
    Returns:
        Response: DRF Response object with user data or error message
        
    Notes:
        - Requires IsAuthenticated permission (handled by JWT middleware)
        - Provides detailed token information for authenticated requests
        - Useful for user session management and token status checking
    """
    # Extract Authorization header from request
    auth_header = request.headers.get('Authorization')
    
    # Validate that Authorization header is present
    if not auth_header:
        return Response({
            'error': 'Authorization header is required'
        }, status=status.HTTP_401_UNAUTHORIZED)

    try:
        # Parse Authorization header format: "Bearer <token>"
        prefix, token = auth_header.split(' ')
        
        # Decode the JWT token to get payload information
        payload = decode_jwt_token(token)

        # Check if token decoding resulted in an error
        if 'error' in payload:
            return Response({
                'valid': False,
                'message': payload['error']
            }, status=status.HTTP_401_UNAUTHORIZED)

        # Convert expiration timestamp to datetime object
        expires = timezone.datetime.fromtimestamp(payload['exp'], tz=timezone.utc)

        # Return success response with user information
        return Response({
            'valid': True,
            'user': request.user.username,
            'expires': expires.isoformat()
        }, status=status.HTTP_200_OK)

    except Exception as e:
        # Handle any unexpected errors during token validation
        return Response({
            'error': f'Token validation failed: {str(e)}'
        }, status=status.HTTP_401_UNAUTHORIZED)