# -*- coding: utf-8 -*-
import scrapy
from wangyiPro.items import WangyiproItem
from selenium import webdriver
from selenium.webdriver import ChromeOptions
class WangyiSpider(scrapy.Spider):
    option = ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    #创建一个浏览器对象
    bro = webdriver.Chrome(executable_path=r'C:\Users\Administrator\Desktop\爬虫+数据\爬虫day06\chromedriver.exe',options=option)
    name = 'wangyi'

    start_urls = ['https://news.163.com/']model_urls = [] #放置的就是四个板块对应的详情页的url
    # allowed_domains = ['www.xxx.com']
    #专门用来解析新闻的内容：接收一下传递过来的item对象
    def newContent_parse(self,response):
        print('newContent_parse()')
        item = response.meta['item']
        #解析新闻内容，然后直接存储到item中
        content_list = response.xpath('//div[@id="endText"]//text()').extract()
        #extract返回的是列表，列表中存储的是字符串
        item['new_content'] = ''.join(content_list)

        yield item
    #用来解析板块对应页面中的新闻数据
    def parse_detail(self,response):
        print('parse_detail()')
        div_list = response.xpath('//div[@class="ndi_main"]/div')
        for div in div_list:
            #只解析到了新闻标题还没有解析到新闻的内容
            item = WangyiproItem()
            new_title = div.xpath('./div/div[1]/h3/a/text()').extract_first()
            new_detail_url = div.xpath('./div/div[1]/h3/a/@href').extract_first()
            item['new_title'] = new_title
            #获取新闻的内用:进行i请求传参，将item传递给下一个解析方法
            yield scrapy.Request(url=new_detail_url,callback=self.newContent_parse,meta={'item':item})
    def parse(self, response):
        print('parse()')
        #解析四个板块对应的url:只有在取文本或者取属性的时候才需要在path中调用extract操作
        li_list = response.xpath('//div[@class="ns_area list"]/ul/li')
        indexs = [3,4,6,7]
        model_li_list = [] #放置选出的四个板块对应的li
        for index in indexs:
            li = li_list[index]
            model_li_list.append(li)
        #解析出四个板块对应的url
        for li in model_li_list:
            model_url = li.xpath('./a/@href').extract_first()
            self.model_urls.append(model_url)
            #对每一个板块的url发起请求获取详情页的页面源码数据
            yield scrapy.Request(url=model_url,callback=self.parse_detail)
    def closed(self,spider):
        self.bro.quit()