from django.db import models


class Category(models.Model):
    """Category model"""
    title_ru = models.CharField(max_length=255)
    title_uz = models.CharField(max_length=255)
    is_subcategory = models.BooleanField(default=False)
    category_id = models.IntegerField(unique=True)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return self.title_uz


class Providers(models.Model):
    """Providers model"""
    title = models.CharField(max_length=255)
    title_short = models.CharField(max_length=255)
    provider_id = models.IntegerField()
    category_id = models.IntegerField()


    def __str__(self):
        return self.title
