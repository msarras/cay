from django.db import models
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    """
    An item sold by the distributor, often without consistent naming,
    packaging, etc.
    """
    name = models.CharField(max_length=255, verbose_name=_("name"))
    common_name = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("common name"))
    organic = models.BooleanField(default=False, blank=True, null=True, verbose_name=_("organic"))
    origin = models.CharField(max_length=30, blank=True, null=True, verbose_name=_("origin"))
    primary_packaging_unit = models.CharField(
            max_length=15, blank=True, null=True, verbose_name=_("primary packaging unit"))
    secondary_packaging_unit = models.CharField(
            max_length=15, blank=True, null=True, verbose_name=_("secondary packaging unit"))
    units_by_packaging = models.PositiveIntegerField(verbose_name=_("units per packaging"))
    was_previously_ordered = models.BooleanField(default=False, verbose_name=_("was previously ordered"))
    comments = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("comments"))

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        return self.name

    @property
    def latest_price(self):
        return self.product_prices.order_by('-date').first().price

    @property
    def brands(self):
        return self.product_brands

    @property
    def basic_foods(self):
        return self.basic_foods


class ProductBrand(models.Model):
    """
    Keep track of the various brands of Products offered by the distributor
    """
    product = models.ForeignKey(
        Product, related_name='product_brands',
        verbose_name=_("product"), on_delete=models.CASCADE
    )
    brand = models.CharField(
        max_length=255, blank=True, null=True, verbose_name=_("brand")
    )

    class Meta:
        verbose_name = _("product brand")

    def __str__(self):
        return self.brand


class ProductBasicFood(models.Model):
    """A ProductBasicFood item that belongs to a specific Basket."""
    product = models.ForeignKey(
        Product, related_name='basic_foods', on_delete=models.CASCADE,
        verbose_name=_("product")
    )
    category = models.CharField(
        max_length=30, blank=True, null=True, verbose_name=_("category")
    )

    class Meta:
        verbose_name = _("product basic food")

    def __str__(self):
        return self.category


class ProductPrice(models.Model):
    """
    Product prices at the distributor change daily based on supply & demand,
    keep track of those prices/date pairs
    """
    product = models.ForeignKey(
        Product, related_name='product_prices', verbose_name=_("product"),
        on_delete=models.CASCADE
    )
    price = models.FloatField(blank=True, null=True, verbose_name=_("price"))
    date = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = _("product price")

    def __str__(self):
        return f'{self.product.name} was {self.price} on {self.date}'
