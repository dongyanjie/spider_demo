# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# 书籍信息
class ToscrapeBookItem(scrapy.Item):
    upc = scrapy.Field()  # 产品编码
    name = scrapy.Field()  # 书名
    price = scrapy.Field()  # 价格
    stock = scrapy.Field()  # 库存量
    review_rating = scrapy.Field()  # 评价等级
    review_num = scrapy.Field()  # 评价数量


# 名人名言
class QuotesItem(scrapy.Item):
    quote = scrapy.Field()  # 名言
    author = scrapy.Field()  # 作者
