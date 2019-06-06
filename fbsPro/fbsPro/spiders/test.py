# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_redis.spiders import RedisCrawlSpider
from fbsPro.items import FbsproItem
class TestSpider(RedisCrawlSpider):
    name = 'test'
    # allowed_domains = ['www.xxx.com']
    # start_urls = ['http://www.xxx.com/']
    #调度器队列的名称
    redis_key = 'dongguan'
    rules = (
        Rule(LinkExtractor(allow=r'type=4&page=\d+'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        a_list = response.xpath('//a[@class="news14"]')
        for a in a_list:
            item = FbsproItem()
            item['title']= a.xpath('./text()').extract_first()

            yield item
