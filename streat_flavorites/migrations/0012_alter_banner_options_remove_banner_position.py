# Generated by Django 4.2.3 on 2023-08-11 04:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('streat_flavorites', '0011_alter_banner_options_banner_position'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='banner',
            options={},
        ),
        migrations.RemoveField(
            model_name='banner',
            name='position',
        ),
    ]
