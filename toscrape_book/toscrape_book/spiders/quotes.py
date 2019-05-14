# -*- coding: utf-8 -*-
# 爬取名人名言
# splash ---JavaScript渲染引擎
import scrapy
from scrapy_splash import SplashRequest
from toscrape_book.items import QuotesItem


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/js']

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, args={'images': 0, 'timeout': 3})

    def parse(self, response):
        # 解析数据
        quotes_item = QuotesItem()
        for sel in response.css('div.quote'):
            quotes_item['quote'] = sel.css('span.text::text').extract_first()
            quotes_item['author'] = sel.css('small.author::text').extract_first()
            yield quotes_item

        # 解析下一页
        href = response.css('li.next>a::attr(href)').extract_first()
        if href:
            url = response.urljoin(href)
            yield SplashRequest(url, args={'images': 0, 'timeout': 3})
