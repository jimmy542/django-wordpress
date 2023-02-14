from bs4 import BeautifulSoup
import datetime
from django_cron import CronJobBase, Schedule

from wordpress.models import Wordpress
import requests
import json
import base64
import logging
import warnings
import re
from wordpress_tag.models import WordPressTag


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
                        n = WordPressTag.objects.filter(wordpress_website=tag['link']).order_by('id').first()
                        if (n!= None):
                            soup = BeautifulSoup(tag['name'])
                            text = soup.get_text()
                            cleantext = re.sub(r"[-()\"#/@;:<>{}`+=~|.!?,]", "", text)
                            t = WordPressTag.objects.get(wordpress_website=tag['link'])
                            t.website_name = website
                            t.tag_name = cleantext
                            t.active = True
                            t.save()
                        else:

                            soup = BeautifulSoup(tag['name'])
                            text = soup.get_text()
                            # print("can insert " + text)
                            cleantext = re.sub(r"[-()\"#/@;:<>{}`+=~|.!?,]", "", text)
                            tag_check = WordPressTag.objects.filter(wordpress_website=tag['link']).order_by('id').first()
                            if (tag_check == None):
                                tag_data = WordPressTag(wordpress_tag_id=tag['id']
                                                        ,active=True
                                                        , tag_name=cleantext
                                                        , wordpress_website=tag['link']
                                                        ,website_name=website)
                                tag_data.save()
                            elif(tag_check!=None):
                                print("duplicate tag record")
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