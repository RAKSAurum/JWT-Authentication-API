"""
Django Admin Configuration Module

This module configures the Django admin interface for the auth_app application.
Currently uses Django's default User admin interface without customizations.

The module imports Django's built-in admin functionality and User model
to leverage the existing admin interface for user management.

Usage:
    This file is automatically loaded by Django when the admin interface
    is accessed at /admin/
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Using Django's default User admin interface
# No custom admin classes are currently defined
# The default UserAdmin provides comprehensive user management capabilities
# including user creation, editing, permissions, and group management