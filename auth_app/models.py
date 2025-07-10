"""
Django Models Module for Authentication App

This module defines the database models for the auth_app application.
Currently, the application uses Django's built-in User model from
django.contrib.auth.models and does not define custom models.

The built-in User model provides comprehensive user management
functionality including authentication, permissions, and user profiles.

For future extensions, custom user models or related models can be
defined in this module following Django's model conventions.
"""

from django.db import models

# Currently using Django's built-in User model
# No custom models are defined at this time
#
# Future model definitions would follow this pattern:
#
# class CustomUserProfile(models.Model):
#     """
#     Extended user profile model for additional user information.
#     """
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     # Additional fields would be defined here
#
# class APIKey(models.Model):
#     """
#     API key model for alternative authentication methods.
#     """
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     # API key fields would be defined here
