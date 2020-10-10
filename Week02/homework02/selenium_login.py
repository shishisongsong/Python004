# 使用selenium模拟登陆processon
from selenium import webdriver
from time import sleep
from login_info import login_url, headers, form_data

# 登陆函数
def login(login_url, headers, form_data):
    with webdriver.Chrome() as broswer:
        # get请求登陆页面
        broswer.get(login_url)
        sleep(1)
        
        # 找到账户密码输入框，并输入密码
        broswer.find_element_by_xpath('//*[@id="login_email"]').send_keys(form_data['login_email'])
        broswer.find_element_by_xpath('//*[@id="login_password"]').send_keys(form_data['login_password'])
        sleep(1)

        # 点击登陆
        broswer.find_element_by_xpath('//*[@id="signin_btn"]').click()
        sleep(1)

        print(broswer.page_source)

if __name__ == "__main__":
    login(login_url, headers, form_data)
