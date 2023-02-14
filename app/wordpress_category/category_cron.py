
import datetime
from django_cron import CronJobBase, Schedule
from wordpress.models import Wordpress
from tag.models import Tag

import requests
import json
import base64
import logging
import warnings
import re

from wordpress_category.models import WordpressCategory


class Sync_Category:
    def do(self):
        data_web = Wordpress.objects.filter(sync_status="sync").order_by('id').first()
        p2 = "/wp-json/wp/v2/categories"
        url = data_web.url + p2
        user = data_web.username
        website = data_web.url
        password = data_web.api_password
        credentials = user + ':' + password
        token = base64.b64encode(credentials.encode())
        header = {'Authorization': 'Basic ' + token.decode('utf-8')}
        data_category = WordpressCategory.objects.filter(category_wordpress_id='noid',wordpress_website='nowebsite').order_by('id')[:100]
        if (len(data_category) > 0):
            for category in data_category:
                name = category.category_name
                slug = category.category_name
                description = category.category_name
                category_id = category.id
                post = {
                    'name': name,
                    'slug': slug,
                    'description': description,
                }
                res = requests.post(url, headers=header, json=post)
                if 200 <= res.status_code <= 300:
                    data2 = res.json()
                    p = WordpressCategory.objects.get(id=category_id)
                    p.category_wordpress_id=data2['id']
                    p.wordpress_name=website
                    p.active=True
                    p.save()
class Sync_Category_CronJob(CronJobBase, Sync_Category):
    """
    Run the job every 5 minutes
    """

    RUN_EVERY_MINS = 5
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = "Sync_Category_CronJob"