# Generated by Django 3.0 on 2020-01-14 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_auto_20200114_0935'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='invoiceid',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
