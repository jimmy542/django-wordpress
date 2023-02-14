# -*- coding: utf-8 -*-
from django_cron import CronJobBase, Schedule
from .models import Content

from wordpress.models import Wordpress
from tag.models import Tag
from category.models import Category
from bs4 import BeautifulSoup
import requests
import base64
import logging
import re
class Get_content:
    """
    Write current date to file.
    """

    file_path = "cron-demo.txt"
    def do(self):
        data_web = Wordpress.objects.filter(sync_status="sync").order_by('id').first()
        logging.info(str(data_web))
        p2 = "/wp-json/wp/v2/posts?per_page=100&page=" + str(data_web.page)
        logging.debug("web data" + p2)
        if (data_web != None):
            url = data_web.url + p2
            user = data_web.username
            website = data_web.url
            password = data_web.password
            credentials = user + ':' + password
            token = base64.b64encode(credentials.encode())
            header = {'Authorization': 'Basic ' + token.decode('utf-8')}
            res = requests.get(url,headers=header)
            if 200 <= res.status_code <= 300:
                data = res.json()
                if (len(data) > 2):
                    for post in data:
                        n = Content.objects.filter(post_wordpress_id=post['id'],wordpress_site=website).order_by('id').first()
                        # print(str(n))
                        if (n != None):
                            print("duplicate")
                            soup = BeautifulSoup(post['content']['rendered'])
                            text = soup.get_text()
                            cleantext = re.sub(r"[-()\"#/@;:<>{}`+=~|.!?,]", "", text)
                            p = Content.objects.get(post_wordpress_id=post['id'])
                            print(cleantext)
                            p.wordpress_content = cleantext
                            p.title = post['title']['rendered']
                            p.wordpress_status_post=post['status']
                            p.active = True
                            p.wordpress_site=post['link']
                            p.save()
                            if (len(post['tags']) > 1):
                                data2 = []
                                for tag in post['tags']:
                                    tag_data = Tag.objects.filter(tag_wordpress_id=tag).order_by('id').first()
                                    if (tag_data == None):
                                        "no data found"
                                    else:
                                        data2.append(tag_data.name)
                                c1 = Content.objects.get(post_wordpress_id=post['id'])
                                c1.tag = data2
                                c1.save()
                            if (len(post['categories']) > 1):
                                data = []
                                for category in post['categories']:
                                    category_data = Category.objects.filter(category_wordpress_id=category).order_by(
                                        'id').first()
                                    if (category_data != None):
                                        data.append(category_data.name)
                                c = Content.objects.get(post_wordpress_id=post['id'])
                                c.cate = data
                                c.save()
                        else:
                            print("can insert")
                            soup = BeautifulSoup(post['content']['rendered'])
                            text = soup.get_text()
                            cleantext = re.sub(r"[-()\"#/@;:<>{}`+=~|.!?,]", "", text)
                            cleantitle = re.sub(r"[-()\"#/@;:<>{}`+=~|.!?,]", "", post['title']['rendered'])
                            logging.info(str(cleantext))
                            p = Content(post_wordpress_id=post['id'], wordpress_content=cleantext,
                                        wordpress_title=cleantitle,wordpress_site=post['link'],wordpress_status_post=post['status'])
                            p.save()
                            if (len(post['tags']) > 1):
                                data2 = []
                                for tag in post['tags']:
                                    tag_data = Tag.objects.filter(tag_wordpress_id=tag).order_by('id').first()
                                    if (tag_data == None):
                                        "no data found"
                                    else:
                                        data2.append(tag_data.name)
                                c1 = Content.objects.get(post_wordpress_id=post['id'])
                                c1.tag = data2
                                c1.save()
                            if (len(post['categories']) > 1):
                                data = []
                                for category in post['categories']:
                                    category_data = Category.objects.filter(category_wordpress_id=category).order_by(
                                        'id').first()
                                    if (category_data != None):
                                        print(category_data.name)
                                        data.append(category_data.name)
                                c = Content.objects.get(post_wordpress_id=post['id'])
                                c.cate = data
                                c.save()

                    data_web.page = data_web.page + 1
                    data_web.save()
                else:
                    data_web.page = 1
                    data_web.save()
                    print("no data found")
            else:
                data_web.page = 1
                data_web.save()
                print(res.status_code)

        else:
            logging.info("url website not active")
        if 200 <= res.status_code <= 300:
            post = res.json()
            logging.info(str(post))
        else:
            status = ["error", res.content]
            logging.info(str(status))
class getContent(CronJobBase, Get_content):
    """
    Run the job every 10 minutes
    """

    RUN_EVERY_MINS = 60
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = "cron.getContent"