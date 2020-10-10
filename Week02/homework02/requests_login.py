# 使用requests模拟登陆processon
import requests
from login_info import login_url, headers, form_data

# 模拟登陆函数
def login(login_url, headers, form_data):
    with requests.Session() as s:
        # 先get请求一次登陆页面，得到cookies
        s.get(url=login_url, headers=headers)
        # 正式登陆
        resp = s.post(url=login_url, data=form_data, headers=headers)
        print(resp.text)

if __name__ == "__main__":
    login(login_url, headers, form_data)
