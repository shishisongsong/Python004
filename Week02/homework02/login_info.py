# 登陆页面需要的信息
from fake_useragent import UserAgent

# 登陆url
login_url = 'https://processon.com/login?f=index'

# 请求头
ua = UserAgent(verify_ssl=False)
headers = {
    'User-Agent': ua.random,
    'Referer': 'https://processon.com/'
}

# 登陆账号与密码
form_data = {
    'login_email': '441807469@qq.com',
    'login_password': '********'
}