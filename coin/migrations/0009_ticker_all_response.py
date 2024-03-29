# Generated by Django 4.0 on 2023-07-24 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coin', '0008_ticker_change_rate_ticker_signed_change_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticker',
            name='delisting_date',
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AddField(
            model_name='ticker',
            name='is_trading_suspended',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='ticker',
            name='market_warning',
            field=models.CharField(default='', max_length=7),
        ),
        migrations.AddField(
            model_name='ticker',
            name='stream_type',
            field=models.CharField(default='', max_length=8),
        ),
    ]
