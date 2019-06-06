# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class BossproPipeline(object):
    f1,f2 = None,None
    def open_spider(self,spider):
        self.f1 = open('a.txt','w',encoding='utf-8')
        self.f2 = open('b.txt', 'w', encoding='utf-8')
    def process_item(self, item, spider):

        #item在同一时刻只可以接收到某一个指定item对象
        if item.__class__.__name__ == 'FirstItem':
            job_title = item['job_title']
            self.f1.write(job_title+'\n')
        else:
            job_desc = item['job_desc']
            self.f2.write(job_desc)
        return item
