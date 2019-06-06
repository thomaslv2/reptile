# -*- coding: utf-8 -*-
import scrapy
from qiubaiPro.items import QiubaiproItem
import hashlib
from redis import Redis
class QiubaiSpider(scrapy.Spider):
    name = 'qiubai'
    conn = Redis(host='127.0.0.1',port=6379)
    # allowed_domains = ['www.xxx.com']
    start_urls = ['https://www.qiushibaike.com/text/']

    def parse(self, response):
        div_list = response.xpath('//div[@id="content-left"]/div')
        for div in div_list:
            #数据指纹：爬取到一条数据的唯一标识
            author = div.xpath('./div/a[2]/h2/text() | ./div/span[2]/h2/text()').extract_first()
            content = div.xpath('./a/div/span//text()').extract()
            content = ''.join(content)

            item = QiubaiproItem()
            item['author'] = author
            item['content'] = content

            #数据指纹的创建
            data = author+content
            hash_key = hashlib.sha256(data.encode()).hexdigest()
            ex = self.conn.sadd('hash_keys',hash_key)
            if ex == 1:
                print('有新数据更新......')
                yield item
            else:
                print('无数据更新！')




