# Generated by Django 4.2.5 on 2024-10-08 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0014_transactionsmodel_commision'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactionsmodel',
            name='cr_currency',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='transactionsmodel',
            name='db_currency',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]