from django.db import models

# Create your models here.
class WordpressCategory(models.Model):
    category_name = models.TextField(default='no category_name name')
    website_name = models.TextField(default='no website')
    detail = models.TextField(default='no detail')
    category_wordpress_id = models.CharField(max_length=140, default='noid')
    wordpress_website = models.TextField(default='nowebsite')
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.category_name