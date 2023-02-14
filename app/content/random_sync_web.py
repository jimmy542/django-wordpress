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
import random
class Random_Sync:
    """
    Write current date to file.
    """

    file_path = "cron-demo.txt"
    def do(self):
        data_all_web = Wordpress.objects.all()
        nextweb_sync = random.choice(data_all_web)

        # set all to nosync

        # set_all_web = Wordpress.objects.all()
        # set_all_web.sync_status = "nosync"
        # set_all_web.save()
        Wordpress.objects.all().order_by('id').update(sync_status="nosync")

        # change sync random
        print(nextweb_sync.name)
        select_web = Wordpress.objects.get(name=nextweb_sync.name)
        select_web.sync_status = "sync"
        select_web.save()

class randomSync(CronJobBase, Random_Sync):
    """
    Run the job every 10 minutes
    """

    RUN_EVERY_MINS = 1
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = "cron.randomSync"