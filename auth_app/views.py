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
    POST /api/auth/login/
    Takes {"username": "user", "password": "pass"}
    Returns JWT token and expiry time
    """
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({
            'error': 'Username and password are required'
        }, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)
    if user:
        token = generate_jwt_token(user)
        expires = timezone.now() + timedelta(seconds=settings.JWT_EXPIRATION_DELTA)

        return Response({
            'token': token,
            'expires': expires.isoformat()
        }, status=status.HTTP_200_OK)

    return Response({
        'error': 'Invalid credentials'
    }, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_token(request):
    """
    POST /api/auth/verify/
    Takes {"token": "jwt_token"}
    Returns token validation status
    """
    token = request.data.get('token')

    if not token:
        return Response({
            'error': 'Token is required'
        }, status=status.HTTP_400_BAD_REQUEST)

    payload = decode_jwt_token(token)
    if 'error' in payload:
        return Response({
            'valid': False,
            'message': payload['error']
        }, status=status.HTTP_401_UNAUTHORIZED)

    return Response({
        'valid': True,
        'message': 'Token is valid'
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def validate_token(request):
    """
    GET /api/auth/validate/
    Requires JWT in Authorization header
    Returns validity, username, and expiry timestamp
    """
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return Response({
            'error': 'Authorization header is required'
        }, status=status.HTTP_401_UNAUTHORIZED)

    try:
        prefix, token = auth_header.split(' ')
        payload = decode_jwt_token(token)

        if 'error' in payload:
            return Response({
                'valid': False,
                'message': payload['error']
            }, status=status.HTTP_401_UNAUTHORIZED)

        expires = timezone.datetime.fromtimestamp(payload['exp'], tz=timezone.utc)

        return Response({
            'valid': True,
            'user': request.user.username,
            'expires': expires.isoformat()
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            'error': f'Token validation failed: {str(e)}'
        }, status=status.HTTP_401_UNAUTHORIZED)