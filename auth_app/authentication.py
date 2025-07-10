from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User
from .utils import decode_jwt_token

class JWTAuthentication(BaseAuthentication):
    """Custom JWT Authentication class"""

    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None

        try:
            prefix, token = auth_header.split(' ')
            if prefix.lower() != 'bearer':
                raise AuthenticationFailed('Invalid token prefix')

            payload = decode_jwt_token(token)
            if 'error' in payload:
                raise AuthenticationFailed(payload['error'])

            user = User.objects.get(id=payload['user_id'])
            return (user, token)

        except ValueError:
            raise AuthenticationFailed('Token format is invalid')
        except User.DoesNotExist:
            raise AuthenticationFailed('User not found')
        except Exception as e:
            raise AuthenticationFailed(f'Authentication failed: {str(e)}')