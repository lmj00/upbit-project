from django.db import models

# Create your models here.
class smlAccount(models.Model):
    currency = models.CharField(max_length=20)
    balance = models.FloatField()
    avg_buy_price = models.FloatField()
    unit_currency = models.CharField(max_length=5)