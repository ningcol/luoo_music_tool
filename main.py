import os
from time import sleep

import requests
from retrying import retry

requests.adapters.DEFAULT_RETRIES = 5 # 增加重连次数


@retry(stop_max_attempt_number=10, wait_random_min=1000, wait_random_max=3000)
def get_url(time, index):
    url = 'http://mp3-cdn2.luoo.net/low/luoo/radio{}/{}.mp3'.format(time, index)
    s = requests.session()
    r = s.get(url)
    s.keep_alive = False
    if r.status_code == 200:
        download(url, r.content)
        print('完成:' + url)
        return url
    return ''

def download(url, content):
    name = url.rsplit('/', 1)[1]
    folder = url.rsplit('/', 2)[1]

    folder_url = '/Users/ningcol/Desktop/luoo/download/' + folder
    isExists=os.path.exists(folder_url)
    if not isExists:
        os.makedirs(folder_url)
        print(folder_url + '  创建成功')
    with open(folder_url + '/' + name, "wb") as code:
        code.write(content)


def prase_index(time, index):
    url = get_url(time, index)
    if len(url) == 0:
        index_str = str(index).zfill(2)
        url = get_url(time, index_str)
    return url, index


def run(time, index):
    url, index = prase_index(time, index)
    if len(url) == 0:
        time = time + 1
        index = 1
        run(time, index)
    else:
        run(time, int(index) + 1)



if __name__ == '__main__':
    time = 1
    index = 1
    run(time, index)