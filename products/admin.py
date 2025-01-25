from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Product, ProductBasicFood, ProductBrand, ProductPrice
from .resources import (
    ProductResource,
    ProductBasicFoodResource,
    ProductBrandResource,
    ProductPriceResource
)


class ProductBrandInline(admin.TabularInline):
    model = ProductBrand
    extra = 1


class ProductBasicFoodInline(admin.TabularInline):
    model = ProductBasicFood
    extra = 1


class ProductPriceInline(admin.TabularInline):
    model = ProductPrice
    extra = 1


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    resource_class = ProductResource
    inlines = [ProductBasicFoodInline, ProductBrandInline, ProductPriceInline]
    list_display = (
        'name', 'common_name', 'organic', 'origin',
        'primary_packaging_unit', 'secondary_packaging_unit',
        'units_by_packaging', 'was_previously_ordered',
        'comments'
    )
    search_fields = list_display


@admin.register(ProductBrand)
class ProductBrandAdmin(ImportExportModelAdmin):
    resource_class = ProductBrandResource
    list_display = ('brand',)


@admin.register(ProductBasicFood)
class ProductBasicFoodAdmin(ImportExportModelAdmin):
    resource_class = ProductBasicFoodResource
    list_display = ('category',)


@admin.register(ProductPrice)
class ProductPriceAdmin(ImportExportModelAdmin):
    resource_class = ProductPriceResource
    list_display = ('product_name', 'price', 'date')
    search_fields = ['product__name']

    def product_name(self, obj):
        return obj.product.name

    product_name.short_description = 'Product Name'
