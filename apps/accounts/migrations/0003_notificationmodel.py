# Generated by Django 4.2.5 on 2024-10-30 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_account_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotificationModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(blank=True, max_length=128, null=True)),
                ('is_active', models.BooleanField(blank=True, default=True, null=True)),
            ],
        ),
    ]