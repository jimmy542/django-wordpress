# # -*- coding: utf-8 -*-
# from django.contrib import admin
# from .models import Category
# from wordpress.models import Wordpress
# from website.models import Website
# from content.models import Cate
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
#
# # Register your models here.
# class CategoryAdmin(admin.ModelAdmin):
#     change_list_template = "category.html"
#     list_display = ['name','category_wordpress_id','website']
#     list_per_page = 20
#     #list_editable = ['name','category_wordpress_id']
#     list_filter = ['name','category_wordpress_id']
#     search_fields = ['name','category_wordpress_id']
#     fields = ['name','category_wordpress_id','active']
#
#     def sync(self,request,queryset):
#         queryset.update(detail="okay")
#
#     def get_urls(self):
#         urls = super().get_urls()
#         my_urls = [
#            path('import_data/', self.import_data),
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
#         p2 = "/wp-json/wp/v2/categories/"
#         url = data_web.url + p2
#         user = data_web.username
#         password = data_web.api_password
#         credentials = user + ':' + password
#         token = base64.b64encode(credentials.encode())
#         header = {'Authorization': 'Basic ' + token.decode('utf-8')}
#         data_category = Category.objects.filter(active=False).order_by('id')[:100]
#         if (len(data_category) > 0):
#             for category in data_category:
#                 cate_id = category.category_wordpress_id
#                 name = category.name
#                 website  = category.website
#                 # print(content)
#                 if(name!=''):
#                     print("existing content")
#                     name = {
#                         'name': name,
#                         'slug': name,
#                         'description':name
#                     }
#                     p1 = Category.objects.get(category_wordpress_id=cate_id)
#                     p1.active=True
#                     p1.save()
#                 else:
#                     print("no content")
#                     name = {
#                         'name': name,
#                         'slug': name,
#                         'description':name
#                     }
#
#                 res = requests.post(url + cate_id, headers=header, json=name)
#                 print(res.content)
#                 if(res.status_code==200):
#                     p = Category.objects.get(category_wordpress_id=cate_id)
#                     p.active=True
#                     p.save()
#
#         print("update wordpress now")
#         return HttpResponseRedirect("../")
#
#     def get_post(self,request):
#         data_web = Wordpress.objects.filter(active=True).order_by('id').first()
#         logging.info(str(data_web))
#         p2 = "/wp-json/wp/v2/categories?per_page=100&page="+str(data_web.category_page)
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
#                     for category in data:
#                         n = Category.objects.filter(category_wordpress_id=category['id']).order_by('id').first()
#                         if(n!=None):
#                             soup = BeautifulSoup(category['name'])
#                             text = soup.get_text()
#                             cleantext = re.sub(r"[-()\"#/@;:<>{}`+=~|.!?,]", "", text)
#                             c = Category.objects.get(category_wordpress_id=category['id'])
#                             c.name = cleantext
#                             c.save()
#                         else:
#                             print("can insert")
#                             cate_n = Cate.objects.filter(name=category['name'])
#                             if(cate_n!=None):
#                                 soup = BeautifulSoup(category['name'])
#                                 text = soup.get_text()
#                                 cleantext = re.sub(r"[-()\"#/@;:<>{}`+=~|.!?,]", "", text)
#                                 c = Category(category_wordpress_id=category['id'],name=cleantext,website=website)
#                                 c.save()
#
#         return HttpResponseRedirect("../")
#     def create_wordpress(self,request):
#         data_web = Wordpress.objects.filter(active=True).order_by('id').first()
#         p2 = "/wp-json/wp/v2/categories"
#         url = data_web.url + p2
#         user = data_web.username
#         password = data_web.api_password
#         credentials = user + ':' + password
#         token = base64.b64encode(credentials.encode())
#         header = {'Authorization': 'Basic ' + token.decode('utf-8')}
#         data_category = Category.objects.filter(category_wordpress_id='noid').order_by('id')[:10]
#         if (len(data_category) > 0):
#             for category in data_category:
#                 name = category.name
#                 slug = category.name
#                 description = category.name
#                 category_id = category.id
#                 post = {
#                     'name': name,
#                     'slug': slug,
#                     'description': description,
#                 }
#                 res = requests.post(url, headers=header, json=post)
#                 if 200 <= res.status_code <= 300:
#                     data2 = res.json()
#                     p = Category.objects.get(id=category_id)
#                     p.category_wordpress_id=data2['id']
#                     p.active=True
#                     p.save()
#         return HttpResponseRedirect("../")
#     def category_insert(self, request):
#         # self.model.objects.all().update(name="set_immortal")
#         # test_insert = Category.objects.create(name='test')
#         user_web = 'https://xn--72c9abh1f8ad1lzc.com/'
#         r= requests.get(user_web)
#         soup = BeautifulSoup(r.content, 'html.parser')
#         data2 = soup.find_all('div', class_='column is-2-desktop is-one-quarter-tablet is-half-mobile')
#         page = soup.find('ul', class_='pagination-list')
#         # print(data2[0])
#         data_text=[]
#         for data3 in data2:
#             data_a = data3.find('a')
#             data_h2 = data3.find('h2')
#             image = data_a.find('img')
#             data_text.append(data_a['href'])
#             # print(data_a['href'])
#             # print(image['src'])
#             # print(data_h2.text)
#
#
#         # print(soup.get_text())
#         with open ('website.txt', 'w', encoding="utf-8") as f:
#             f.write(str(data_text))
#         # try:
#         #     n = Category.objects.filter(name='test').order_by('id').first()
#         #     logging.info('duplicate data')
#         #     self.message_user(request, "ข้อมูลมีอยู่แล้ว")
#         #     # number already exists
#         # except ObjectDoesNotExist:
#         #     # number does not exist
#         #     data = Category(name='test')
#         #     data.save()
#         #     logging.info('create data')
#         # self.message_user(request, "กำลัง ดูดข้อมูล")
#         return HttpResponseRedirect("../")
#
#     def set_mortal(self, request):
#         self.model.objects.all().update(name="set_mortal")
#         self.message_user(request, "All heroes are now mortal")
#         return HttpResponseRedirect("../")
#
#     # def clean_data(self,)
#
# admin.site.register(Category,CategoryAdmin)