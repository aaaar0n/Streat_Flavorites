# Generated by Django 4.2.3 on 2023-08-11 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streat_flavorites', '0008_alter_banner_options_banner_position'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='url',
            field=models.URLField(blank=True),
        ),
    ]
