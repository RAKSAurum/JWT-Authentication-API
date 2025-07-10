"""
WSGI (Web Server Gateway Interface) Configuration Module

This module provides the WSGI application configuration for the Django project.
WSGI is the standard interface between web servers and Python web applications,
enabling deployment with various web servers like Apache, Nginx with uWSGI,
or Gunicorn.

The module configures the Django WSGI application with proper environment
settings and exports the application callable for WSGI servers.

WSGI servers supported:
    - Gunicorn: gunicorn jwt_auth_api.wsgi:application
    - uWSGI: uwsgi --module jwt_auth_api.wsgi:application
    - Apache with mod_wsgi
    - Nginx with uWSGI

Dependencies:
    - Django (django.core.wsgi)
    - Compatible WSGI server

Author: [Your Name]
Created: [Date]
Version: 1.0.0
"""

import os
from django.core.wsgi import get_wsgi_application

# Set the Django settings module environment variable
# This must be set before importing Django components
# Points to the main settings configuration file
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jwt_auth_api.settings')

# Create and configure the WSGI application
# This callable is used by WSGI servers to handle HTTP requests
# The application handles the request/response cycle
application = get_wsgi_application()