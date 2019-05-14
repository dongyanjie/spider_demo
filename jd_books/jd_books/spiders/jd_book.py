# -*- coding: utf-8 -*-

# 爬取京东商城中的书籍信息
import scrapy
from scrapy_splash import SplashRequest
from jd_books.items import JdBooksItem

# 调用 scrollIntoView(true) 完成拖拽动作
# 自定义的lua脚本， 逻辑： 打开页面->等待渲染->执行js触发数据加载->等待渲染->返回html
lua_script = '''
function main(splash)
    splash:go(splash.args.url)
    splash:wait(2)
    splash:runjs("document.getElementsByClassName('page')[0].scrollIntoView(true)")
    splash:wait(2)
    return splash:html()
end
'''


class JdBookSpider(scrapy.Spider):
    name = 'jd_book'
    allowed_domains = ['search.jd.com']
    # start_urls = ['http://search.jd.com/']
    base_url = 'https://search.jd.com/Search?keyword=python&enc=utf-8&book=y&wq=python'

    # 提交对第一个页面的请求
    def start_requests(self):
        # 请求第一页，无须js渲染
        yield scrapy.Request(self.base_url, callback=self.parse_urls, dont_filter=True)

    def parse_urls(self, response):
        # 获取商品总数，计算出总页数
        # total = int(float(response.css('span#J_resCount::text').extract_first()[:3]) * 10000)

        total = 1000   # 模拟爬取前1000本

        pageNum = total // 60 + (1 if total % 60 else 0)

        # 构造每页的url ,向Splash的execute端点发送请求
        for i in range(pageNum):
            url = '%s&page=%s' % (self.base_url, 2 * i + 1)
            yield SplashRequest(url,
                                endpoint='execuse',
                                args={'lua_source': lua_script},
                                cache_args=['lua_source'],
                                )

    def parse(self, response):
        # 获取一个页面中每本书的名字和价格
        i = 1
        for sel in response.css('ul.gl-warp.clearfix>li.gl-item'):

            if i < 1000:
                i += 1
                item = JdBooksItem()
                item['name'] = sel.css('div.p-name').xpath('.//em/text()').extract_first()
                item['price'] = sel.css('div.p-price i::text').extract_first()
                yield item
