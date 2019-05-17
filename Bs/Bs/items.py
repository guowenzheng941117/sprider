# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BsItem(scrapy.Item):
    # 自如类型（合租、整租...）
    id = scrapy.Field()
    # 标题
    title = scrapy.Field()
    # 链接
    link = scrapy.Field()
    # 时间
    issueTime = scrapy.Field()
    type = scrapy.Field()
    stage = scrapy.Field()
    pass
