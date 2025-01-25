from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget
from .models import Product, ProductBasicFood, ProductBrand, ProductPrice


class ProductResource(resources.ModelResource):
    brands = fields.Field(
        column_name='brand',
        attribute='product_brands',
        widget=ManyToManyWidget(ProductBrand, field='name')
    )
    basic_food = fields.Field(
        column_name='basic_food',
        attribute='product_basic_food',
        widget=ForeignKeyWidget(ProductBasicFood, field='name')
    )
    price = fields.Field(
        column_name='price',
        attribute='product_prices',
        widget=ForeignKeyWidget(ProductPrice, field='price')
    )
    date = fields.Field(
        column_name='date',
        attribute='date',
        widget=ForeignKeyWidget(ProductPrice, field='date')
    )

    class Meta:
        model = Product
        skip_unchanged = True
        import_id_fields = ['name']
        fields = (
            'name', 'common_name', 'organic', 'origin',
            'primary_packaging_unit', 'secondary_packaging_unit',
            'units_by_packaging', 'was_previously_ordered',
            'comments'
        )


class ProductBasicFoodResource(resources.ModelResource):
    product = fields.Field(
        column_name='name',
        attribute='product',
        widget=ForeignKeyWidget(Product, 'name')
    )
    category = fields.Field(column_name='category', attribute='category')

    class Meta:
        model = ProductBasicFood
        skip_unchanged = True
        import_id_fields = ['product', 'category']
        fields = ('product', 'category')


class ProductBrandResource(resources.ModelResource):
    product = fields.Field(
        column_name='name',
        attribute='product',
        widget=ForeignKeyWidget(Product, 'name')
    )
    brand = fields.Field(column_name='brand', attribute='brand')

    class Meta:
        model = ProductBrand
        skip_unchanged = True
        import_id_fields = ['product', 'brand']
        fields = ('product', 'brand')


class ProductPriceResource(resources.ModelResource):
    product = fields.Field(
        column_name='name',
        attribute='product',
        widget=ForeignKeyWidget(Product, 'name')
    )
    price = fields.Field(column_name='price', attribute='price')
    date = fields.Field(column_name='date', attribute='date')

    class Meta:
        model = ProductPrice
        skip_unchanged = True
        import_id_fields = ['product', 'price', 'date']
        fields = ('product', 'price', 'date')
