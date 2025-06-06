# Generated by Django 5.2 on 2025-04-30 03:24

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0010_remove_product_wishlist_wishlist'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='wishlist',
            field=models.ManyToManyField(blank=True, related_name='wishlist_products', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Wishlist',
        ),
    ]
