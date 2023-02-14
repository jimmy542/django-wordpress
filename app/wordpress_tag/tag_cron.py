
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


class Sync_Tag:
    def do(self):
        data_web = Wordpress.objects.filter(active="True").order_by('id').first()
        p2 = "/wp-json/wp/v2/categories"
        url = data_web.url + p2
        user = data_web.username
        website = data_web.url
        password = data_web.api_password
        credentials = user + ':' + password
        token = base64.b64encode(credentials.encode())
        header = {'Authorization': 'Basic ' + token.decode('utf-8')}
        data_tag = WordPressTag.objects.filter(wordpress_tag_id='noid').order_by('id')[:100]
        if (len(data_tag) > 0):
            for tag2 in data_tag:
                name = tag2.tag_name
                slug = tag2.tag_name
                description = tag2.tag_name
                tag_id = tag2.id
                post = {
                    'name': name,
                    'slug': slug,
                    'description': description,
                }
                res = requests.post(url, headers=header, json=post)
                if 200 <= res.status_code <= 300:
                    data2 = res.json()
                    p = WordPressTag.objects.get(id=tag_id)
                    p.wordpress_tag_id=data2['id']
                    p.website_name=website
                    p.active=True
                    p.sync_status='sync'
                    p.save()
class Sync_tag_CronJob(CronJobBase, Sync_Tag):
    """
    Run the job every 5 minutes
    """

    RUN_EVERY_MINS = 5
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = "Sync_tag_CronJob"