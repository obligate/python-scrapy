# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import codecs
import json


from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter

import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi

class ArticlespiderPipeline:
    def process_item(self, item, spider):
        return item


# 重写ImagesPipeline的Item_completed方法，获取图片的真实的物理路径
# 需要在setting.py 配置： 'ArticleSpider.pipelines.ArticleImagePipeline': 1,
class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        if "front_image_url" in item:
            # image_file_path = ""   # 防止报错
            for ok, value in results:
                image_file_path = value["path"]
            item["front_image_path"] = image_file_path

        return item


# 自定义json文件的导出
# 需要在setting.py 配置：'ArticleSpider.pipelines.JsonWithEncodingPipeline': 2,
class JsonWithEncodingPipeline(object):
    #自定义json文件的导出
    def __init__(self):
        self.file = codecs.open('article.json', 'w', encoding="utf-8")
    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item
    def spider_closed(self, spider):
        self.file.close()

# 用scrapy提供的json export导出json文件
# 跟上面的JsonWithEncodingPipeline 只需要提供一个即可
# 需要在setting.py 配置：'ArticleSpider.pipelines.JsonExporterPipleline': 3,
class JsonExporterPipleline(object):
    #调用scrapy提供的json export导出json文件
    def __init__(self):
        self.file = open('articleexport.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

# 采用同步的机制写入mysql，不建议
class MysqlPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect('127.0.0.1', 'root', 'root', 'article_spider', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            insert into cnblogs_article(title, url,url_object_id,front_image_url,front_image_path,praise_nums,comment_nums, fav_nums, tags, content, create_date)
            VALUES (%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s) ON DUPLICATE KEY UPDATE praise_nums=VALUES(praise_nums)
        """
        params = list()
        params.append(item.get("title", ""))
        params.append(item.get("url", ""))
        params.append(item.get("url_object_id", ""))
        front_images = ','.join(item.get("front_image_url", []))
        params.append(front_images)
        params.append(item.get("front_image_path", ""))
        params.append(item.get("praise_nums", 0))
        params.append(item.get("comment_nums", 0))
        params.append(item.get("fav_nums", 0))
        params.append(item.get("tags", ""))
        params.append(item.get("content", ""))
        params.append(item.get("create_date", "1970-07-01"))
        self.cursor.execute(insert_sql, tuple(params))

        self.conn.commit()

        return item

# 采用异步的机制写入mysql
class MysqlTwistedPipline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)

        return cls(dbpool)

    def process_item(self, item, spider):
        #使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)  # 将do_insert方法，放到twisted框架执行
        query.addErrback(self.handle_error, item, spider) #处理异常
        return item

    def handle_error(self, failure, item, spider):
        #处理异步插入的异常
        print(failure)

    def do_insert(self, cursor, item):
        #执行具体的插入
        insert_sql = """
                    insert into cnblogs_article(title, url,url_object_id,front_image_url,front_image_path,praise_nums,comment_nums, fav_nums, tags, content, create_date)
                    VALUES (%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s) ON DUPLICATE KEY UPDATE praise_nums=VALUES(praise_nums)
                """
        params = list()
        params.append(item.get("title", ""))
        params.append(item.get("url", ""))
        params.append(item.get("url_object_id", ""))
        front_images = ','.join(item.get("front_image_url", []))
        params.append(front_images)
        params.append(item.get("front_image_path", ""))
        params.append(item.get("praise_nums", 0))
        params.append(item.get("comment_nums", 0))
        params.append(item.get("fav_nums", 0))
        params.append(item.get("tags", ""))
        params.append(item.get("content", ""))
        params.append(item.get("create_date", "1970-07-01"))
        cursor.execute(insert_sql, tuple(params))
