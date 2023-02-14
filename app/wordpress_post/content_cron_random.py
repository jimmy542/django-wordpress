# -*- coding: utf-8 -*-
import datetime
from django_cron import CronJobBase, Schedule


from wordpress.models import Wordpress

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

from wordpress_post.models import WordpressPost
from wordpress_category.models import WordpressCategory
from wordpress_tag.models import WordPressTag


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
        # data_content = WordpressPost.objects.filter(active=False).order_by('id')[:150]
        data_content = WordpressPost.objects.filter(active=False).order_by('id')[:10]
        if (len(data_content) > 0):
            for post in data_content:
                post_id = post.wordpress_post_id
                content = post.wordpress_content
                title = post.wordpress_title
                focuskw = post.focus_keyword
                website_link = post.wordpress_website
                description_keyword =post.description_keyword
                if (len(content)==0):
                    print("no content use " + title)
                    d_content = title
                else:
                    d_content = content
                    # print("have content" + content)
                if(len(focuskw)==0):
                    data_focuskw = title
                else:
                    data_focuskw = focuskw
                if(len(description_keyword)==0):
                    data_description_keyword = title
                else:
                    data_description_keyword = description_keyword

                tag  = post.tag.all()
                category = post.category.all()
                print(len(tag))
                print(len(category))
                data_cate1=[]
                data_cate2 = []
                for cate in category:
                    # print(cate.category_wordpress_id)
                    data_cate1.append(cate.category_wordpress_id)
                data_tag1=[]
                data_tag2=[]
                print('before cate '+str(data_cate1))
                for tag_id in tag:
                    # print(tag_id.wordpress_tag_id)
                    data_tag1.append(tag_id.wordpress_tag_id)

                if(str(len(category)) < "4"):
                    total_cate = random.randint(10, 25)
                    cate_ids = WordpressCategory.objects.filter(active=True).order_by('?')[:total_cate]
                    for c1 in cate_ids:
                        data_cate2.append(c1.category_wordpress_id)
                        print(c1.category_wordpress_id)
                all_cate = data_cate1+data_cate2

                if(str(len(tag)) == "1"):
                    tatal_tag = random.randint(10, 30)
                    print("insert record should be"+str(tatal_tag))
                    d2 = WordPressTag.objects.order_by('?')[:tatal_tag]
                    for c2 in d2:
                        data_tag2.append(c2.wordpress_tag_id)
                    print("no tag")
                all_tag = data_tag1+data_tag2
                post = {
                        'title': title,
                        'content': d_content,
                        'status': 'publish',
                        "meta": {
                            "_yoast_wpseo_focuskw": data_focuskw,
                            "_yoast_wpseo_metadesc": data_description_keyword
                        },
                        'categories': all_cate,
                        'tags': all_tag

                    }
                res = requests.post(url + post_id, headers=header, json=post)
                if (res.status_code == 200):
                    p = WordpressPost.objects.get(wordpress_post_id=post_id,wordpress_website=website_link)
                    p.active = True
                    p.save()
        message = f"Code: {self.code}    Current date: {datetime.datetime.now()}\n"
        with open(self.file_path, "a") as myfile:
            myfile.write(message)

class Random_Content_CronJob(CronJobBase,Random_Content):
    """
    Run the job every 60 minutes
    """

    RUN_EVERY_MINS = 60
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = "cron.Random_Content_CronJob"