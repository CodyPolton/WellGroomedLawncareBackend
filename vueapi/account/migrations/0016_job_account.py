# Generated by Django 3.0 on 2020-01-24 04:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0015_job_invoiceid'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='account',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='account.Account'),
            preserve_default=False,
        ),
    ]
