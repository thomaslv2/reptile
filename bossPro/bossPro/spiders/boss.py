# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from bossPro.items import DetailItem,FirstItem
#爬取的是岗位名称（首页）和岗位描述(详情页)
class BossSpider(CrawlSpider):
    name = 'boss'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['https://www.zhipin.com/c101010100/?query=python%E5%BC%80%E5%8F%91&page=1&ka=page-prev']
    #获取所有的页码连接
    link = LinkExtractor(allow=r'page=\d+')
    link_detail = LinkExtractor(allow=r'/job_detail/.*?html')
    #/job_detail/f2a47b2f40c53bd41XJ93Nm_GVQ~.html
    #/job_detail/47dc9803e93701581XN80ty7GFI~.html
    rules = (
        Rule(link, callback='parse_item', follow=True),
        Rule(link_detail, callback='parse_detail'),
    )
    #将页码连接对应的页面数据中的岗位名称进行解析
    def parse_item(self, response):
        li_list = response.xpath('//div[@class="job-list"]/ul/li')
        for li in li_list:
            item = FirstItem()
            job_title = li.xpath('.//div[@class="job-title"]/text()').extract_first()
            item['job_title'] = job_title
            # print(job_title)

            yield item
    def parse_detail(self,response):
        job_desc = response.xpath('//*[@id="main"]/div[3]/div/div[2]/div[2]/div[1]/div//text()').extract()
        item = DetailItem()
        job_desc = ''.join(job_desc)
        item['job_desc'] = job_desc

        yield item

