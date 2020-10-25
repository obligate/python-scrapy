# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import datetime
import re

import scrapy
from scrapy.loader import ItemLoader
# from scrapy.loader.processors import MapCompose, TakeFirst, Join, Identity  # deprecated
from itemloaders.processors import MapCompose, TakeFirst, Join, Identity


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

# def add_cnblogs(value):
#     return value+"-cnblogs"
#
# def add_test(value):
#     return value+"-test"

# def remove_comment_tags(value):
#     #去掉tag中提取的评论
#     if "评论" in value:
#         return ""
#     else:
#         return value

def date_convert(value):
    match_re = re.match(".*?(\d+.*)", value)
    if match_re:
        return match_re.group(1)
    else:
        return "0000-00-00"

class CnBlogsArticleItemLoader(ItemLoader):
    # 自定义itemloader,从list变成str，在output的时候统一变成TakeFirst()
    default_output_processor = TakeFirst()

class CnBlogsArticleItem(scrapy.Item):
    title = scrapy.Field(
        # input_processor=MapCompose(add_cnblogs, add_test),
        # output_processor=TakeFirst()
    )
    create_date = scrapy.Field(
        input_processor=MapCompose(date_convert)
    )
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    front_image_url = scrapy.Field(
        output_processor=Identity()    # 需要使用list
    )
    front_image_path = scrapy.Field()
    praise_nums = scrapy.Field()
    comment_nums = scrapy.Field()
    fav_nums = scrapy.Field()
    tags = scrapy.Field(
        # input_processor=MapCompose(remove_comment_tags),
        output_processor=Join(separator=",")
    )
    content = scrapy.Field()


