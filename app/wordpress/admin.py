from django.contrib import admin
from .models import Wordpress
# Register your models here.
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import path
class WordpressAdmin(admin.ModelAdmin):
    change_list_template = "website.html"
    list_display = ['name','url','username','password','active','api_password','page','tag_page','category_page','sync_status']
    list_per_page = 20
    list_filter = ['name','url']
    search_fields = ['name','url']
    fields = ['name','url','active','username','password','api_password','page','tag_page','category_page','sync_status']
    actions = ['active']
    def active(self, request, queryset):
        data_web = Wordpress.objects.filter(active=True).update(active=False)
        queryset.update(active=True)
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('reset_sync/', self.reset_sync),
        ]
        return my_urls + urls
    def reset_sync(self,request):
        reset_page = Wordpress.objects.filter(active=True).update(page=1,category_page=1,tag_page=1)
        print("reset")
        return HttpResponseRedirect("../")
admin.site.register(Wordpress,WordpressAdmin)