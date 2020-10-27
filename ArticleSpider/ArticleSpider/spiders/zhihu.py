# _*_ coding: utf-8 _*_
# @Time     : 2020/10/26 22:46
# @Author   : Peter
# @File     : zhihu.py


import re
import json
from urllib import parse

import scrapy



class ZhihuSpider(scrapy.Spider):
    name = "zhihu"
    allowed_domains = ["www.zhihu.com"]
    start_urls = ['https://www.zhihu.com/']

    def parse(self, response):
        pass



