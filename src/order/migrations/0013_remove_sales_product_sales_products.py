# Generated by Django 5.2 on 2025-05-12 02:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0012_remove_sales_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sales',
            name='product',
        ),
        migrations.AddField(
            model_name='sales',
            name='products',
            field=models.JSONField(default=list),
        ),
    ]
