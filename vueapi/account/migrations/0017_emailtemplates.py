# Generated by Django 3.0 on 2020-01-25 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0016_job_account'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailTemplates',
            fields=[
                ('templateid', models.AutoField(primary_key=True, serialize=False)),
                ('subject', models.CharField(max_length=255)),
                ('body', models.TextField(blank=True)),
            ],
            options={
                'db_table': 'email_templates',
                'ordering': ['templateid'],
            },
        ),
    ]
