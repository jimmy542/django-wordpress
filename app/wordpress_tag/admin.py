from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import WordPressTag



class WordpressTagAdmin(admin.ModelAdmin):
    list_display = ['tag_name','wordpress_website','wordpress_tag_id','sync_status']
    list_per_page = 20
    list_filter = ['tag_name']
    search_fields = ['tag_name','wordpress_website','wordpress_tag_id','sync_status']
    fields = ['tag_name','wordpress_website','website_name','wordpress_tag_id','sync_status','active']
    actions = ['active']
admin.site.register(WordPressTag,WordpressTagAdmin)