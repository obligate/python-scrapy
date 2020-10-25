# _*_ coding: utf-8 _*_
# @Time     : 2020/10/25 12:14
# @Author   : Peter
# @File     : common.py

import hashlib


def get_md5(url):
    if isinstance(url, str):
        url = url.encode('utf-8')
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


if __name__ == '__main__':
    print(get_md5('http://news.cnblogs.com'))
