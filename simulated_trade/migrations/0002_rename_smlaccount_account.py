# Generated by Django 4.0 on 2023-06-05 07:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simulated_trade', '0001_smlAccount'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='smlAccount',
            new_name='Account',
        ),
    ]