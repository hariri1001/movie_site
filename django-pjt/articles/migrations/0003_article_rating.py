# Generated by Django 4.2.16 on 2024-11-20 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_article_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='rating',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=2, null=True),
        ),
    ]
