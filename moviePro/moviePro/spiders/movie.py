# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from redis import Redis
from moviePro.items import MovieproItem
class MovieSpider(CrawlSpider):
    conn = Redis(host='127.0.0.1',port=6379)
    name = 'movie'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['https://www.4567tv.tv/frim/index1.html']

    rules = (
        Rule(LinkExtractor(allow=r'/frim/index1-\d+\.html'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        #解析出当前页码对应页面中电影详情页的url
        li_list = response.xpath('//div[@class="stui-pannel_bd"]/ul/li')
        for li in li_list:
            #解析详情页的url
            detail_url = 'https://www.4567tv.tv'+li.xpath('./div/a/@href').extract_first()
            #ex == 1:该url没有被请求过  ex == 0:该url已经被请求过了
            ex = self.conn.sadd('movie_detail_urls',detail_url)
            if ex == 1:
                print('有新数据可爬取......')
                yield scrapy.Request(url=detail_url,callback=self.parse_detail)
            else:
                print('暂无新数据可爬取！')
    def parse_detail(self,response):
        name = response.xpath('/html/body/div[1]/div/div/div/div[2]/h1/text()').extract_first()
        m_type = response.xpath('/html/body/div[1]/div/div/div/div[2]/p[1]/a[1]/text()').extract_first()
        item = MovieproItem()
        item['name'] = name
        item['m_type'] = m_type

        yield item
