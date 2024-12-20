# Generated by Django 4.2.5 on 2024-10-25 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0023_alter_transactionsmodel_payment_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactionsmodel',
            name='payment_type',
            field=models.CharField(choices=[(0, 'UZCARD to UZCARD'), (1, 'UZCARD to HUMO'), (2, 'HUMO to UZCARD'), (3, 'HUMO to HUMO'), (4, 'UZCARD to PAYNET'), (5, 'HUMO to PAYNET'), (6, 'RF to UZB'), (7, 'UZB to RF')], default='card', help_text='Choose the type of payment, either card payment or oplata.', max_length=10),
        ),
    ]
