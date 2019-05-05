from baike_spider import url_manager
from baike_spider import html_downloader
from baike_spider import html_parser
from baike_spider import html_outputer


# 爬虫主程序
class SpiderMain(object):
    def __init__(self):
        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOutputer()

    # 爬虫调度程序
    def craw(self, root_url):
        count = 1
        self.urls.add_new_url(root_url)
        # 判断url是否已存在，避免重复抓取
        while self.urls.has_new_url():
            try:
                new_url = self.urls.get_new_url()
                print("craw %d : %s" % (count, new_url))

                # 下载页面
                html_cont = self.downloader.download(new_url)
                # 解析页面
                new_urls, new_data = self.parser.paser(new_url, html_cont)
                # 将新的url补充进url管理器
                self.urls.add_new_urls(new_urls)
                # 收集数据
                self.outputer.collect_data(new_data)

                # 只爬取20条数据
                if count == 20:
                    break
                count = count + 1
            except:
                print('craw failed')
        self.outputer.output_html()


# 爬虫入口文件
if __name__ == '__main__':
    root_url = "http://baike.baidu.com/view/21087.htm"
    obj_spider = SpiderMain()
# 启动爬虫
    obj_spider.craw(root_url)
