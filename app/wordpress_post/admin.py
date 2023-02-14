from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import WordpressPost
# Register your models here.
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import path

class WordpressPostAdmin(admin.ModelAdmin):
    change_list_template = "wordpress_post.html"
    list_display = ['wordpress_title','wordpress_content','wordpress_post_id','iframe','wordpress_website','wordpress_status_post']
    list_per_page = 20
    list_filter = ['wordpress_status_post','website_name']
    search_fields = ['wordpress_title','wordpress_content','wordpress_post_id','iframe','wordpress_website','wordpress_status_post']
    fields = ['active','wordpress_title','wordpress_content','focus_keyword','description_keyword','tag','category']
    filter_horizontal=['tag','category']


    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('reset_sync/', self.reset_sync),
        ]
        return my_urls + urls
    def reset_sync(self,request):
        reset_page = WordpressPost.objects.filter(active=True).update(active=False)
        print("reset")
        return HttpResponseRedirect("../")

admin.site.register(WordpressPost,WordpressPostAdmin)