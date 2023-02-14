from bs4 import BeautifulSoup
import datetime
from django_cron import CronJobBase, Schedule
from wordpress.models import Wordpress
from tag.models import Tag
from category.models import Category
from content.models import Cate
import requests
import json
import base64
import logging
import warnings
import re
class Get_Category:
    def do(self):
        data_web = Wordpress.objects.filter(sync_status="sync").order_by('id').first()
        logging.info(str(data_web))
        p2 = "/wp-json/wp/v2/categories?per_page=100&page="+str(data_web.category_page)
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
                    for category in data:
                        n = Category.objects.filter(category_wordpress_id=category['id']).order_by('id').first()
                        if (n!= None):
                            soup = BeautifulSoup(category['name'])
                            text = soup.get_text()
                            cleantext = re.sub(r"[-()\"#/@;:<>{}`+=~|.!?,]", "", text)
                            c = Category.objects.get(category_wordpress_id=category['id'])
                            c.name = cleantext
                            c.save()
                        else:
                            print("can insert")
                            cate_n = Cate.objects.filter(name=category['name'])
                            if (cate_n != None):
                                soup = BeautifulSoup(category['name'])
                                text = soup.get_text()
                                cleantext = re.sub(r"[-()\"#/@;:<>{}`+=~|.!?,]", "", text)
                                c = Category(category_wordpress_id=category['id'], name=cleantext, website=website)
                                c.save()
                    data_web.category_page = data_web.category_page + 1
                    data_web.save()
                else:
                    data_web.category_page = 1
                    data_web.save()
                    print("no data found")
            else:
                data_web.category_page = 1
                data_web.save()
                print(res.status_code)
class Get_Category_CronJob(CronJobBase, Get_Category):
    """
    Run the job every 35 minutes
    """

    RUN_EVERY_MINS = 5
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = "Get_Category_CronJob"