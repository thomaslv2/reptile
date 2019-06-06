# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from aip import AipNlp

APP_ID = '16206022'
API_KEY = 'gYdxoMCbG2MiAC0vLaf262A2'
SECRET_KEY = 'UEarziHffpLHcWVMmFU9Yk1Ptbvw6reS'
client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

class WangyinewsallPipeline(object):
    fp = None

    def open_spider(self, spider):
        # title = item['title']
        print(spider)
        self.fp = open('wangyinewsall/网易国内新闻/' + '国内新闻' + '.txt', 'wt', encoding='utf-8')

    def process_item(self, item, spider):
        title = item['title']
        desc = item['desc'].strip()
        # desc = item['desc'].replace('问：','\n问：').replace('答：','\n答：')
        self.fp.write(title + '\n' + desc + '\n----------------------------------------\n')
        return item

    def close_spider(self, spider):
        self.fp.close()


class MysqlPipeline(object):
    conn = None
    cursor = None
    count=0

    def open_spider(self, spider):
        self.conn = pymysql.Connect(host='127.0.0.1', port=3306, user='root', password='123', db='news')
        print(self.conn)

    def process_item(self, item, spider):
        keywords=''
        title = item['title']
        desc = item['desc'].strip()
        self.cursor = self.conn.cursor()


        keydic=client.keyword(title, desc)
        keyword_list=keydic.get('items','')

        for keyword in keyword_list:
            if keyword['score']>0.8:
                keywords=keywords+keyword['tag']+','

        tagdic=client.topic(title, desc)
        tag=tagdic.get('item','')['lv1_tag_list'][0]['tag']
        # print(keywords,tag)


        try:
            self.count+=1
            # print('走着了')
            # self.cursor.execute('insert into detailnews(title,content) values ("%s","%s")' % (title, desc))
            self.cursor.execute('insert into detailnews( id,title, keywords, type, content) VALUES ("%s","%s","%s","%s","%s")' % (self.count,title,keywords,tag, desc))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()
