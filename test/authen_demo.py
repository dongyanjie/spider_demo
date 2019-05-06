import requests
from requests.auth import AuthBase

URL = 'https://api.github.com'


def build_uri(endpoint):
    return '/'.join([URL, endpoint])


def base_auth():
    # 基本认证
    response = requests.get(build_uri('user'), auth=('username', 'password'))
    print(response.text)
    print(response.request.headers)
    print(response.status_code)


# 面向对象方式认证
class GithubAuth(AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        # requests 加headers
        r.headers['Authorization'] = ' '.join(['token', self.token])
        return r


def oauth_advanced():
    # 我的信息token
    auth = GithubAuth('46f1e990879c3107f2b03c87610a0dd0e6ebf301')
    # user/emails
    response = requests.get(build_uri('user/emails'), auth=auth)
    print(response.text)
    print(response.request.headers)
    print(response.status_code, response.reason)


if __name__ == '__main__':
    # base_auth()
    oauth_advanced()
