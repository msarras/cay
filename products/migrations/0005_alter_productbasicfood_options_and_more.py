# Generated by Django 5.0.7 on 2025-01-22 15:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_alter_product_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productbasicfood',
            options={'verbose_name': 'product basic food'},
        ),
        migrations.AlterModelOptions(
            name='productbrand',
            options={'verbose_name': 'product brand'},
        ),
        migrations.AlterModelOptions(
            name='productprice',
            options={'verbose_name': 'product price'},
        ),
        migrations.AlterField(
            model_name='product',
            name='comments',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='comments'),
        ),
        migrations.AlterField(
            model_name='product',
            name='common_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='common name'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=255, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='product',
            name='organic',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='organic'),
        ),
        migrations.AlterField(
            model_name='product',
            name='origin',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='origin'),
        ),
        migrations.AlterField(
            model_name='product',
            name='primary_packaging_unit',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='primary packaging unit'),
        ),
        migrations.AlterField(
            model_name='product',
            name='secondary_packaging_unit',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='secondary packaging unit'),
        ),
        migrations.AlterField(
            model_name='product',
            name='units_by_packaging',
            field=models.PositiveIntegerField(verbose_name='units per packaging'),
        ),
        migrations.AlterField(
            model_name='product',
            name='was_previously_ordered',
            field=models.BooleanField(default=False, verbose_name='was previously ordered'),
        ),
        migrations.AlterField(
            model_name='productbasicfood',
            name='category',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='category'),
        ),
        migrations.AlterField(
            model_name='productbasicfood',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='basic_foods', to='products.product', verbose_name='product'),
        ),
        migrations.AlterField(
            model_name='productbrand',
            name='brand',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='brand'),
        ),
        migrations.AlterField(
            model_name='productbrand',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_brands', to='products.product', verbose_name='product'),
        ),
        migrations.AlterField(
            model_name='productprice',
            name='price',
            field=models.FloatField(blank=True, null=True, verbose_name='price'),
        ),
        migrations.AlterField(
            model_name='productprice',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_prices', to='products.product', verbose_name='product'),
        ),
    ]
