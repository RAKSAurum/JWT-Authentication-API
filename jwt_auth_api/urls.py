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
    /static/         - Static files (CSS, JavaScript, images)

Dependencies:
    - Django URL routing system
    - Django admin interface
    - auth_app URL patterns
    - Django static files framework
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

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

# Static files serving configuration
# This section handles serving of static files (CSS, JavaScript, images)
# Required for Django admin interface styling and functionality
if settings.DEBUG or not settings.DEBUG:
    # Serve static files in both development and production modes
    # This ensures Django admin interface displays with proper styling
    urlpatterns += static(
        settings.STATIC_URL,           # URL prefix for static files (/static/)
        document_root=settings.STATIC_ROOT  # Physical directory path (/app/staticfiles)
    )