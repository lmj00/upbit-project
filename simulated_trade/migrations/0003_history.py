# Generated by Django 4.0 on 2023-06-05 08:04

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simulated_trade', '0002_rename_smlaccount_account'),
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('side', models.CharField(max_length=3)),
                ('market', models.CharField(max_length=20)),
                ('price', models.DecimalField(decimal_places=20, default=Decimal('0.0'), max_digits=40)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('volume', models.DecimalField(decimal_places=20, default=Decimal('0.0'), max_digits=60)),
                ('paid_fee', models.DecimalField(decimal_places=20, default=Decimal('0.0'), max_digits=40)),
            ],
        ),
    ]