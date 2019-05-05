import requests

URL_IP = 'http://www.httpbin.org/ip'
URL_GET = 'http://www.httpbin.org/get'


def use_simple_requests():
    response = requests.get(URL_IP)
    print(response.headers)
    print(response.text)


def use_params_requests():
    # 构建请求参数
    params = {'param1': 'hello', 'param2': 'world'}
    # 发送请求
    response = requests.get(URL_GET, params=params)
    # 处理响应
    print(response.headers)
    print(response.status_code, response.reason)

    print(response.json())


if __name__ == '__main__':
    print('>>>use simple requests')
    use_simple_requests()
    print('>>>use params requests')
    use_params_requests()
