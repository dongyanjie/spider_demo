# -*- coding: utf-8 -*-
import scrapy
from douban_scrapy.items import DoubanScrapyItem
# 提取链接的另一种方式
# from scrapy.linkextractors import LinkExtractor


class DoubanSpiderSpider(scrapy.Spider):
    name = 'douban_spider'
    allowed_domains = ['movie.douban.com']
    start_urls = ['http://movie.douban.com/top250']

    # 另一种方式
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    # }
    # def start_requests(self):
    #     url = 'https://movie.douban.com/top250'
    #     yield scrapy.Request(url, headers=self.headers)

    def parse(self, response):
        # 循环电影条目
        movie_list = response.xpath('//div[@class="article"]//ol[@class="grid_view"]/li')

        for i_item in movie_list:
            douban_item = DoubanScrapyItem()
            douban_item['number'] = i_item.xpath(".//div[@class='item']//em//text()").extract_first()
            douban_item['movie_name'] = i_item.xpath(
                ".//div[@class='info']/div[@class='hd']/a/span[@class='title']/text()").extract_first()
            content = i_item.xpath(".//div[@class='info']/div[@class='bd']/p[1]/text()").extract()
            for i_content in content:
                content_s = ''.join(i_content.split())
                douban_item['introduce'] = content_s
            douban_item['star'] = i_item.xpath(".//span[@class='rating_num']/text()").extract_first()
            douban_item['evaluate'] = i_item.xpath(".//div[@class='star']//span[4]/text()").extract_first()
            douban_item['describe'] = i_item.xpath(".//p[@class='quote']/span//text()").extract_first()

            yield douban_item

            # 构造下一页的请求
            for next_link in response.css('.paginator .next a::attr(href)').extract():
                if next_link:
                    url = response.urljoin(next_link)
                    print(url)
                    yield scrapy.Request(url=url, callback=self.parse)

            # # 提取链接的另一种方式
            # le = LinkExtractor(restrict_css='.paginator .next')
            # links = le.extract_links(response)
            # if links:
            #     next_url = links[0].url
            #     yield scrapy.Request(next_url, callback=self.parse)

