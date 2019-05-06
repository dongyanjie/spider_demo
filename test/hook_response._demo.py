# -*- coding:utf-8 -*-
import requests


# 钩子函数
def get_key_info(response, *args, **kwargs):
    # 回调函数
    print(response.headers['Content-Type'])


# 主程序
def hook_main():
    requests.get('https://api.github.com', hooks=dict(response=get_key_info))


if __name__ == '__main__':
    hook_main()
