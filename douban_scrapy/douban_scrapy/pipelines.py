# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem


class DoubanScrapyPipeline(object):

    def __init__(self):
        self.file = open('douban_top250.txt', mode='a')

    def process_item(self, item, spider):
        # return item
        number = item['number']
        movie_name = item['movie_name']
        introduce = item['introduce']
        star = item['star']
        evaluate = item['evaluate']
        describe = item['describe']
        line_data = number + ' ' + movie_name + ' ' + introduce + ' ' + star + ' ' + evaluate + ' ' + describe + '\n'

        if line_data:
            self.file.write(line_data)

    def close_spider(self, spider):
        self.file.close()


# 过滤重复数据
# class DuplicatesPipeline(object):
#     def __init__(self):
#         self.movie_set = set()
#
#     def process_item(self, item, spider):
#         movie_name = item['movie_name']
#         if movie_name in self.movie_set:
#             raise DropItem("duplicate movie found:%s" % item)
#         self.movie_set.add(movie_name)
#         return item
