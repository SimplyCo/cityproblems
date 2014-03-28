from django.db import models


class SiteParameters(models.Model):
    key = models.CharField(max_length=50)
    value = models.CharField(max_length=100)
    description = models.CharField(max_length=200)