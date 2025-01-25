# Generated by Django 5.0.7 on 2024-11-19 19:56

import datetime
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Basket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='BasketBasicFood',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('basket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='basic_foods', to='baskets.basket')),
                ('category', models.CharField(max_length=30, blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BasketPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(blank=True, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('basket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prices', to='baskets.basket')),
            ],
        ),
        migrations.CreateModel(
            name='WeeklyBasketItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week_of', models.DateField(default=django.utils.timezone.now)),
                ('valid_until', models.DateField(blank=True, null=True)),
                ('basket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='basket_items', to='baskets.basket')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
        ),
    ]
