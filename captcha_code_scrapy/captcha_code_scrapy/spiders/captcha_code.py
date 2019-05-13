# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request, FormRequest
import json
from PIL import Image
from io import BytesIO
import pytesseract
from scrapy.log import logger


class CaptchaCodeSpider(scrapy.Spider):
    name = 'captcha_code'
    allowed_domains = ['xxx.com']
    start_urls = ['http://xxx.com/']

    def parse(self, response):
        pass

    # 网站登录url
    login_url = 'http://xxx.com/login'
    user = 'xxx'
    password = '123456'

    def start_requests(self):
        yield Request(self.login_url, callback=self.login, dont_filter=True)

    # 该方法既是登录页面解析函数，也是下载验证码图片的相应处理函数
    def login(self, response):
        # 如果response.meta['login_response']存在，当前response为验证码图片的响应
        # 否则当前response为登录页面的响应
        login_response = response.meta.get('login_response')

        if not login_response:
            # 此时response 为登录页面的响应，从中提取验证码图片的url，下载验证码图片
            captchaUrl = response.css('label img::attr(src)').extract_first()
            captchaUrl = response.urljoin(captchaUrl)

            # 构造Request时，将当前response保存到meta字典中
            yield Request(captchaUrl, callback=self.login, meta={'login_response': response}, dont_filter=True)
        else:
            # 此时response 为验证码图片的响应，response.body是图片二进制数据
            # login_response为登录页面的响应，用其构造表单请求并发送
            formdata = {
                'email': self.user,
                'pass': self.password,
                'code': self.get_captcha_by_OCR(response.body)
            }
            yield FormRequest.from_response(login_response, callback=self.parse_login, formdata=formdata,
                                            dont_filter=True)

    def parse_login(self, response):
        # 根据响应结果判断是否登录成功
        info = json.loads(response.text)
        if info['error'] == '0':
            logger.info('登录成功')
            return super().start_requests()
        logger.info('登录失败')
        return self.start_requests()

    # ORM 识别验证码
    def get_captcha_by_OCR(self, data):
        img = Image.open(BytesIO(data))
        img = img.convent('L')
        captcha = pytesseract.image_to_string(img)
        img.close()
        return captcha

    # 人工识别
    def get_captcha_by_user(self, data):
        img = Image.open(BytesIO(data))
        img.show()
        captcha = input('输入验证码：')
        img.close()
        return captcha
