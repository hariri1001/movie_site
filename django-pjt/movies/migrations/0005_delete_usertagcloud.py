# Generated by Django 4.2.16 on 2024-11-21 13:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0004_usertagcloud'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserTagCloud',
        ),
    ]
