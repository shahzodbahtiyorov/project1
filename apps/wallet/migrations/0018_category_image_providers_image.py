# Generated by Django 4.2.5 on 2024-10-22 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0017_remove_category_image_remove_providers_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='image/category'),
        ),
        migrations.AddField(
            model_name='providers',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='provider_images/'),
        ),
    ]
