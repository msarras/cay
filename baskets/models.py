from django.db import models
from products.models import Product
from django.utils.translation import gettext_lazy as _


class Basket(models.Model):
    """
    A Basket represents a category of goods, e.g., fruits, vegetables,
    mushrooms, or whatever arbitrary category.
    """
    name = models.CharField(max_length=30, unique=True, verbose_name=_("name"))

    class Meta:
        verbose_name = _("basket")

    def __str__(self):
        return self.name


class BasketBasicFood(models.Model):
    """A BasicFood item that belongs to a specific Basket."""
    basket = models.ForeignKey(
        Basket, related_name='basic_foods', verbose_name=_("basket"),
        on_delete=models.CASCADE
    )
    category = models.CharField(
        max_length=30, blank=True, null=True, verbose_name=_("category")
    )

    class Meta:
        verbose_name = _("basket basic food")

    def __str__(self):
        return self.category


class BasketPrice(models.Model):
    """
    For a given Basket of goods, we want to assign a fixed weekly price/budget.
    """
    basket = models.ForeignKey(
        Basket, on_delete=models.CASCADE, related_name='prices',
        verbose_name=_("basket")
    )
    price = models.FloatField(blank=True, null=True, verbose_name=_("price"))
    date = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = _("basket price")
        verbose_name_plural = _("basket prices")

    def __str__(self):
        return f"Price of {self.basket.name} on {self.date}"


class WeeklyBasketItem(models.Model):
    """
    WeeklyBasketItems are the Products of a particular category (e.g., fruits,
    vegetables) that are selected at the beginning of the week on behalf of
    members, wherein members later choose Baskets based on whether they
    want/need the WeeklyBasketItems
    """
    basket = models.ForeignKey(
        Basket, on_delete=models.CASCADE, related_name='basket_items',
        verbose_name=_("basket")
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name=_("product")
    )
    week_of = models.DateField(
        blank=True, null=True, verbose_name=_("week of"))
    valid_until = models.DateField(
        blank=True, null=True, verbose_name=_("valid until")
    )

    class Meta:
        verbose_name = _("weekly basket item")

    def __str__(self):
        return(
            f"{self.product.name} in {self.basket.name} for week "
            f"ending {self.valid_until}"
        )
