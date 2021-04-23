import time
from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        cnx= None
        self.stdout.write('waiting for db')

        while not cnx:
            try:
                cnx= connections['default']
            except OperationalError:
                self.stdout.write('Unavailable, waiting 1S')
                time.sleep(1)
        
        self.stdout.write(self.style.SUCCESS("Connection successful"))