# basket/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Basket, BasketItem
from products.models import Product

def add_to_basket(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    basket, created = Basket.objects.get_or_create(user=request.user)

    basket_item, created = BasketItem.objects.get_or_create(basket=basket, product=product)
    if not created:
        basket_item.quantity += 1  # Increment quantity if already in basket
    basket_item.save
