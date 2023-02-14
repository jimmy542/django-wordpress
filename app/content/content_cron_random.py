# -*- coding: utf-8 -*-
import datetime
from django_cron import CronJobBase, Schedule
from .models import Content
from .models import Cate
from wordpress.models import Wordpress
from website.models import Website
from tag.models import Tag
from category.models import Category
# Register your models here.
from django.urls import path
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from bs4 import BeautifulSoup
import requests
import json
import base64
import logging
import warnings
import re
import random
class Random_Content:
    """
    Write current date to file.
    """

    file_path = "cron-demo.txt"
    def do(self):
        data_web = Wordpress.objects.filter(sync_status="sync").order_by('id').first()
        p2 = "/wp-json/wp/v2/posts/"
        url = data_web.url + p2
        user = data_web.username
        password = data_web.api_password
        credentials = user + ':' + password
        token = base64.b64encode(credentials.encode())
        header = {'Authorization': 'Basic ' + token.decode('utf-8')}
        data_content = Content.objects.filter(active=False).order_by('id')[:150]
        if (len(data_content) > 0):
            for post in data_content:
                post_id = post.post_wordpress_id
                content = post.wordpress_content
                title = post.wordpress_title
                focuskw = post.focus_keyword
                description_keyword =post.description_keyword
                print(len(content))
                if (len(content)==0):
                    print("no content use " + title)
                    d_content = title
                else:
                    d_content = content
                    print("have content" + content)
                if(len(focuskw)==0):
                    data_focuskw = title
                else:
                    data_focuskw = focuskw
                if(len(description_keyword)==0):
                    data_description_keyword = title
                else:
                    data_description_keyword = description_keyword
                category = str(post.cate)
                tag = str(post.tag)
                x = category.split(",")
                x2 = tag.split(",")
                data = []
                data2 = []

                if(str(len(x)) < "3"):
                    total_cate = random.randint(5, 10)
                    cate_ids = Category.objects.filter(active=True).order_by('?')[:total_cate]
                    data = []
                    for c1 in cate_ids:
                        data.append(c1.category_wordpress_id)
                if(str(len(x2)) == "1"):
                    print(post_id)
                    n2 = random.randint(10, 30)
                    print("insert record should be"+str(n2))
                    d2 = Tag.objects.order_by('?')[:n2]
                    for c2 in d2:
                        data2.append(c2.tag_wordpress_id)
                    print("no tag")
                    print(str(data2))
                post = {
                        'title': title,
                        'content': d_content,
                        'status': 'publish',
                        "meta": {
                            "_yoast_wpseo_focuskw": data_focuskw,
                            "_yoast_wpseo_metadesc": data_description_keyword
                        },
                        'categories': data,
                        'tags': data2

                    }
                res = requests.post(url + post_id, headers=header, json=post)
                if (res.status_code == 200):
                    p = Content.objects.get(post_wordpress_id=post_id)
                    p.active = True
                    p.save()
        message = f"Code: {self.code}    Current date: {datetime.datetime.now()}\n"
        with open(self.file_path, "a") as myfile:
            myfile.write(message)

class Random_Content_CronJob(CronJobBase, Random_Content):
    """
    Run the job every 10 minutes
    """

    RUN_EVERY_MINS = 60
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = "cron.Random_Content_CronJob"