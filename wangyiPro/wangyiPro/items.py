# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WangyiproItem(scrapy.Item):
    # define the fields for your item here like:
    new_title = scrapy.Field()
    new_content = scrapy.Field()
