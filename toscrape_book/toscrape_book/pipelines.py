# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3
import pymysql
import redis
from scrapy import Item
from twisted.enterprise import adbapi


class ToscrapeBookPipeline(object):
    review_rating_map = {
        'One': 1,
        'Two': 2,
        'Three': 3,
        'Four': 4,
        'Five': 5,
    }
    # 英镑兑换人民币汇率
    exchange_rate = 8.5309

    def process_item(self, item, spider):
        # 转换汇率，提取price字段,如（£51.36），转换为float类型
        price = float(item['price'][1:]) * self.exchange_rate
        item['price'] = '￥%.2f' % price
        # 转换星级，如（One -- 1）
        rating = item.get('review_rating')
        if rating:
            item['review_rating'] = self.review_rating_map[rating]
        return item


# 保存到sqlite数据库中
class SQLitePipeline(object):
    def open_spider(self, spider):
        db_name = spider.settings.get('SQLITE_DB_NAME', 'scrapy_default.db')
        self.db_conn = sqlite3.connect(db_name)
        self.db_cur = self.db_conn.cursor()

    def close_spider(self, spider):
        self.db_conn.commit()
        self.db_conn.close()

    def process_item(self, item, spider):
        self.insert_db(item)

        return item

    def insert_db(self, item):
        values = (
            item['upc'],
            item['name'],
            item['price'],
            item['review_rating'],
            item['review_num'],
            item['stock'],
        )
        sql = 'INSERT INTO books VALUES (?,?,?,?,?,?)'
        self.db_cur.execute(sql, values)


# 保存到mysql数据库中
class MysqlPipeline(object):
    def open_spider(self, spider):
        db = spider.settings.get('MYSQL_DB_NAME', 'scrapy_default.db')
        host = spider.settings.get('MYSQL_HOST', 'localhost')
        port = spider.settings.get('MYSQL_PORT', 3306)
        user = spider.settings.get('MYSQL_USER', 'root')
        passwd = spider.settings.get('MYSQL_PASSWORD', '')

        self.db_conn = pymysql.connect(host=host, port=port, db=db, user=user, passwd=passwd, charset='utf8')
        self.db_cur = self.db_conn.cursor()

    def close_spider(self, spider):
        self.db_conn.commit()
        self.db_conn.close()

    def process_item(self, item, spider):
        self.insert_db(item)

        return item

    def insert_db(self, item):
        values = (
            item['upc'],
            item['name'],
            item['price'],
            item['review_rating'],
            item['review_num'],
            item['stock'],
        )
        sql = 'INSERT INTO books VALUES (%s,%s,%s,%s,%s,%s)'
        self.db_cur.execute(sql, values)


# 保存到mysql数据库中 （连接池方式）
class MysqlAsyncPipeline(object):
    def open_spider(self, spider):
        db = spider.settings.get('MYSQL_DB_NAME', 'scrapy_default.db')
        host = spider.settings.get('MYSQL_HOST', 'localhost')
        port = spider.settings.get('MYSQL_PORT', 3306)
        user = spider.settings.get('MYSQL_USER', 'root')
        passwd = spider.settings.get('MYSQL_PASSWORD', '')

        self.db_pool = adbapi.ConnectionPool('pymysql', host=host, db=db, user=user, passwd=passwd, charset='utf8')

    def close_spider(self, spider):
        self.db_pool.close()

    def process_item(self, item, spider):
        self.db_pool.runInteraction(self.insert_db, item)

        return item

    def insert_db(self, tx, item):
        values = (
            item['upc'],
            item['name'],
            item['price'],
            item['review_rating'],
            item['review_num'],
            item['stock'],
        )
        sql = 'INSERT INTO books VALUES (%s,%s,%s,%s,%s,%s)'
        tx.execute(sql, values)


# 保存到redis数据库中
class RedisPipeline(object):
    def open_spider(self, spider):
        index = spider.settings.get('REDIS_DB_INDEX', 0)
        host = spider.settings.get('REDIS_HOST', 'localhost')
        port = spider.settings.get('REDIS_PORT', 6379)

        self.db_conn = redis.StrictRedis(host=host, port=port, db=index)
        self.item_i = 0

    def close_spider(self, spider):
        self.db_conn.commit()
        self.db_conn.close()

    def process_item(self, item, spider):
        self.insert_db(item)

        return item

    def insert_db(self, item):
        if isinstance(item, Item):
            item = dict(item)

            self.item_i += 1
        self.db_conn.hmset('book:%s' % self.item_i, item)
