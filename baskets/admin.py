from django.contrib import admin
from .models import Basket, BasketBasicFood, BasketPrice, WeeklyBasketItem


class BasketPriceInline(admin.TabularInline):
    model = BasketPrice
    extra = 1


class BasketBasicFoodInline(admin.TabularInline):
    model = BasketBasicFood
    extra = 1


class WeeklyBasketItemInline(admin.TabularInline):
    model = WeeklyBasketItem
    extra = 1


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    inlines = [BasketPriceInline, BasketBasicFoodInline, WeeklyBasketItemInline]


@admin.register(BasketBasicFood)
class BasketBasicFoodAdmin(admin.ModelAdmin):
    list_display = ('basket', 'category')
    search_fields = ('basket', 'category')
    list_filter = ('basket',)


@admin.register(BasketPrice)
class BasketPriceAdmin(admin.ModelAdmin):
    list_display = ('basket', 'price', 'date')
    search_fields = ('basket__name',)
    list_filter = ('date',)
    date_hierarchy = 'date'


@admin.register(WeeklyBasketItem)
class WeeklyBasketItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'basket', 'week_of', 'valid_until')
    search_fields = ('product__name', 'basket__name', 'week_of', 'valid_until')
    list_filter = ('week_of', 'basket')
