# Generated by Django 3.0 on 2020-02-09 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0029_auto_20200209_1126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timesheet',
            name='end_time',
            field=models.TimeField(null=True),
        ),
    ]