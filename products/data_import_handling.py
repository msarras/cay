from products.resources import (
    ProductResource,
    ProductBasicFoodResource,
    ProductBrandResource,
    ProductPriceResource
)
from tablib import Dataset
import pandas as pd
import numpy as np


class DataImport:
    RESOURCE_MAP = {
        'products': (ProductResource, 'get_products_dataset'),
        'basic food categories': (ProductBasicFoodResource, 'get_categories_dataset'),
        'brands': (ProductBrandResource, 'get_brands_dataset'),
        'prices': (ProductPriceResource, 'get_prices_dataset'),
    }

    def __init__(self, file_path):
        self.file_path = file_path
        self.sheet = self.transform_products_sheet()
        self.resources = [(resource_class(), getattr(self, method_name)(), name)
                          for name, (resource_class, method_name) in self.RESOURCE_MAP.items()]

    def transform_products_sheet(self):
        xlsx = pd.ExcelFile(self.file_path)
        sheet = pd.read_excel(xlsx, 'Liste des prix (Luis)', header=2)

        # Define a common name derived from the product name
        sheet['common_name'] = sheet['ITEMS'].str.split().str[0].str.capitalize()

        # Rename columns
        rename_columns = {
            'ITEMS': 'name', 'common_name': 'common_name', 'BIO': 'organic',
            'OR.': 'origin', 'PRIX': 'price', 'Brand': 'brand_1',
            'Brand 2': 'brand_2', 'EMBALLAGE SECONDAIRE': 'secondary_packaging_unit',
            'EMBALLAGE PRIMAIRE': 'primary_packaging_unit',
            'UNITÉS X EMB.': 'units_by_packaging',
            'Preparé pour la liste du collectif': 'was_previously_ordered',
            'Categorie': 'category', 'Actuel Date Prix': 'date',
            'Commentaires': 'comments'
        }
        sheet.rename(columns=rename_columns, inplace=True)

        # Clean up the data
        sheet.replace('?', None, inplace=True)
        sheet.replace('nan', None, inplace=True)

        # Convert boolean columns
        sheet['organic'] = sheet['organic']\
            .replace({'BIO': True, np.nan: False}).astype(bool)
        sheet['was_previously_ordered'] = sheet['was_previously_ordered']\
            .replace({'OUI': True, 'NON': False}).astype(bool)

        # Replace pd.NA with None
        sheet = sheet.where(pd.notna(sheet), None)[list(rename_columns.values())]

        # Convert 'price' to float, handling None
        sheet['price'] = sheet['price']\
            .astype(float)\
            .where(pd.notna(sheet['price']), None)

        # Convert 'units_by_packaging' to int, handling None
        sheet['units_by_packaging'] = pd.to_numeric(sheet['units_by_packaging'], errors='coerce')\
            .fillna(0).astype(int)

        # Remove duplicated rows based on name
        sheet = sheet[~sheet.duplicated(subset='name')]

        # Coerce date column to date type
        sheet['date'] = pd.to_datetime(sheet['date'], errors='coerce')\
            .astype(object)\
            .fillna(pd.Timestamp('2024-01-01'))

        return sheet

    def get_products_dataset(self):
        return Dataset().load(self.sheet)

    def get_categories_dataset(self):
        categories = self.sheet[['name', 'category']]
        categories.loc[:, 'category'] = categories['category'].str.split(',')
        pivot_long_categories = categories.explode('category')
        pivot_long_categories['category'] = pivot_long_categories['category'].str.strip()
        return Dataset().load(pivot_long_categories)

    def get_brands_dataset(self):
        return Dataset().load(
            pd.melt(
                self.sheet,
                id_vars=['name'],
                value_vars=['brand_1', 'brand_2'],
                var_name='brand_type',
                value_name='brand'
            )[['name', 'brand']]\
                .dropna()\
                .drop_duplicates()\
                .sort_values(by='name')\
                .reset_index(drop=True)
        )

    def get_prices_dataset(self):
        return Dataset().load(self.sheet[['name', 'price', 'date']])

    def import_data(self):
        print(f'\n')
        for resource, data, name in self.resources:
            try:
                resource.import_data(data, dry_run=False, raise_errors=True)
                print(f'  Successfully imported {name}')
            except Exception as e:
                print(f'  {name.capitalize()} import error: {str(e)}')
