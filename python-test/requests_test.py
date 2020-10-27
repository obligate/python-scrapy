# _*_ coding: utf-8 _*_
# @Time     : 2020/10/24 23:28
# @Author   : Peter
# @File     : requests_test.py


import requests

response = requests.get('https://news.cnblogs.com/NewsAjax/GetAjaxNewsInfo?contentId=675731')
print(response.text)

import json

j_data = json.loads(response.text)
print(j_data['TotalView'])
