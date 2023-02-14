from django.contrib import admin
from .models import Website
# Register your models here.



class WebsiteAdmin(admin.ModelAdmin):

    list_display = ['name','url','active','page','que']
    list_per_page = 20
    list_filter = ['name','url']
    search_fields = ['name','url']
    fields = ['name','url','active','page','que']
    actions = ['active']

    def active(self, request, queryset):
        data_web = Website.objects.filter(active=True).update(active=False)
        queryset.update(active=True)



admin.site.register(Website,WebsiteAdmin)