# _*_ coding: utf-8 _*_
# @Time     : 2020/10/24 2:30
# @Author   : Peter
import re
import json
from urllib import parse

import scrapy
from scrapy import Selector
from scrapy import Request
import requests

from ArticleSpider.items import CnBlogsArticleItem
from ArticleSpider.utils import common



class CnblogsSpider(scrapy.Spider):
    name = 'cnblogs'
    allowed_domains = ['news.cnblogs.com']
    start_urls = ['https://news.cnblogs.com/']

    def parse(self, response):
        # 1.xpath
        # url = response.xpath('//*[@id="entry_675694"]/div[2]/h2/a/@href').extract_first("")
        # url = response.xpath('//div[@id="news_list"]/div[1]/div[2]/h2/a/@href').extract_first("")
        # url = response.xpath('//div[@id="news_list"]//h2[@class="news_entry"]/a/@href').extract_first("")

        # 2. css selector
        # url = response.css('div#news_list h2.news_entry a::attr(href)').extract()

        # 3.通过Selector来实现，需要导入from scrapy import Selector,主要是为了自己使用方便，建议还是使用1,2
        # sel = Selector(text=response.text)
        # url = response.css('div#news_list h2.news_entry a::attr(href)').extract()

        """
        # 1. 获取文章列表页中的文章url并交给scrapy下载后并进行解析
        # 2. 获取下一页的url并交给scrapy进行下载， 下载完成后交给parse
        :param response:
        :return:
        """
        # urls = response.css('div#news_list h2.news_entry a::attr(href)').extract()
        # post_nodes = response.css('#news_list .news_block')  # div#news_list div.news_block
        # post_nodes = response.xpath('//div[@id="news_list"]/div[@class="news_block"]')
        post_nodes = response.xpath('//div[@id="news_list"]/div[@class="news_block"]')[:1]   # debug时候用

        for post_node in post_nodes:
            # image_url = post_node.css('.entry_summary a img::attr(src)').extract_first("")
            # post_url = post_node.css('h2.news_entry  a::attr(href)').extract_first("")
            image_url = post_node.xpath('.//div[@class="entry_summary"]/a/img/@src').extract_first("")
            post_url = post_node.xpath('.//h2[@class="news_entry"]/a/@href').extract_first("")
            # 获取文章列表页中的文章url并交给scrapy下载后并进行解析,此时会生成一个request，交给scrapy进行处理, 爬取帖子详情页
            yield Request(url=parse.urljoin(response.url, post_url), meta={'front_image_url': image_url},
                          callback=self.parse_detail)

        # 提取下一页并交给scrapy进行下载
        # 获取分页中的最后一个a标签，判断它的值是否为Next
        # 方便调试，可以把post_nodes的代码注释掉
        # css方式
        # next_url = response.css('div.pager a:last-child::text').extract_first("")
        # if next_url == 'Next >':
        #     next_url = response.css('div.pager a:last-child::attr(href)').extract_first("")
        #     yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse)
        # xpath方式
        # next_url = response.xpath('//div[@class=pager]//a[contains(text(),"Next >"]').extract_first("")

        # debug的时候可以注释掉
        # next_url = response.xpath('//a[contains(text(),"Next >")]/@href').extract_first("")  # 获取a标签中的值包含Next >的并获取href
        # if next_url:
        #     yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    def parse_by_css(self, response):
        # 1.xpath
        # url = response.xpath('//*[@id="entry_675694"]/div[2]/h2/a/@href').extract_first("")
        # url = response.xpath('//div[@id="news_list"]/div[1]/div[2]/h2/a/@href').extract_first("")
        # url = response.xpath('//div[@id="news_list"]//h2[@class="news_entry"]/a/@href').extract_first("")

        # 2. css selector
        # url = response.css('div#news_list h2.news_entry a::attr(href)').extract()

        # 3.通过Selector来实现，需要导入from scrapy import Selector,主要是为了自己使用方便，建议还是使用1,2
        # sel = Selector(text=response.text)
        # url = response.css('div#news_list h2.news_entry a::attr(href)').extract()

        """
        # 1. 获取文章列表页中的文章url并交给scrapy下载后并进行解析
        # 2. 获取下一页的url并交给scrapy进行下载， 下载完成后交给parse
        :param response:
        :return:
        """

        post_nodes = response.css('#news_list .news_block')  # div#news_list div.news_block
        for post_node in post_nodes:
            image_url = post_node.css('.entry_summary a img::attr(src)').extract_first("")
            post_url = post_node.css('h2.news_entry  a::attr(href)').extract_first("")
            # 获取文章列表页中的文章url并交给scrapy下载后并进行解析,此时会生成一个request，交给scrapy进行处理, 爬取帖子详情页
            yield Request(url=parse.urljoin(response.url, post_url), meta={'front_image_url': image_url},
                          callback=self.parse_detail)

        # 提取下一页并交给scrapy进行下载
        # 获取分页中的最后一个a标签，判断它的值是否为Next
        next_url = response.css('div.pager a:last-child::text').extract_first("")
        if next_url == 'Next >':
            next_url = response.css('div.pager a:last-child::attr(href)').extract_first("")
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    def parse_detail(self, response):
        match_re = re.match(".*?(\d+)", response.url)

        if match_re:
            article_item = CnBlogsArticleItem()
            post_id = match_re.group(1)
            title = response.xpath('//*[@id="news_title"]//a/text()').extract_first("")
            create_date = response.xpath('//*[@id="news_info"]//*[@class="time"]/text()').extract_first("")
            # 提取时间
            match_re = re.match(".*?(\d+.*)", create_date)
            if match_re:
                create_date = match_re.group(1)

            content = response.xpath('//*[@id="news_content"]').extract()[0]  # 内容一般保存html
            tag_list = response.xpath('//*[@class="news_tags"]//a/text()').extract()
            tags = ",".join(tag_list)  # mysql存储的时候，用逗号隔开

            # 同步请求代码，在并发要求不是很高时可以采用,建议采用异步，yield方式
            # html = requests.get(parse.urljoin(response.url, "/NewsAjax/GetAjaxNewsInfo?contentId={}".format(post_id)))
            # j_data = json.loads(html.text)
            # praise_nums = j_data["DiggCount"]
            # fav_nums = j_data["TotalView"]
            # comment_nums = j_data["CommentCount"]

            article_item['url'] = response.url
            article_item['title'] = title
            article_item['create_date'] = create_date
            article_item['content'] = content
            article_item['tags'] = tags
            # 报错：ValueError:Missing scheme in request url:h
            # 上述报错原因：对于图片下载的字段一定要使用list类型，故[response.meta.get("front_image_url", "")]
            if response.meta.get("front_image_url", ""):
                article_item["front_image_url"] = [response.meta.get("front_image_url", "")]
            else:
                article_item["front_image_url"] = []

            yield Request(url=parse.urljoin(response.url, "/NewsAjax/GetAjaxNewsInfo?contentId={}".format(post_id)),
                          meta={'article_item': article_item},
                          callback=self.parse_nums)

    def parse_detail_by_css(self, response):
        match_re = re.match('.*?(\d+)', response.url)
        if match_re:
            article_item = CnBlogsArticleItem()
            post_id = match_re.group(1)
            title = response.css('#news_title a::text').extract_first("")
            create_date = response.css('#news_info .time::text').extract_first("")
            # 提取时间
            match_re = re.match(".*?(\d+.*)", create_date)
            if match_re:
                create_date = match_re.group(1)

            content = response.css('#news_content').extract()[0]  # 内容一般保存html
            tag_list = response.css(".news_tags a::text").extract()
            tags = ",".join(tag_list)  # mysql存储的时候，用逗号隔开

            # 同步请求代码，在并发要求不是很高时可以采用,建议采用异步，yield方式
            # html = requests.get(parse.urljoin(response.url, "/NewsAjax/GetAjaxNewsInfo?contentId={}".format(post_id)))
            # j_data = json.loads(html.text)
            # praise_nums = j_data["DiggCount"]
            # fav_nums = j_data["TotalView"]
            # comment_nums = j_data["CommentCount"]

            article_item['url'] = response.url
            article_item['title'] = title
            article_item['create_date'] = create_date
            article_item['content'] = content
            article_item['tags'] = tags
            article_item['front_image_url'] = response.meta.get('front_image_url', '')

            yield Request(url=parse.urljoin(response.url, "/NewsAjax/GetAjaxNewsInfo?contentId={}".format(post_id)),
                          meta={'article_item': article_item},
                          callback=self.parse_nums)

    def parse_nums(self, response):
        j_data = json.loads(response.text)
        article_item = response.meta.get('article_item', '')
        praise_nums = j_data["DiggCount"]
        fav_nums = j_data["TotalView"]
        comment_nums = j_data["CommentCount"]
        article_item['praise_nums'] = praise_nums
        article_item['fav_nums'] = fav_nums
        article_item['comment_nums'] = comment_nums
        article_item['url_object_id'] = common.get_md5(article_item['url'])

        yield article_item  # yield这个数据，此时pipeline会去处理,需要在settings配置pipeline



