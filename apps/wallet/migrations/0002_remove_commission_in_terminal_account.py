# Generated by Django 4.2.5 on 2024-08-20 08:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commission',
            name='in_terminal_account',
        ),
    ]