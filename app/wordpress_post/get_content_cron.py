# -*- coding: utf-8 -*-
from django.db.models import Count
from django_cron import CronJobBase, Schedule

from wordpress_category.models import WordpressCategory
from wordpress_tag.models import WordPressTag
from .models import WordpressPost

from wordpress.models import Wordpress
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
        print('----------------------------------------------------------------------')
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
                        n = WordpressPost.objects.filter(wordpress_website=post['link']).count()
                        if (n!= 0):
                            print("duplicate")
                            soup = BeautifulSoup(post['content']['rendered'])
                            text = soup.get_text()
                            cleantext = re.sub(r"[-()\"#/@;:<>{}`+=~|.!?,]", "", text)
                            p = WordpressPost.objects.get(wordpress_website=post['link'])
                            print(cleantext)
                            p.wordpress_content = cleantext
                            p.title = post['title']['rendered']
                            p.wordpress_status_post=post['status']
                            p.website_name = website
                            p.active = True
                            p.wordpress_site=post['link']
                            p.save()
                            if (len(post['tags']) > 1):
                                for tag in post['tags']:
                                    tag_data = WordPressTag.objects.filter(wordpress_tag_id=tag,website_name=website).order_by('id').first()
                                    if (tag_data == None):
                                        "no data tag found"
                                    else:
                                        c1 = WordpressPost.objects.get(wordpress_website=post['link'])
                                        c1.tag.add(tag_data.id)
                            # print(post['categories'])
                            if (len(post['categories']) > 1):
                                for category in post['categories']:
                                    print(category)
                                    category_data = WordpressCategory.objects.filter(category_wordpress_id=category,website_name=website).order_by('id').first()
                                    if (category_data == None):
                                        "no data category found"
                                    else:
                                        print(category_data.id)
                                        c = WordpressPost.objects.get(wordpress_website=post['link'])
                                        c.category.add(category_data.id)
                        else:
                            print("can insert")
                            soup = BeautifulSoup(post['content']['rendered'])
                            text = soup.get_text()
                            cleantext = re.sub(r"[-()\"#/@;:<>{}`+=~|.!?,]", "", text)
                            cleantitle = re.sub(r"[-()\"#/@;:<>{}`+=~|.!?,]", "", post['title']['rendered'])
                            p = WordpressPost(wordpress_post_id=post['id'], wordpress_content=cleantext,
                                        wordpress_title=cleantitle,wordpress_website=post['link'],wordpress_status_post=post['status'],website_name=website)
                            p.save()
                            if (len(post['tags']) > 1):
                                for tag in post['tags']:
                                    tag_data = WordPressTag.objects.filter(wordpress_tag_id=tag,website_name=website).order_by('id').first()
                                    if (tag_data == None):
                                        "no data tag found"
                                    else:
                                        c1 = WordpressPost.objects.get(wordpress_website=post['link'])
                                        c1.tag.add(tag_data.id)
                            # print(post['categories'])
                            if (len(post['categories']) > 1):
                                for category in post['categories']:
                                    print(category)
                                    category_data = WordpressCategory.objects.filter(category_wordpress_id=category,website_name=website).order_by('id').first()
                                    if (category_data == None):
                                        "no data category found"
                                    else:
                                        print(category_data.id)
                                        c = WordpressPost.objects.get(wordpress_website=post['link'])
                                        c.category.add(category_data.id)
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
class getContent(CronJobBase,Get_content):
    """
    Run the job every 20 minutes
    """

    RUN_EVERY_MINS = 20
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = "cron.getContent"