# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class CrawlSpider(CrawlSpider):
    name = 'c'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['https://www.qiushibaike.com/text/']
    #连接提取器：可以根据指定规则进行连接的提取
    #allow表示的就是提取连接规则：正则
    link = LinkExtractor(allow=r'')
    link1 = LinkExtractor(allow=r'/text/')
    rules = (
        #规则解析器：根据指定规则进行响应数据的解析
        #follow：将连接提取器继续作用到连接提取器提取出的连接所对应的页面源码中
        Rule(link, callback='parse_item', follow=True),
        Rule(link1, callback='parse_item'),
    )
    #回调函数调用的次数是由连接提取器提取连接个数决定
    def parse_item(self, response):
        print(response)
