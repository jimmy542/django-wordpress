# -*- coding: utf-8 -*-
from django.db import models
import tagulous.models
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200,unique=True)
    detail = models.TextField(default='')
    category_wordpress_id = models.CharField(max_length=140, default='noid')
    category_django_id = models.CharField(max_length=140, default='noid')
    website = models.CharField(max_length=200)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name + " / " + self.detail