# Generated by Django 3.0 on 2020-01-25 23:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0017_emailtemplates'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='invoice_type',
            field=models.CharField(default='Mowing', max_length=255),
            preserve_default=False,
        ),
    ]