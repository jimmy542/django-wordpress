# # -*- coding: utf-8 -*-
# from django.contrib import admin
# from .models import Content
# from .models import Cate
# from wordpress.models import Wordpress
# from website.models import Website
# from tag.models import Tag
# from category.models import Category
# # Register your models here.
# from django.urls import path
# from django.http import HttpResponse, HttpResponseRedirect
# from django.core.exceptions import ObjectDoesNotExist
# from bs4 import BeautifulSoup
# import requests
# import json
# import base64
# import logging
# import warnings
# import re
# import random
#
# class ContentAdmin(admin.ModelAdmin):
#     change_list_template = "post.html"
#     list_display = ['wordpress_title','wordpress_content','post_wordpress_id','iframe','wordpress_site','wordpress_status_post']
#     list_per_page = 100
#     list_filter = ['wordpress_title']
#     search_fields = ['wordpress_title','wordpress_content','post_wordpress_id','wordpress_site']
#     fields = ['wordpress_title','focus_keyword','description_keyword','wordpress_content','active','iframe','wordpress_site','cate','tag']
#
#
#
#     def get_urls(self):
#         urls = super().get_urls()
#         my_urls = [
#             path('import_data/', self.import_data),
#             path('send_data/', self.create_wordpress),
#             path('update_data/', self.update_wordpress),
#             path('get_data/', self.get_post),
#             path('reset_sync/', self.reset_sync),
#         ]
#         return my_urls + urls
#     def reset_sync(self,request):
#         post = Content.objects.filter(active=True).update(active=False)
#         print("reset")
#         return HttpResponseRedirect("../")
#     def get_post(self, request):
#         data_web = Wordpress.objects.filter(active=True).order_by('id').first()
#         logging.info(str(data_web))
#         p2 = "/wp-json/wp/v2/posts?per_page=100&page="+str(data_web.page)
#         logging.debug("web data"+p2)
#         if(data_web!=None):
#             url = data_web.url+p2
#             user = data_web.username
#             website = data_web.url
#             password = data_web.password
#             credentials = user + ':' + password
#             token = base64.b64encode(credentials.encode())
#             header = {'Authorization': 'Basic ' + token.decode('utf-8')}
#             res = requests.get(url, headers=header)
#             print("get post")
#
#             # print(str(res.content))
#             if 200 <= res.status_code <= 300:
#                 data = res.json()
#                 if(len(data)>2):
#                     for post in data:
#                         n = Content.objects.filter(post_wordpress_id=post['id']).order_by('id').first()
#                         if(n!=None):
#                             print("duplicate")
#                             soup = BeautifulSoup(post['content']['rendered'])
#
#                             text = soup.get_text()
#                             cleantext = re.sub(r"[-()\"#/@;:<>{}`+=~|.!?,]", "", text)
#                             p = Content.objects.get(post_wordpress_id=post['id'])
#                             print(cleantext)
#                             p.wordpress_content = cleantext
#                             p.title=post['title']['rendered']
#                             p.active=True
#                             p.save()
#                             if (len(post['tags']) > 1):
#                                 data2 = []
#                                 for tag in post['tags']:
#                                     tag_data = Tag.objects.filter(tag_wordpress_id=tag).order_by('id').first()
#                                     if(tag_data==None):
#                                         "no data found"
#                                     else:
#                                         data2.append(tag_data.name)
#                                 c1 = Content.objects.get(post_wordpress_id=post['id'])
#                                 c1.tag = data2
#                                 c1.save()
#                             if (len(post['categories']) > 1):
#                                 data = []
#                                 for category in post['categories']:
#                                     category_data = Category.objects.filter(category_wordpress_id=category).order_by(
#                                         'id').first()
#                                     if (category_data != None):
#                                         data.append(category_data.name)
#                                 c = Content.objects.get(post_wordpress_id=post['id'])
#                                 c.cate = data
#                                 c.save()
#                         else:
#                             print("can insert")
#                             soup = BeautifulSoup(post['content']['rendered'])
#                             text = soup.get_text()
#                             cleantext = re.sub(r"[-()\"#/@;:<>{}`+=~|.!?,]", "", text)
#                             cleantitle = re.sub(r"[-()\"#/@;:<>{}`+=~|.!?,]", "", post['title']['rendered'])
#                             logging.info(str(cleantext))
#                             p = Content(post_wordpress_id=post['id'], wordpress_content=cleantext,wordpress_title=cleantitle,wordpress_site=data_web.url)
#                             p.save()
#                             if(len(post['tags'])>1):
#                                 data2 = []
#                                 for tag in post['tags']:
#                                     tag_data = Tag.objects.filter(tag_wordpress_id=tag).order_by('id').first()
#                                     if(tag_data == None):
#                                         "no data found"
#                                     else:
#                                         data2.append(tag_data.name)
#                                 c1 = Content.objects.get(post_wordpress_id=post['id'])
#                                 c1.tag = data2
#                                 c1.save()
#                             if(len(post['categories'])>1):
#                                 data=[]
#                                 for category in post['categories']:
#                                     category_data = Category.objects.filter(category_wordpress_id=category).order_by('id').first()
#                                     if(category_data!=None):
#                                         print(category_data.name)
#                                         data.append(category_data.name)
#                                 c = Content.objects.get(post_wordpress_id=post['id'])
#                                 c.cate=data
#                                 c.save()
#
#
#                     data_web.page = data_web.page + 1
#                     data_web.save()
#                 else:
#                     data_web.page = 1
#                     data_web.save()
#                     print("no data found")
#             else:
#                 data_web.page = 1
#                 data_web.save()
#                 print(res.status_code)
#
#         else:
#             logging.info("url website not active")
#         if 200 <= res.status_code <= 300:
#             post = res.json()
#             logging.info(str(post))
#         else:
#             status =["error",res.content]
#             logging.info(str(status))
#
#         return HttpResponseRedirect("../")
#
#     def update_wordpress(self,request):
#         data_web = Wordpress.objects.filter(active=True).order_by('id').first()
#         p2 = "/wp-json/wp/v2/posts/"
#         url = data_web.url + p2
#         user = data_web.username
#         password = data_web.api_password
#         credentials = user + ':' + password
#         token = base64.b64encode(credentials.encode())
#         header = {'Authorization': 'Basic ' + token.decode('utf-8')}
#         data_content = Content.objects.filter(active=False).order_by('id')[:100]
#         if (len(data_content) > 0):
#             for post in data_content:
#                 post_id = post.post_wordpress_id
#                 content = post.wordpress_content
#                 title  = post.wordpress_title
#                 category= str(post.cate)
#                 tag = str(post.tag)
#
#                 data = []
#                 data2 = []
#                 x=category.split(",")
#                 x2=tag.split(",")
#                 if(len(x)!=0):
#                     for n in x:
#                         category_data = Category.objects.filter(name__icontains=n.strip()).order_by('id').first()
#                         if (category_data != None):
#                             data.append(category_data.category_wordpress_id)
#                 if(len(x2)!=0):
#                     for n2 in x2:
#                         print(n2)
#                         tagdata = Tag.objects.filter(name__icontains=n2.strip()).order_by('id').first()
#                         if(tagdata!=None):
#                             data2.append(tagdata.tag_wordpress_id)
#
#
#
#
#                 if(content!=""):
#                     print("existing content")
#                     post = {
#                         'title': title,
#                         'content': content,
#                         'status' : 'publish',
#                         "meta": {
#                             "_yoast_wpseo_focuskw": content,
#                             "_yoast_wpseo_metadesc":content
#                         },
#                         'categories': data,
#                         'tags':data2
#
#                     }
#                     print(post)
#                 else:
#                     print("no content")
#                     post = {
#                         'title': title,
#                         'content': title,
#                         'status': 'publish',
#                         "meta": {
#                             "_yoast_wpseo_focuskw": title,
#                             "_yoast_wpseo_metadesc":title
#                         },
#                         'categories':data,
#                         'tags':data2
#                     }
#
#                 res = requests.post(url + post_id, headers=header, json=post)
#                 if(res.status_code==200):
#                     p = Content.objects.get(post_wordpress_id=post_id)
#                     p.active=True
#                     p.save()
#
#         print("update wordpress now")
#         return HttpResponseRedirect("../")
#
#     def create_wordpress(self,request):
#         data_web = Wordpress.objects.filter(active=True).order_by('id').first()
#         p2 = "/wp-json/wp/v2/posts"
#         url = data_web.url + p2
#         user = data_web.username
#         password = data_web.api_password
#         credentials = user + ':' + password
#         token = base64.b64encode(credentials.encode())
#         header = {'Authorization': 'Basic ' + token.decode('utf-8')}
#         post = {
#                 "title": "title",
#                 "content": "content",
#                 "status": "draft",
#                 "meta": {
#                     "_yoast_wpseo_focuskw": "_yoast_wpseo_focuskw",
#                     "_yoast_wpseo_metadesc":"_yoast_wpseo_metadesc",
#                     }
#         }
#         response = requests.post(url, headers=header, json=post)
#         print(response)
#         return HttpResponseRedirect("../")
#
#     def import_data(self,request):
#         data_website = Website.objects.filter(active=True).order_by('id').first()
#         print(data_website.url)
#         print("importing")
#         return HttpResponseRedirect("../")
#
#     def category_insert(self, request):
#         # self.model.objects.all().update(name="set_immortal")
#         # test_insert = Category.objects.create(name='test')
#         user_web = 'https://xn--72c9abh1f8ad1lzc.com/'
#         r = requests.get(user_web)
#         soup = BeautifulSoup(r.content, 'html.parser')
#         data2 = soup.find_all('div', class_='column is-2-desktop is-one-quarter-tablet is-half-mobile')
#         page = soup.find('ul', class_='pagination-list')
#         # print(data2[0])
#         data_text = []
#         for data3 in data2:
#             data_a = data3.find('a')
#             data_h2 = data3.find('h2')
#             image = data_a.find('img')
#             data_text.append(data_a['href'])
#             # print(data_a['href'])
#             # print(image['src'])
#             # print(data_h2.text)
#
#         # print(soup.get_text())
#         with open('website.txt', 'w', encoding="utf-8") as f:
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
#
# admin.site.register(Content, ContentAdmin)