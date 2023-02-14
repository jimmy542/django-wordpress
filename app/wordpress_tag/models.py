from django.db import models




# Create your models here.
class WordPressTag(models.Model):
    website_name =  models.TextField(default='no website')
    tag_name = models.CharField(max_length=100)
    wordpress_website = models.TextField(default='nowebsite')
    wordpress_tag_id = models.CharField(max_length=100,default="noid")
    sync_status = models.CharField(max_length=10,default="nosync")
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.tag_name



