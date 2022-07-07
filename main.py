import requests
import re
import time
from fake_useragent import UserAgent
from tqdm import tqdm

# 代理地址
proxies = {
    "http": "socks5://127.0.0.1:port",
    "https": "socks5://127.0.0.1:port",
}

# 标头
headers = {
    'user-agent': UserAgent(verify_ssl=False).random
}

headers2 = {'accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh-HK;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6',
            'referer': 'https://www.pixiv.net/',
            'sec-fetch-dest': 'image',
            'sec-fetch-mode': 'no-cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': UserAgent(verify_ssl=False).random,
            }

response_1 = requests.get("https://www.pixiv.net/ranking.php?mode=daily", headers=headers, proxies=proxies)
daily_list = response_1.text  # 获取pixiv日榜html文字

ID = re.findall('"data-type=".*?"data-id="(.*?)"', daily_list)  # 获取日榜图片id
# print(ID)

part = "https://www.pixiv.net/artworks/"  # 定义前缀

for site in tqdm(ID):
    URL = part + str(site)
    URL = URL.split(" ")  # URL转list
    '''得到图片页面网址'''
    for download in URL:
        response_2 = requests.get(download, headers=headers, proxies=proxies)
        html = response_2.text  # 获取图片展示页面html文字
        download_links = re.findall('"original":"(.*?)"}', html)  # 找到下载链接
        download_links = "".join(download_links)  # 转str

        # print(download_links)
        file_name = download_links.split('/')[-1]  # 链接反向切片得到文件名
        # print(file_name)
        time.sleep(5)  # 防ban
        requests.DEFAULT_RETRIES = 100  # 增加重连次数防报错
        s = requests.session()
        s.keep_alive = False  # 关闭多余连接
        r = requests.get(download_links, headers=headers2, proxies=proxies)
        with open('./pic/' + file_name, 'wb+') as f:  # 存
            f.write(r.content)
