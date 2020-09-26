# 从猫眼爬取前10个电影的名称、类型和上映时间
# 并以UTF-8字符集保存到csv格式的文件中

import requests
from bs4 import BeautifulSoup as bs
import lxml.etree
import pandas as pd
import random

# 各种user-agent和代理
user_agents = ["Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Safari/535.19",
            "Mozilla/5.0 (Linux; U; Android 4.0.4; en-gb; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
            "Mozilla/5.0 (Linux; U; Android 2.2; en-gb; GT-P1000 Build/FROYO) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
            "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0",
            "Mozilla/5.0 (Android; Mobile; rv:14.0) Gecko/14.0 Firefox/14.0",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36",
            "Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19",
            "Mozilla/5.0 (iPad; CPU OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3",
            "Mozilla/5.0 (iPod; U; CPU like Mac OS X; en) AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/3A101a Safari/419.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"]
proxies = [{"http": "104.129.196.147:8800"},
        {"http": "175.43.59.47:9999"},
        {"http": "104.129.192.197:8800"},
        {"http": "104.129.196.86:8800"},
        {"http": "180.97.33.93:80"}]

# request头部
user_agent = random.choice(user_agents)
cookie = '''uuid_n_v=v1; uuid=64A646F0FF4011EA805853CB23A5B1A2517F1E5169FE4FC885E8554BBC368F1A; _csrf=9ae0e796b7c935484a58f3ec3cb495c5367b882dca4707b60d1b785a44cba6b6; _lxsdk_cuid=174c5cb353ec8-0a67fa66311015-31627403-13c680-174c5cb353e24; _lxsdk=64A646F0FF4011EA805853CB23A5B1A2517F1E5169FE4FC885E8554BBC368F1A; mojo-uuid=9a8de8ba92328a5cc0affefc04b8ec82; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1601046264; mojo-session-id={"id":"7d05ccc3738582de88240efec6d866ff","time":1601091753415}; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1601094188; __mta=146128139.1601046263870.1601094181982.1601094187916.11; mojo-trace-id=11; _lxsdk_s=174c8814f98-e80-cc6-8b2%7C%7C11'''
header = {"user-agent":user_agent, "cookie":cookie}

# 代理
proxy = random.choice(proxies)

# url
myurl = "https://maoyan.com/films?showType=3&offset=120"

# 请求结果
response = requests.get(myurl, headers=header, proxies=proxy)

# bs构建html解析器
bs_info = bs(response.text, "html.parser")
# print(response.text)

# # 本地测试
# with open("./test.htm") as f:
#     response_text = f.read()
# bs_info = bs(response_text, "html.parser")

movie_info_list = []  # 电影信息列表，写入csv的数据

# 查找前10个电影的信息
for tags in bs_info.find_all(name="div", attrs={"class":"movie-item film-channel"}, limit=10):
    # print(tags)
    # 将tags给HTML化
    selector = lxml.etree.HTML(str(tags))
    # 电影名称
    film_name = selector.xpath('//div[@class="movie-hover-info"]/div[1]/span[1]/text()')[0]
    # 电影类型
    film_type = selector.xpath('//div[@class="movie-hover-info"]/div[2]/text()')[1].strip()
    # 上映日期
    film_date = selector.xpath('//div[@class="movie-hover-info"]/div[4]/text()')[1].strip()
    
    print(film_name, film_type, film_date)

    movie_info_list.append([film_name, film_type, film_date])

# 写入csv文件中
movie_info = pd.DataFrame(data=movie_info_list)
movie_info.to_csv('./movie_info.csv', encoding='utf8', index=False, header=False)


