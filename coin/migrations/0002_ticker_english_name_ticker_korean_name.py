# Generated by Django 4.0 on 2023-03-17 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coin', '0001_ticker'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticker',
            name='english_name',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='ticker',
            name='korean_name',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
