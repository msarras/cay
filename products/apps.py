from django.db import connection
from django.db.utils import OperationalError
from django.apps import apps, AppConfig
from django.core.management import call_command

import time

class ProductsConfig(AppConfig):
    name = 'products'

"""
    # don't use this for the moment since we don't often need to import the
    # initial data meant to seed the db. However, if used then a db health
    # check needs to be made since the django docker container would most
    # likely go up before the db container is ready to accept connections
    # but also the tailwind container needs python so timing needs to be
    # figured out
    def ready(self):
        # Check if the Product table is populated
        Product = apps.get_model('products', 'Product')

        print('Waiting for database...')
        db_conn = None
        while not db_conn:
            try:
                connection.ensure_connection()
                db_conn = True
            except OperationalError:
                print('Database unavailable, waiting 1 second...')
                time.sleep(1)

        print('Database available!')

        if not Product.objects.exists():  # Check if there are any products
            # If the table is empty, run the import command
            call_command('import_products')
"""
