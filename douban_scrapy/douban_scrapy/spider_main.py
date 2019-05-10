from scrapy import cmdline

# 直接解析到json文件中
# cmdline.execute('scrapy crawl douban_spider -o douban.json'.split())

# 执行pipelines.py里的Pipeline
cmdline.execute('scrapy crawl douban_spider'.split())

# 指定 spider名字%(name)s 和 爬取时间%(time)s 为目录
# cmdline.execute('scrapy crawl douban_spider -o "export_data/%(name)s/%(time)s.csv"'.split())
