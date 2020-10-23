# _*_ coding: utf-8 _*_
# @Time     : 2020/10/24 0:21
# @Author   : Peter
# @File     : test.py

import re

line = 'peter123'

regex_str = '^p.*'    # 字符以p开始，后面可以是任意字符
if re.match(regex_str, line):  # 只有模式匹配成功，就会返回一个值
    print('yes')