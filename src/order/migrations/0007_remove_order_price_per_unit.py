# Generated by Django 5.2 on 2025-05-08 00:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_remove_order_product_remove_order_quantity_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='price_per_unit',
        ),
    ]
