import scrapy
from scrapy import Selector


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
        sel = Selector(text=response.text)
        url = response.css('div#news_list h2.news_entry a::attr(href)').extract()
        pass
