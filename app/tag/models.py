from django.db import models
from django.contrib import admin
# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=200)
    detail = models.TextField()
    tag_wordpress_id = models.CharField(max_length=140, default='noid')
    tag_django_id = models.CharField(max_length=140, default='noid')
    website = models.CharField(max_length=200)
    active = models.BooleanField(default=False)
    def __str__(self):
        return self.name + " / " + self.detail
