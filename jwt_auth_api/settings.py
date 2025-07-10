"""
Django Project Settings Configuration Module

This module contains all configuration settings for the Django JWT Authentication API
project. It defines database connections, security settings, installed applications,
middleware configuration, and custom JWT authentication parameters.

The settings are designed for production use with environment variable configuration
using python-decouple for secure credential management. All sensitive information
is externalized through environment variables.

Key Features:
    - Environment-based configuration management
    - PostgreSQL database integration
    - JWT authentication configuration
    - Django REST Framework setup
    - Security and internationalization settings

Dependencies:
    - python-decouple for environment variable management
    - PostgreSQL database
    - Django REST Framework
"""

import os
from decouple import config
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# This provides the absolute path to the project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
# Secret key for cryptographic signing - loaded from environment variable
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
# Debug mode setting - defaults to False for production safety
DEBUG = config('DEBUG', default=False, cast=bool)

# Allowed hosts for the Django application
# Parsed from comma-separated environment variable
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')

# Application definition
# List of all Django applications in the project
INSTALLED_APPS = [
    # Django built-in applications
    'django.contrib.admin',        # Admin interface
    'django.contrib.auth',         # Authentication framework
    'django.contrib.contenttypes', # Content type framework
    'django.contrib.sessions',     # Session framework
    'django.contrib.messages',     # Messaging framework
    'django.contrib.staticfiles',  # Static file management
    
    # Third-party applications
    'rest_framework',              # Django REST Framework
    
    # Local applications
    'auth_app',                    # JWT authentication application
]

# Middleware configuration
# List of middleware classes processed in order for each request/response
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',      # Security enhancements
    'whitenoise.middleware.WhiteNoiseMiddleware',       # Static file serving
    'django.contrib.sessions.middleware.SessionMiddleware',  # Session management
    'django.middleware.common.CommonMiddleware',          # Common functionality
    'django.middleware.csrf.CsrfViewMiddleware',          # CSRF protection
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Authentication
    'django.contrib.messages.middleware.MessageMiddleware',  # Message framework
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Clickjacking protection
]

# Root URL configuration module
# Points to the main URL configuration file
ROOT_URLCONF = 'jwt_auth_api.urls'

# Template configuration
# Settings for Django's template engine
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],                    # Additional template directories
        'APP_DIRS': True,             # Look for templates in app directories
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI application configuration
# Points to the WSGI application callable
WSGI_APPLICATION = 'jwt_auth_api.wsgi.application'

# Database configuration
# PostgreSQL database settings with environment variable configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # PostgreSQL database engine
        'NAME': config('DB_NAME'),                  # Database name
        'USER': config('DB_USER'),                  # Database user
        'PASSWORD': config('DB_PASSWORD'),          # Database password
        'HOST': config('DB_HOST', default='db'),    # Database host (default: db for Docker)
        'PORT': config('DB_PORT', default='5432'),  # Database port
    }
}

# Password validation configuration
# List of password validators to enforce password security
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization configuration
# Language and timezone settings
LANGUAGE_CODE = 'en-us'      # Default language
TIME_ZONE = 'UTC'            # Default timezone
USE_I18N = True              # Enable internationalization
USE_L10N = True              # Enable localization
USE_TZ = True                # Enable timezone support

# Static files configuration (CSS, JavaScript, Images)
# Settings for serving static files in production
STATIC_URL = '/static/'                              # URL prefix for static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Directory for collected static files

# Use WhiteNoise storage backend for compression and caching
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Django REST Framework configuration
# Global settings for API functionality
REST_FRAMEWORK = {
    # Default authentication classes for all API endpoints
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'auth_app.authentication.JWTAuthentication',  # Custom JWT authentication
    ],
    
    # Default permission classes for all API endpoints
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',  # Require authentication by default
    ],
}

# JWT (JSON Web Token) Configuration
# Custom settings for JWT authentication implementation
JWT_SECRET_KEY = config('JWT_SECRET_KEY', default=SECRET_KEY)  # JWT signing key
JWT_ALGORITHM = 'HS256'                                       # JWT signing algorithm
JWT_EXPIRATION_DELTA = 3600                                   # Token expiration time (1 hour)