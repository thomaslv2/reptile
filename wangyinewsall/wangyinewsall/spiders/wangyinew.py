# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from wangyinewsall.items import WangyinewsallItem


class WangyinewSpider(scrapy.Spider):
    option = ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    #创建一个浏览器对象
    bro=webdriver.Chrome(executable_path='D:\Jpyter_notebook_work\爬虫day06\wangyinewsall\wangyinewsall\spiders\chromedriver.exe',options=option)
    name = "wangyinew"
    # allowed_domains = ["www.asd.com"]
    start_urls = ['https://news.163.com/']
    models_url=[]

    def parse(self, response):
        model_li_list=response.xpath('//div[@class="ns_area list"]/ul/li')
        num_list=[3,4,6,7]
        for num in num_list[0:1]:
            model_url=model_li_list[num].xpath('./a/@href').extract_first()
            self.models_url.append(model_url)
            yield scrapy.Request(url=model_url,callback=self.title_parse)

    def title_parse(self, response):
        # page_text=response.text
        # with open('res.html','w',encoding='utf-8')as f:
        #     f.write(page_text)
        detailnews_div_list=response.xpath('//div[@class="ndi_main"]/div')
        # detailnews_div_list=response.xpath('//div[@class="ndi_main"]/div')
        # print(detailnews_div_list)
        for detailnews_div in detailnews_div_list[0:2]:
            title=detailnews_div.xpath('./div/div[1]/h3/a//text()').extract_first()
            detailnews_url=detailnews_div.xpath('./div/div[1]/h3/a//@href').extract_first()
            # print(title,detailnews_url)
            item=WangyinewsallItem()
            item['title']=title
            yield scrapy.Request(url=detailnews_url,callback=self.detail_parse,meta={'item':item})

    def detail_parse(self, response):
        item=response.meta['item']
        detail_list=response.xpath('//*[@id="endText"]/p//text()').extract()
        desc='\n'.join(detail_list)
        print(desc)
        item['desc']=desc
        # print(desc)
        yield item

    def closed(self,spider):
        self.bro.quit()




