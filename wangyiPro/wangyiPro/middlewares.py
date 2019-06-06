# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

from time import sleep

from scrapy.http import HtmlResponse
class WangyiproDownloaderMiddleware(object):

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None
    #该方法可以拦截到所有的响应对象（需求中需要处理的是指定的某些响应对象）
    def process_response(self, request, response, spider):
        #找出指定的响应对象进行处理操作
        #可以根据指定的请求对象定位到指定的响应对象
        #指定的请求对象可以通过请求的url进行定位
        #定位指定的url？ spider.model_urls
        model_urls = spider.model_urls
        bro = spider.bro
        if request.url in model_urls:
            #通过指定的url就定位到了指定的request
            #通过指定的request定位到指定的response（不符合需求的要求）
            #自己手动的创建四个符合需求要求的新的响应对象（需要将符合要求的响应数据存储放置到新的响应对象中）
            #使用新的响应对象替换原来原始的响应对象
            bro.get(request.url)  #使用浏览器对四个板块对应的url发起请求
            sleep(2)
            js = 'window.scrollTo(0,document.body.scrollHeight)'
            bro.execute_script(js)
            sleep(2)
            #页面源码数据中就包含了动态加载出来的新闻数据
            page_text = bro.page_source

            #手动创建一个新的响应对象，将page_text作为响应数据封装到改响应对象中
            #body参数表示的就是响应数据
            return HtmlResponse(url=bro.current_url, body=page_text, encoding='utf-8', request=request)


        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

