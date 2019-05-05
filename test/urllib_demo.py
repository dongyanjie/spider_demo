import urllib.request
import urllib.parse

URL_IP = 'http://www.httpbin.org/ip'
URL_GET = 'http://www.httpbin.org/get'


def use_simple_urllib():
    response = urllib.request.urlopen(URL_IP)
    print(response.info())

    print(''.join([line for line in response.readlines()]))


def use_params_urllib():
    # 构建请求参数
    params = urllib.parse.urlencode({'param1': 'hello', 'param2': 'world'})
    print(params)
    # 发送请求
    response = urllib.request.urlopen('?'.join([URL_GET, '%s']) % params)
    # 处理响应
    print(response.info())
    print(response.getcode())

    print(''.join([line for line in response.readlines()]))


if __name__ == '__main__':
    print('>>>use simple urllib')
    use_simple_urllib()
    print('>>>use params urllib')
    use_params_urllib()
