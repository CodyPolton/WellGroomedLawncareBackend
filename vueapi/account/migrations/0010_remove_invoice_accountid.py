# Generated by Django 3.0 on 2020-01-13 00:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_auto_20200112_1843'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='accountid',
        ),
    ]