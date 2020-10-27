# _*_ coding: utf-8 _*_
# @Time     : 2020/10/27 14:34
# @Author   : Peter
# @File     : decorate_test.py
import time

# 装饰器
def timer(func):
    def wrapper(*kw, **kwargs):
        start_time = time.time()
        func(*kw, **kwargs)
        end_time = time.time()
        print('{} run time {}'.format(func.__name__, end_time - start_time))
    return wrapper

@timer
def test1(name, age):
    time.sleep(3)


test1('Peter', 18)   # 相当于执行timer(test1)('Peter,18)
