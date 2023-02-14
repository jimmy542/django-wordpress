# # -*- coding: utf-8 -*-
# from django.contrib import admin
# from .models import Tag
# from wordpress.models import Wordpress
# from website.models import Website
# from content.models import TagData
# import logging
# from django.urls import path
# from django.http import HttpResponse, HttpResponseRedirect
# from django.core.exceptions import ObjectDoesNotExist
# from bs4 import BeautifulSoup
# import requests
# import json
# import base64
# import re
#
# # Register your models here.
# class TagAdmin(admin.ModelAdmin):
#     change_list_template = "tag.html"
#     list_display = ['name','tag_wordpress_id','website']
#     list_per_page = 20
#     #list_editable = ['name','category_wordpress_id']
#     list_filter = ['name','tag_wordpress_id','website']
#     search_fields = ['name','tag_wordpress_id','website']
#     fields = ['name','tag_wordpress_id','active']
#
#     def sync(self,request,queryset):
#         queryset.update(detail="okay")
#
#     def get_urls(self):
#         urls = super().get_urls()
#         my_urls = [
#             path('import_data/', self.import_data),
#             path('send_data/', self.create_wordpress),
#             path('update_data/', self.update_wordpress),
#             path('get_data/', self.get_post),
#         ]
#         return my_urls + urls
#     def import_data(self):
#         logging.info("loggin create wordpress")
#
#     def create_wordpress(self):
#         logging.info("loggin create wordpress")
#
#         return HttpResponseRedirect("../")
#     def update_wordpress(self,request):
#         data_web = Wordpress.objects.filter(active=True).order_by('id').first()
#         p2 = "/wp-json/wp/v2/tags/"
#         url = data_web.url + p2
#         user = data_web.username
#         password = data_web.api_password
#         credentials = user + ':' + password
#         token = base64.b64encode(credentials.encode())
#         header = {'Authorization': 'Basic ' + token.decode('utf-8')}
#         data_tag = Tag.objects.filter(active=False).order_by('id')[:100]
#         if (len(data_tag) > 0):
#             for tag in data_tag:
#                 tag_id = tag.tag_wordpress_id
#                 name = tag.name
#                 website  = tag.website
#                 # print(content)
#                 if(name!=""):
#                     print("existing content")
#                     name = {
#                         'name': name,
#                         'slug': name,
#                         'description':name
#                     }
#                 else:
#                     print("no content")
#                     name = {
#                         'name': name,
#                         'slug': name,
#                         'description':name
#                     }
#
#                 res = requests.post(url + tag_id, headers=header, json=name)
#                 if(res.status_code==200):
#                     p = Tag.objects.get(tag_wordpress_id=tag_id)
#                     p.active=True
#                     p.save()
#
#         print("update wordpress now")
#         return HttpResponseRedirect("../")
#
#     def get_post(self,request):
#         data_web = Wordpress.objects.filter(active=True).order_by('id').first()
#         logging.info(str(data_web))
#         p2 = "/wp-json/wp/v2/tags?per_page=100&page=1"
#         if(data_web!=None):
#             url = data_web.url+p2
#             user = data_web.username
#             website = data_web.url
#             password = data_web.password
#             credentials = user + ':' + password
#             token = base64.b64encode(credentials.encode())
#             header = {'Authorization': 'Basic ' + token.decode('utf-8')}
#             res = requests.get(url, headers=header)
#             if 200 <= res.status_code <= 300:
#                 data = res.json()
#                 if(len(data)>1):
#                     for tag in data:
#                         n = Tag.objects.filter(tag_wordpress_id=tag['id']).order_by('id').first()
#                         if(n!=None):
#                             soup = BeautifulSoup(tag['name'])
#                             text = soup.get_text()
#                             cleantext = re.sub(r"[-()\"#/@;:<>{}`+=~|.!?,]", "", text)
#                             t = Tag.objects.get(tag_wordpress_id=tag['id'])
#                             t.name = cleantext
#                             t.save()
#                         else:
#                             print("can insert")
#                             soup = BeautifulSoup(tag['name'])
#                             text = soup.get_text()
#                             cleantext = re.sub(r"[-()\"#/@;:<>{}`+=~|.!?,]", "", text)
#                             tag_n = TagData.objects.filter(name=cleantext)
#                             if (tag_n != None):
#                                 ta = TagData(name=cleantext, slug=cleantext)
#                                 ta.save()
#                                 tag_n2 = TagData.objects.get(name=cleantext)
#                                 t = Tag(tag_wordpress_id=tag['id'],name=cleantext,website=website,tag_django_id=tag_n2.id)
#                                 t.save()
#
#         return HttpResponseRedirect("../")
#
# admin.site.register(Tag,TagAdmin)