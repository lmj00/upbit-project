# Generated by Django 4.0 on 2023-03-26 02:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coin', '0003_change_ticker'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticker',
            name='acc_trade_price_24h',
            field=models.FloatField(null=True),
        ),
    ]
