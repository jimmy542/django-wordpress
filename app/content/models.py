from django.db import models
import tagulous.models

class Cate(tagulous.models.TagModel):
    class TagMeta:
        force_lowercase = True

class TagData(tagulous.models.TagModel):
    class TagMeta:
        force_lowercase = True

class Content(models.Model):
    name = models.CharField(max_length=200)
    detail = models.TextField()
    post_wordpress_id = models.CharField(max_length=140, default='noid')
    wordpress_content = models.TextField(blank=True)
    wordpress_title = models.TextField()
    active = models.BooleanField(default=False)
    wordpress_site=models.CharField(max_length=200,default='nowebsite')
    wordpress_status_post=models.TextField(blank=True)
    iframe=models.TextField(default='no iframe')
    cate = tagulous.models.TagField(to=Cate,blank=True)
    tag = tagulous.models.TagField(to=TagData,blank=True)
    focus_keyword = models.TextField(blank=True)
    description_keyword = models.TextField(blank=True)