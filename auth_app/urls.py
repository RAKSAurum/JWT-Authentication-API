"""
URL Configuration Module for Authentication App

This module defines the URL patterns for the auth_app application.
It maps URL paths to their corresponding view functions for JWT
authentication endpoints.

The URL patterns provide RESTful endpoints for:
- User login and token generation
- Token verification
- Token validation

All URLs are relative to the app's base URL as configured in the
main project's URL configuration.

Author: [Your Name]
Created: [Date]
Version: 1.0.0
"""

from django.urls import path
from . import views

# URL patterns for JWT authentication endpoints
# These patterns are included in the main project URLs with 'api/auth/' prefix
urlpatterns = [
    # POST /api/auth/login/
    # Endpoint for user authentication and JWT token generation
    # Accepts username/password and returns JWT token with expiration
    path('login/', views.login, name='login'),
    
    # POST /api/auth/verify/
    # Endpoint for JWT token verification
    # Accepts token and returns validation status
    path('verify/', views.verify_token, name='verify_token'),
    
    # GET /api/auth/validate/
    # Endpoint for JWT token validation with user info
    # Requires Authorization header and returns user details
    path('validate/', views.validate_token, name='validate_token'),
]