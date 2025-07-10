import jwt
import uuid
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User

def generate_jwt_token(user):
    """Generate JWT token for a user with unique identifier"""
    now = timezone.now()
    payload = {
        'user_id': user.id,
        'username': user.username,
        'exp': now + timedelta(seconds=settings.JWT_EXPIRATION_DELTA),
        'iat': now,
        'jti': str(uuid.uuid4()),
    }
    
    token = jwt.encode(payload, settings.JWT_SECRET_KEY, 
                      algorithm=settings.JWT_ALGORITHM)
    return token

def decode_jwt_token(token):
    """Decode JWT token and return payload"""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, 
                           algorithms=[settings.JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return {'error': 'Token has expired'}
    except jwt.InvalidTokenError:
        return {'error': 'Invalid token'}
    except Exception as e:
        return {'error': f'Token decode error: {str(e)}'}

def get_user_from_token(token):
    """Get user from JWT token"""
    payload = decode_jwt_token(token)
    if 'error' in payload:
        return None
    
    try:
        user = User.objects.get(id=payload['user_id'])
        return user
    except User.DoesNotExist:
        return None