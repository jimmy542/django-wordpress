from django.db import models

# Create your models here.
from wordpress_category.models import WordpressCategory
from wordpress_tag.models import WordPressTag


class WordpressPost(models.Model):
    website_name = models.TextField(blank=True)
    wordpress_post_id = models.CharField(max_length=100,default='noid')
    wordpress_website = models.TextField(default='no website')
    detail = models.TextField(max_length=100,default='detail')
    wordpress_content = models.TextField(blank=True)
    wordpress_title = models.TextField(max_length=100,default='notitle')
    active = models.BooleanField(default=False)
    wordpress_status_post = models.TextField(blank=True)
    iframe = models.TextField(default='no iframe')
    focus_keyword = models.TextField(blank=True)
    description_keyword = models.TextField(blank=True)
    tag =  models.ManyToManyField(WordPressTag,default=None)
    category = models.ManyToManyField(WordpressCategory,default=None)

    def __str__(self):
        return self.wordpress_title