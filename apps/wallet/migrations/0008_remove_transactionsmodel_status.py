# Generated by Django 4.2.5 on 2024-09-17 09:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0007_transactionsmodel_payment_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transactionsmodel',
            name='status',
        ),
    ]