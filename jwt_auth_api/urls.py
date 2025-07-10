"""
Main URL Configuration Module for Django JWT Authentication API

This module defines the root URL patterns for the entire Django project.
It serves as the central routing configuration that maps URL paths to
their corresponding view functions and includes application-specific
URL patterns.

The URL configuration follows Django's URL routing conventions and
provides a clean, RESTful API structure for the JWT authentication
system.

URL Structure:
    /admin/          - Django admin interface
    /api/auth/       - JWT authentication endpoints

Dependencies:
    - Django URL routing system
    - Django admin interface
    - auth_app URL patterns

Author: [Your Name]
Created: [Date]
Version: 1.0.0
"""

from django.contrib import admin
from django.urls import path, include

# Main URL patterns for the Django project
# These patterns define the top-level routing structure
urlpatterns = [
    # Django Admin Interface
    # URL: /admin/
    # Provides access to Django's built-in admin interface
    # Requires superuser credentials for access
    path('admin/', admin.site.urls),
    
    # JWT Authentication API Endpoints
    # URL: /api/auth/
    # Includes all authentication-related endpoints from auth_app
    # Routes to: login/, verify/, validate/ endpoints
    path('api/auth/', include('auth_app.urls')),
]