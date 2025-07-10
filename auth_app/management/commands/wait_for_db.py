"""
Django Management Command: Database Connection Waiter

This module provides a Django management command that waits for the database
to become available before proceeding. This is particularly useful in
containerized environments where the application container might start
before the database container is fully ready.

Usage:
    python manage.py wait_for_db
"""

import time
from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Django management command to wait for database availability.
    
    This command continuously attempts to connect to the default database
    until a successful connection is established. It's designed to handle
    scenarios where the application starts before the database service
    is fully operational.
    
    Attributes:
        help (str): Help text displayed when running --help
    """
    
    help = 'Wait for database to be ready'

    def handle(self, *args, **options):
        """
        Main command execution method.
        
        Continuously attempts to establish a database connection with a 1-second
        interval between attempts. Outputs status messages to stdout and exits
        when the database becomes available.
        
        Args:
            *args: Variable length argument list (unused)
            **options: Arbitrary keyword arguments from command line
            
        Returns:
            None
            
        Raises:
            OperationalError: Caught and handled during connection attempts
        """
        self.stdout.write('Waiting for database…')
        db_conn = None
        
        # Continuously attempt database connection until successful
        while not db_conn:
            try:
                # Attempt to get database connection and ensure it's active
                db_conn = connections['default']
                db_conn.ensure_connection()
            except OperationalError:
                # Log retry message and wait before next attempt
                self.stdout.write('Database unavailable, retrying in 1 second...')
                time.sleep(1)
        
        # Success message with Django's styling
        self.stdout.write(self.style.SUCCESS('Database available!'))