# Generated by Django 4.0.6 on 2023-08-25 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_market_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='market',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]
