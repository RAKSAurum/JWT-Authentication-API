"""
Django Management Script

This is the main Django management script that provides a command-line interface
for administrative tasks. It serves as the entry point for running Django
management commands such as database migrations, running the development server,
creating superusers, and custom management commands.

The script automatically configures the Django environment and provides access
to all built-in and custom management commands defined in the project.

Common Usage Examples:
    python manage.py runserver              # Start development server
    python manage.py makemigrations         # Create new database migrations
    python manage.py migrate                # Apply database migrations
    python manage.py createsuperuser        # Create admin user
    python manage.py collectstatic          # Collect static files
    python manage.py wait_for_db            # Custom command to wait for database

Dependencies:
    - Django framework
    - Python 3.6+ (recommended 3.8+)
    - All project dependencies from requirements.txt
"""

import os
import sys

# Main execution block
# Only executes when script is run directly (not imported)
if __name__ == '__main__':
    # Set the Django settings module environment variable
    # This tells Django which settings configuration to use
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jwt_auth_api.settings')
    
    try:
        # Import Django's command-line management utility
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Provide helpful error message if Django is not installed
        # or virtual environment is not activated
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # Execute the management command with command-line arguments
    # sys.argv contains the command and its arguments
    execute_from_command_line(sys.argv)