# Generated by Django 4.2.3 on 2023-08-08 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streat_flavorites', '0002_cart_cartitem_cart_items_cart_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='likes',
            field=models.PositiveIntegerField(default=0),
        ),
    ]