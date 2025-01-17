# Generated by Django 3.0 on 2020-01-03 13:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobExpenseType',
            fields=[
                ('job_expense_typeid', models.AutoField(primary_key=True, serialize=False)),
                ('job_expense_type', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'job_expense_types',
                'ordering': ['job_expense_typeid'],
            },
        ),
        migrations.AlterField(
            model_name='account',
            name='email',
            field=models.EmailField(blank=True, max_length=255),
        ),
        migrations.CreateModel(
            name='JobExpense',
            fields=[
                ('job_expenseid', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('expense_type', models.CharField(max_length=255)),
                ('date_purchased', models.DateTimeField(null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Job')),
            ],
            options={
                'db_table': 'job_expense',
                'ordering': ['job_expenseid'],
            },
        ),
    ]
