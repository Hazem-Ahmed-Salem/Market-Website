# Generated by Django 5.2 on 2025-05-10 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_alter_productcomplaint_order_number_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='technicalcomplaint',
            name='issue_description',
        ),
        migrations.AddField(
            model_name='technicalcomplaint',
            name='complaint_description',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='technicalcomplaint',
            name='issue_type',
            field=models.CharField(choices=[('website', 'Website Problem'), ('app', 'Mobile App Issue'), ('payment', 'Payment System Error'), ('account', 'Account Access Problem'), ('checkout', 'Checkout Process Issue'), ('other', 'Other Technical Issue')], default='website', max_length=100),
        ),
    ]
