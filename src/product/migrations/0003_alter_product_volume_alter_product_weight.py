# Generated by Django 5.2 on 2025-04-23 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_alter_product_volume_alter_product_weight_stock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='volume',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='product',
            name='weight',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
