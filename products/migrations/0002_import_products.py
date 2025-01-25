from django.db import migrations
from django.conf import settings
from products.data_import_handling import DataImport


def import_products(apps, schema_editor):
    file_path = settings.BASE_DIR / 'data/collective-excel-template.xlsx'
    data_importer = DataImport(file_path)
    data_importer.import_data()


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(import_products),
    ]
