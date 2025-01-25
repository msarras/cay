from django.db import migrations
from baskets.constants import BASKETS_DATA

from tasks.utils import get_end_of_week


def seed_baskets(apps, schema_editor):
    Basket = apps.get_model('baskets', 'Basket')
    BasketBasicFood = apps.get_model('baskets', 'BasketBasicFood')
    BasketPrice = apps.get_model('baskets', 'BasketPrice')
    WeeklyBasketItem = apps.get_model('baskets', 'WeeklyBasketItem')
    Product = apps.get_model('products', 'Product')

    for basket_data in BASKETS_DATA:
        # Create the Basket instance
        basket, created = Basket.objects.get_or_create(name=basket_data['name'])
        for basic_food_category in basket_data['category']:
            basket_food_category, created = BasketBasicFood.objects.get_or_create(basket=basket, category=basic_food_category)


        for entry in basket_data['entries']:
            # Create the BasketPrice instance if it doesn't exist
            basket_price, created = BasketPrice.objects.get_or_create(
                basket=basket,
                price=entry['price'],
                date=entry['date']
            )

            # Add products to the basket
            for product_name in entry['products']:
                # Get or create the Product instance by name
                product, created = Product.objects.get_or_create(name=product_name)

                # Create a WeeklyBasketItem instance to link the product to the basket
                WeeklyBasketItem.objects.get_or_create(
                    basket=basket,
                    product=product,
                    valid_until=get_end_of_week()
                )


class Migration(migrations.Migration):

    dependencies = [
        ('baskets', '0001_initial'),
        ('products', '0002_import_products'),
    ]

    operations = [
        migrations.RunPython(seed_baskets),
    ]
