# Generated by Django 5.2 on 2025-04-29 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(default='default_profile.png', upload_to='profile_pictures/'),
        ),
    ]
