# Generated by Django 4.2.5 on 2024-11-04 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0039_category_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cardmodel',
            name='blocked',
            field=models.BooleanField(default=True),
        ),
    ]
