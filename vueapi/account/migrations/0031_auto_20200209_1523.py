# Generated by Django 3.0 on 2020-02-09 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0030_auto_20200209_1522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timesheet',
            name='pause_time',
            field=models.TimeField(null=True),
        ),
    ]
