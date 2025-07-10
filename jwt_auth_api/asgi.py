"""
ASGI (Asynchronous Server Gateway Interface) Configuration Module

This module provides the ASGI application configuration for the Django project.
ASGI is the asynchronous successor to WSGI and enables Django to handle
asynchronous operations, WebSockets, and other advanced features.

The module configures the Django ASGI application with proper environment
settings and exports the application callable for ASGI servers like
Uvicorn, Daphne, or Hypercorn.

ASGI servers supported:
    - Uvicorn: uvicorn jwt_auth_api.asgi:application
    - Daphne: daphne jwt_auth_api.asgi:application
    - Hypercorn: hypercorn jwt_auth_api.asgi:application

Dependencies:
    - Django (django.core.asgi)
    - Python 3.7+ (for ASGI support)
"""

import os
from django.core.asgi import get_asgi_application

# Set the Django settings module environment variable
# This must be set before importing Django components
# Points to the main settings configuration file
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jwt_auth_api.settings')

# Create and configure the ASGI application
# This callable is used by ASGI servers to handle requests
# The application handles both HTTP and WebSocket protocols
application = get_asgi_application()