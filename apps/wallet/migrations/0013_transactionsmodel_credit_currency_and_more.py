# Generated by Django 4.2.5 on 2024-10-08 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0012_alter_transactionsmodel_db_rrn'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactionsmodel',
            name='credit_currency',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='transactionsmodel',
            name='debit_currency',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='transactionsmodel',
            name='rate',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
