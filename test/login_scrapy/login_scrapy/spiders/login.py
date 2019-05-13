# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request, FormRequest


class LoginSpider(scrapy.Spider):
    name = 'login'
    allowed_domains = ['example.webscraping.com']
    start_urls = ['http://example.webscraping.com/places/default/user/profile']

    def parse(self, response):
        #         解析登陆后下载的页面，此例中为个人信息页面
        keys = response.css('table label::text').re('(.+):')
        values = response.css('table td.w2p_fw::text').extract()

        yield dict(zip(keys, values))

    # 登录页面的url
    login_url = 'http://example.webscraping.com/places/default/user/login'

    def start_requests(self):
        yield scrapy.Request(self.login_url, callback=self.login)

    def login(self, response):
        # 登录页面的解析函数，构造FormRequest 对象提交表单
        fd = {'email': '123@zxc.com', 'password': '123456'}
        yield FormRequest.from_response(response, formdata=fd, callback=self.parse_login)

    def parse_login(self, response):
        #         等录成功后，继续爬取start_urls中的页面
        if 'Welcome 1' in response.text:
            yield from super().start_requests()

