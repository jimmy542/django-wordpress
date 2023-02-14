import random
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
class Sync_Content:
    """
    Write current date to file.
    """

    file_path = "cron-demo.txt"
    def do(self):
        data_web = Wordpress.objects.filter(active=True).order_by('id').first()
        p2 = "/wp-json/wp/v2/posts/"
        url = data_web.url + p2
        user = data_web.username
        password = data_web.api_password
        credentials = user + ':' + password
        token = base64.b64encode(credentials.encode())
        header = {'Authorization': 'Basic ' + token.decode('utf-8')}
        data_content = Content.objects.filter(active=False).order_by('id')[:30]
        if (len(data_content) > 0):
            for post in data_content:
                post_id = post.post_wordpress_id
                content = post.wordpress_content
                title = post.wordpress_title
                category = str(post.cate)
                tag = str(post.tag)

                data = []
                data2 = []
                x = category.split(",")
                x2 = tag.split(",")
                if (len(x) != 0):
                    for n in x:
                        category_data = Category.objects.filter(name__icontains=n.strip()).order_by('id').first()
                        if (category_data != None):
                            data.append(category_data.category_wordpress_id)
                if (len(x2) != 0):
                    for n2 in x2:
                        print(n2)
                        tagdata = Tag.objects.filter(name__icontains=n2.strip()).order_by('id').first()
                        if (tagdata != None):
                            data2.append(tagdata.tag_wordpress_id)

                if (content != ""):
                    print("existing content")
                    post = {
                        'title': title,
                        'content': content,
                        'status': 'publish',
                        "meta": {
                            "_yoast_wpseo_focuskw": title,
                            "_yoast_wpseo_metadesc": content
                        },
                        'categories': data,
                        'tags': data2

                    }
                else:
                    print("no content")
                    post = {
                        "title": title,
                        "content": content,
                        "status": 'publish',
                        "meta_data": {
                            "key": "_yoast_wpseo_focuskw",
                            "value":content,
                            "key": "_yoast_wpseo_metadesc",
                            "value": content,
                        },
                        'categories': data,
                        'tags': data2
                    }

                res = requests.post(url + post_id, headers=header, json=post)
                if (res.status_code == 200):
                    p = Content.objects.get(post_wordpress_id=post_id)
                    p.active=True
                    p.save()
        message = f"Code: {self.code}    Current date: {datetime.datetime.now()}\n"
        with open(self.file_path, "a") as myfile:
            myfile.write(message)
class RunEveryTenMinutesCronJob(CronJobBase, Sync_Content):
    """
    Run the job every 10 minutes
    """

    RUN_EVERY_MINS = 1200
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = "cron.RunEveryTenMinutesCronJob"