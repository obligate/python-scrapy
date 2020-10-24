# _*_ coding: utf-8 _*_
# @Time     : 2020/10/24 20:50
# @Author   : Peter
# @File     : urllib_test.py

from urllib import parse


# parse.urljoin()
# 使用 urllib.parse.urljoin将相对的一个地址组合成一个url，对于输入没有限制，开头必须是http://或者https://，否则将不组合前面的部分
url = "http://www.baidu.com/"
post_url = "n/123"
ret = parse.urljoin(url, post_url)
print(ret)
post_url = "http://www.cnblogs.com/n/123"
ret = parse.urljoin(url, post_url)     # post_url是http开头的，不组合前面的url，所以输出的是post_url本身
print(ret)
