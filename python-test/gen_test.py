# _*_ coding: utf-8 _*_
# @Time     : 2020/10/24 21:59
# @Author   : Peter
# @File     : gen_test.py

def my_gen():
    yield 1
    yield 2
    yield 3
    return 4


def my_fun():
    return 4


print(my_fun())    # 4

# 1.
# print(my_gen())    # <generator object my_gen at 0x000002185942A7C8>

# 2.
# 可以停止的函数
# print(next(my_gen()))   # 1
# print(next(my_gen()))   # 1
# print(next(my_gen()))   # 1
# print(next(my_gen()))   # 会报错

# 3.
# gen = my_gen()
# print(next(gen))   # 1
# print(next(gen))   # 2
# print(next(gen))   # 3
# print(next(gen))   # 会报错

# 4. 不会报错
for data in my_gen():
    print(data)

