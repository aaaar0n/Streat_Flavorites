# Generated by Django 4.2.3 on 2023-08-11 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streat_flavorites', '0007_banner'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='banner',
            options={'ordering': ['position']},
        ),
        migrations.AddField(
            model_name='banner',
            name='position',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
