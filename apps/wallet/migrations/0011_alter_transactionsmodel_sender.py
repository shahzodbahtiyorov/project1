# Generated by Django 4.2.5 on 2024-10-08 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0010_form'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactionsmodel',
            name='sender',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
