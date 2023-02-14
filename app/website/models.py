# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
class Website(models.Model):
    name = models.CharField(max_length=200,default="")
    url = models.CharField(max_length=200,default="")
    active = models.BooleanField(default=False)
    page = models.IntegerField(default=1)
    que= models.IntegerField(default=0)
    def __str__(self):
        return self.name + " / " + self.url