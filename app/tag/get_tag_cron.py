from bs4 import BeautifulSoup
import datetime
from django_cron import CronJobBase, Schedule
from wordpress.models import Wordpress
from tag.models import Tag
from wordpress.models import Wordpress
from content.models import TagData
from website.models import Website
from tag.models import Tag
from category.models import Category
from content.models import Cate
import requests
import json
import base64
import logging
import warnings
import re
class Get_Tag:
    def do(self):
        data_web = Wordpress.objects.filter(sync_status="sync").order_by('id').first()
        logging.info(str(data_web))
        p2 = "/wp-json/wp/v2/tags?per_page=100&page="+str(data_web.tag_page)
        if (data_web != None):
            url = data_web.url + p2
            user = data_web.username
            website = data_web.url
            password = data_web.password
            credentials = user + ':' + password
            token = base64.b64encode(credentials.encode())
            header = {'Authorization': 'Basic ' + token.decode('utf-8')}
            res = requests.get(url, headers=header)
            if 200 <= res.status_code <= 300:
                data = res.json()
                if (len(data) > 1):
                    for tag in data:
                        n = Tag.objects.filter(tag_wordpress_id=tag['id']).order_by('id').first()
                        if (n!= None):
                            soup = BeautifulSoup(tag['name'])
                            text = soup.get_text()
                            cleantext = re.sub(r"[-()\"#/@;:<>{}`+=~|.!?,]", "", text)
                            t = Tag.objects.get(tag_wordpress_id=tag['id'])
                            t.name = cleantext
                            t.active = True
                            t.save()
                        else:
                            print("can insert")
                            soup = BeautifulSoup(tag['name'])
                            text = soup.get_text()
                            cleantext = re.sub(r"[-()\"#/@;:<>{}`+=~|.!?,]", "", text)
                            tag_n = TagData.objects.filter(name=cleantext)
                            if (tag_n != None):
                                ta = TagData(name=cleantext, slug=cleantext)
                                ta.save()
                                tag_n2 = TagData.objects.get(name=cleantext)
                                t = Tag(tag_wordpress_id=tag['id'], name=cleantext, website=website,
                                        tag_django_id=tag_n2.id)
                                t.save()
                    data_web.tag_page = data_web.tag_page + 1
                    data_web.save()
                else:
                    data_web.tag_page = 1
                    data_web.save()
                    print("no data found")
            else:
                data_web.tag_page = 1
                data_web.save()
                print(res.status_code)
class Get_Tag_CronJob(CronJobBase, Get_Tag):
    """
    Run the job every 35 minutes
    """

    RUN_EVERY_MINS = 5
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = "Get_Tag_CronJob"