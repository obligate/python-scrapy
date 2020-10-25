# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline


class ArticlespiderPipeline:
    def process_item(self, item, spider):
        return item


# 重写ImagesPipeline的Item_completed方法，获取图片的真实的物理路径
# 需要在setting.py 配置： 'ArticleSpider.pipelines.ArticleImagePipeline': 1,
class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        if "front_image_url" in item:
            for ok, value in results:
                image_file_path = value["path"]
            item["front_image_path"] = image_file_path

        return item