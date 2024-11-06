from django.db import models
from super_app import settings


class Identification(models.Model):
    # code
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    status = models.IntegerField('Status', default=0)
    code = models.CharField('Code', max_length=128, null=True)
    access_token = models.TextField('Access Token')
    expires_in = models.IntegerField('Expires In', default=0)
    token_type = models.CharField('Token Type', max_length=255)
    scope = models.CharField('Scope', max_length=255, null=True)
    refresh_token = models.TextField('Refresh Token', null=True)
    comparison_value = models.CharField('Comparison Value', max_length=255, null=True)
    seria = models.CharField('Seria', max_length=255, null=True)
    pinfl = models.CharField('Pinfl', max_length=255, null=True)
    response = models.JSONField('Response', null=True)
    image = models.TextField('Person Image', null=True)
    must_refresh_token = models.DateTimeField(auto_now_add=False, null=True, editable=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} - {self.seria}'





