# _*_ coding: utf-8 _*_
# @Time     : 2020/10/24 2:30
# @Author   : Peter

from urllib import parse

import scrapy
from scrapy import Selector
from scrapy import Request


class CnblogsSpider(scrapy.Spider):
    name = 'cnblogs'
    allowed_domains = ['news.cnblogs.com']
    start_urls = ['http://news.cnblogs.com/']

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
        post_nodes = response.xpath('//div[@id="news_list"]/div[@class="news_block"]')

        for post_node in post_nodes:
            # image_url = post_node.css('.entry_summary a img::attr(src)').extract_first("")
            # post_url = post_node.css('h2.news_entry  a::attr(href)').extract_first("")
            image_url = post_node.xpath('.//div[@class="entry_summary"]/a/img/@src').extract_first("")
            post_url = post_node.xpath('.//h2[@class="news_entry"]/a/@href').extract_first("")
            # 获取文章列表页中的文章url并交给scrapy下载后并进行解析,此时会生成一个request，交给scrapy进行处理, 爬取帖子详情页
            yield Request(url=parse.urljoin(response.url, post_url), meta={'front_image_url': image_url}, callback=self.parse_detail)

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
        next_url = response.xpath('//a[contains(text(),"Next >")]/@href').extract_first("")    # 获取a标签中的值包含Next >的并获取href
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)
        pass

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
            yield Request(url=parse.urljoin(response.url, post_url), meta={'front_image_url': image_url}, callback=self.parse_detail)

        # 提取下一页并交给scrapy进行下载
        # 获取分页中的最后一个a标签，判断它的值是否为Next
        next_url = response.css('div.pager a:last-child::text').extract_first("")
        if next_url == 'Next >':
            next_url = response.css('div.pager a:last-child::attr(href)').extract_first("")
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    def parse_detail(self, response):
        pass
