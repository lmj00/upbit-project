# Generated by Django 4.0 on 2023-03-30 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(max_length=36)),
                ('side', models.CharField(max_length=3)),
                ('ord_type', models.CharField(max_length=6)),
                ('price', models.IntegerField()),
                ('state', models.CharField(max_length=6)),
                ('market', models.CharField(max_length=10)),
                ('created_at', models.CharField(max_length=25)),
                ('volume', models.FloatField()),
                ('remaining_volume', models.FloatField()),
                ('reserved_fee', models.FloatField()),
                ('remaining_fee', models.FloatField()),
                ('paid_fee', models.FloatField()),
                ('locked', models.FloatField()),
                ('executed_volume', models.FloatField()),
                ('trades_count', models.FloatField()),
            ],
        ),
    ]
