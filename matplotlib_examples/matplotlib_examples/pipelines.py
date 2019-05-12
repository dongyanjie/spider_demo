# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.files import FilesPipeline
from urllib.parse import urlparse
from os.path import basename, dirname, join


# 覆盖file_path方法来实现所期望的文件命名规则
# http://matplotlib.org/examples/（类别）/（文件名.py）
class MyFilesPipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None):
        path = urlparse(request.url).path
        return join(basename(dirname(path)), basename(path))


class MatplotlibExamplesPipeline(object):
    def process_item(self, item, spider):
        return item
