# Generated by Django 4.2.5 on 2024-09-21 15:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wallet', '0008_remove_transactionsmodel_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Identification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(default=0, verbose_name='Status')),
                ('code', models.CharField(max_length=128, null=True, verbose_name='Code')),
                ('access_token', models.TextField(verbose_name='Access Token')),
                ('expires_in', models.IntegerField(default=0, verbose_name='Expires In')),
                ('token_type', models.CharField(max_length=255, verbose_name='Token Type')),
                ('scope', models.CharField(max_length=255, null=True, verbose_name='Scope')),
                ('refresh_token', models.TextField(null=True, verbose_name='Refresh Token')),
                ('comparison_value', models.CharField(max_length=255, null=True, verbose_name='Comparison Value')),
                ('seria', models.CharField(max_length=255, null=True, verbose_name='Seria')),
                ('pinfl', models.CharField(max_length=255, null=True, verbose_name='Pinfl')),
                ('response', models.JSONField(null=True, verbose_name='Response')),
                ('image', models.TextField(null=True, verbose_name='Person Image')),
                ('must_refresh_token', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]