import time
from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Wait for database to be ready'

    def handle(self, *args, **options):
        self.stdout.write('Waiting for database…')
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
                db_conn.ensure_connection()
            except OperationalError:
                self.stdout.write('Database unavailable, retrying in 1 second...')
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('Database available!'))