# Generated by Django 4.2.5 on 2024-10-31 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0036_alter_transactionsmodel_payment_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactionsmodel',
            name='payment_type',
            field=models.IntegerField(default=0),
        ),
    ]
