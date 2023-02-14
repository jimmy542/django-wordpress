from django.db import models

# Create your models here.
class Wordpress(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=500)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    api_password = models.CharField(max_length=100,default="")
    page = models.IntegerField(default=1)
    tag_page = models.IntegerField(default=1)
    category_page = models.IntegerField(default=1)
    active = models.BooleanField(default=False)
    que= models.IntegerField(default=0)
    sync_status = models.CharField(max_length=10,default="nosync")