# _*_ coding: utf-8 _*_
# @Time     : 2020/10/26 22:46
# @Author   : Peter
# @File     : zhihu.py


import re
import json
from urllib import parse
import time

import scrapy
from selenium import webdriver


class ZhihuSpider(scrapy.Spider):
    name = "zhihu"
    allowed_domains = ["www.zhihu.com"]
    start_urls = ['https://www.zhihu.com/']

    def start_requests(self):
        browser = webdriver.Chrome(executable_path='E:/Work/Lib/python/chromedriver_win32/chromedriver.exe')
        browser.get('https://www.zhihu.com/signin')
        browser.find_element_by_css_selector('.SignFlow-tabs .SignFlow-tab:nth-child(2)').click()
        browser.find_element_by_css_selector('.SignFlow-accountInput.Input-wrapper input').send_keys('18782902568')
        browser.find_element_by_css_selector('.SignFlow-password input').send_keys('admin12')
        browser.find_element_by_css_selector('.Button.SignFlow-submitButton.Button--primary.Button--blue').click()
        time.sleep(60)




