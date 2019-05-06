import json
import requests
from requests import exceptions

URL = 'https://api.github.com'


def build_uri(endpoint):
    return '/'.join([URL, endpoint])


def better_print(json_str):
    return json.dumps(json.loads(json_str), indent=4)


def request_method():
    response = requests.get(build_uri('users/dongyanjie'))
    print(better_print(response.text))
    print(response.url)


def parpas_request():
    response = requests.get(build_uri('users'), params={'since': 11})
    print(better_print(response.text))
    print(response.url)


# 通过api修改个人信息
def json_request():
    response = requests.post(build_uri('user/emails'), auth=('username', 'password'), json=['hello@github.com'])
    print(better_print(response.text))
    print(response.headers)
    print(response.status_code)


def timeout_request():
    try:
        response = requests.get(build_uri('users/dongyanjie'), timeout=0.1)
    except exceptions.Timeout as e:
        raise ValueError(e.strerror)
    else:
        print(response.text)


# 自定义requests
def hard_requests():
    from requests import Request, Session
    s = Session()
    headers = {'User-Agent': 'fake1.3.4'}
    req = Request('GET', build_uri('users/dongyanjie'), headers=headers)
    # 准备 还未发出
    prepped = req.prepare()
    print(prepped.headers)
    print(prepped.body)
    print(prepped.url)
    # 发出请求
    resp = s.send(prepped, timeout=5)
    print(resp.status_code, resp.reason)
    print(resp.headers)
    print(resp.text)
    # print(resp.json())
    print('花费时间', resp.elapsed)


if __name__ == '__main__':
    # request_method()
    # parpas_request()
    # timeout_request()
    hard_requests()
