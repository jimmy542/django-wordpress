
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import logging
class ReadWebSite:

    def scan_first_page(self):
    user_web = 'https://xn--72c9abh1f8ad1lzc.com/'
    r  = requests.get(user_web)
    data = r.text
    soup = BeautifulSoup(data)
    print(soup)