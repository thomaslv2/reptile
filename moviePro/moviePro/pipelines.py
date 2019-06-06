# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class MovieproPipeline(object):
    def process_item(self, item, spider):
        conn = spider.conn
        dic = {
            'name':item['name'],
            'm_type':item['m_type']
        }
        conn.lpush('movie_data',dic)
        return item
