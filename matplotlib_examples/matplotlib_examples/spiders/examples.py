# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from matplotlib_examples.items import MatplotlibExamplesItem


class ExamplesSpider(scrapy.Spider):
    name = 'examples'
    allowed_domains = ['matplotlib.org']
    start_urls = ['http://matplotlib.org/examples/index.html']

    def parse(self, response):
        # 抓取当前css下面的所有链接  deny= 排除.html结尾的文件
        le = LinkExtractor(restrict_css='div.toctree-wrapper.compound', deny='/index.html$')
        links = le.extract_links(response)
        print(len(links))  # 链接数量

        for link in links:
            yield scrapy.Request(link.url, callback=self.parse_examples)

    def parse_examples(self, response):
        # example = {}
        # example['file_urls'] = []
        href = response.css('li a.reference.internal::attr(href)').extract_first()
        url = response.urljoin(href)
        # 实例化一个对象
        example = MatplotlibExamplesItem()

        example['file_urls'] = [url]
        # example['file_urls'].append(url)

        return example
