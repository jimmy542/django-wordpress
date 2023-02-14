
import datetime
from django_cron import CronJobBase, Schedule
from wordpress.models import Wordpress
from tag.models import Tag
from category.models import Category
import requests
import json
import base64
import logging
import warnings
import re
class Sync_Category:
    def do(self):
        data_web = Wordpress.objects.filter(sync_status="sync").order_by('id').first()
        p2 = "/wp-json/wp/v2/categories"
        url = data_web.url + p2
        user = data_web.username
        password = data_web.api_password
        credentials = user + ':' + password
        token = base64.b64encode(credentials.encode())
        header = {'Authorization': 'Basic ' + token.decode('utf-8')}
        data_category = Category.objects.filter(category_wordpress_id='noid').order_by('id')[:100]
        if (len(data_category) > 0):
            for category in data_category:
                name = category.name
                slug = category.name
                description = category.name
                category_id = category.id
                post = {
                    'name': name,
                    'slug': slug,
                    'description': description,
                }
                res = requests.post(url, headers=header, json=post)
                if 200 <= res.status_code <= 300:
                    data2 = res.json()
                    p = Category.objects.get(id=category_id)
                    p.category_wordpress_id=data2['id']
                    p.active=True
                    p.save()
class Sync_Category_CronJob(CronJobBase, Sync_Category):
    """
    Run the job every 10 minutes
    """

    RUN_EVERY_MINS = 5
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = "RunEveryThreeMinutesCronJob"