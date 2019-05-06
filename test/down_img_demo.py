import requests


# demo: 下载图片，文件
def download_image():
    # 伪造header信息
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
    # 限定url
    url = 'http://cdn.ifanr.cn/wp-content/uploads/2014/06/github.png'
    # 以流方式打开
    response = requests.get(url, headers=headers, stream=True)
    print(response.status_code, response.reason)
    # 打开文件
    with open('demo.jpg', 'wb') as f:
        # 每128写入一次
        for chunk in response.iter_content(128):
            f.write(chunk)


def download_image_improved():
    # 伪造header信息
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
    # 限定url
    url = 'http://hbimg.b0.upaiyun.com/72793a0808bb1e0f73e84b32ba0d77b862a52fc318979-hS3o7b_fw658'

    from contextlib import closing
    # 以流方式打开，打开传输流后 用完自动关闭
    with closing(requests.get(url, headers=headers, stream=True)) as response:
        # 打开文件
        with open('demo.jpg', 'wb') as f:
            # 每128写入一次
            for chunk in response.iter_content(128):
                f.write(chunk)

    print(response.status_code, response.reason)


if __name__ == '__main__':
    # download_image()
    download_image_improved()
