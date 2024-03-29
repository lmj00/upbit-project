from django.db import models
from decimal import Decimal

# Create your models here.
class Account(models.Model):
    currency = models.CharField(max_length=20)
    balance = models.DecimalField(max_digits=40, decimal_places=20, default=Decimal('0.0'))
    avg_buy_price = models.DecimalField(max_digits=40, decimal_places=20, default=Decimal('0.0'))
    unit_currency = models.CharField(max_length=5)


class History(models.Model):
    side = models.CharField(max_length=3)
    market = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=40, decimal_places=20, default=Decimal('0.0'))
    created_at = models.DateTimeField(auto_now_add=True)
    volume = models.DecimalField(max_digits=60, decimal_places=20, default=Decimal('0.0'))
    paid_fee = models.DecimalField(max_digits=40, decimal_places=20, default=Decimal('0.0'))


class Bookmark(models.Model):
    market = models.CharField(max_length=20)