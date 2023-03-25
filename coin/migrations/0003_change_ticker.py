# Generated by Django 4.0 on 2023-03-20 00:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coin', '0002_ticker_english_name_ticker_korean_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticker',
            name='acc_trade_price_24h',
        ),
        migrations.RemoveField(
            model_name='ticker',
            name='change_rate',
        ),
        migrations.RemoveField(
            model_name='ticker',
            name='english_name',
        ),
        migrations.RemoveField(
            model_name='ticker',
            name='korean_name',
        ),
        migrations.RemoveField(
            model_name='ticker',
            name='market',
        ),
        migrations.RemoveField(
            model_name='ticker',
            name='signed_change_rate',
        ),
        migrations.RemoveField(
            model_name='ticker',
            name='trade_date_kst',
        ),
        migrations.RemoveField(
            model_name='ticker',
            name='trade_time_kst',
        ),
        migrations.AddField(
            model_name='ticker',
            name='acc_ask_volume',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='ticker',
            name='acc_bid_volume',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='ticker',
            name='ask_bid',
            field=models.CharField(default='', max_length=3),
        ),
        migrations.AddField(
            model_name='ticker',
            name='code',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AddField(
            model_name='ticker',
            name='market_state',
            field=models.CharField(default='', max_length=8),
        ),
        migrations.AddField(
            model_name='ticker',
            name='type',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AlterField(
            model_name='ticker',
            name='highest_52_week_date',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='ticker',
            name='lowest_52_week_date',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='ticker',
            name='timestamp',
            field=models.IntegerField(),
        ),
    ]