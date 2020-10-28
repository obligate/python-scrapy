# _*_ coding: utf-8 _*_
# @Time     : 2020/10/24 1:30
# @Author   : Peter
# @File     : main.py
# 1. 需要把当前文件所在的根目录添加到环境变量才可以进行debug
# 2. 使用execute执行命令
# 3. 就可以在spider中，添加断点，进行debug

from scrapy.cmdline import execute

import sys
import os

# print(__file__)
# print(os.path.abspath(__file__))                   # 获取当前文件的所在的根目录
# print(os.path.dirname(os.path.abspath(__file__)))  # 获取当前文件的所在的根目录,建议用这种

sys.path.append(os.path.dirname(os.path.abspath(__file__)))   # 需要把当前文件所在的根目录添加到环境变量才可以进行debug

# execute(['scrapy', 'crawl', 'cnblogs'])
execute(['scrapy', 'crawl', 'zhihu'])
