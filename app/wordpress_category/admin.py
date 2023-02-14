from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import WordpressCategory
# Register your models here.


class WordpressCategoryAdmin(admin.ModelAdmin):

    list_display = ['category_name', 'detail', 'category_wordpress_id', 'wordpress_website','website_name']
    list_per_page = 20
    list_filter = ['category_name']
    search_fields = ['category_name', 'detail', 'category_wordpress_id', 'wordpress_website','website_name']
    fields = ['category_name', 'detail', 'category_wordpress_id', 'wordpress_website','website_name','active']
    actions = ['active']


admin.site.register(WordpressCategory,WordpressCategoryAdmin)