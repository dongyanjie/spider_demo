import re
from urllib import request, parse
from bs4 import BeautifulSoup
import pymysql.cursors


# 获取数据库连接
connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='',
                             db='spider_test',
                             charset='utf8mb4',
                             )

resp = request.urlopen('http://baijiahao.baidu.com/s?id=1598585193192010665&wfr=spider&for=pc').read().decode('utf-8')
soup = BeautifulSoup(resp, 'html.parser')
links = soup.find_all('a', href=re.compile(r'^https://mbd.baidu.com'))

try:
    # 获取会话指针
    with connection.cursor() as cursor:
        for link in links:
            if link.get_text():
                print(link.get_text())
                # 创建sql语句
                sql = "INSERT INTO `urls` (`url_name`, `url_href`) VALUES (%s, %s)"
                # 执行sql语句
                cursor.execute(sql, (link.get_text(), link['href']))
                # 提交
                connection.commit()
finally:
    # 关闭
    connection.close()


# # 得到总记录数
# cursor.execute()
# # 查询下一行
# cursor.fetchone()
# 查询三条数据
# cursor.fetchmany(size=3)
# # 得到所有数据
# cursor.fetchall()
