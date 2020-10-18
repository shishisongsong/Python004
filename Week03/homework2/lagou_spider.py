# 多线程使用selenium爬取拉勾网的各地区的python工程师的薪资情况
import threading
from selenium import webdriver
import time
import pymysql

class ConnDB(object):  # 连接数据库类
    def __init__(self, conn_info):
        self.conn = pymysql.connect(**conn_info)

    def insert_many(self, sql, data):
        cur = self.conn.cursor()
        try:
            cur.executemany(sql, data)
        except Exception as e:
            print(e)
            self.conn.rollback()
        finally:
            cur.close()
        self.conn.commit()

    def query(self, sql):
        cur = self.conn.cursor()
        cur.execute(sql)
        results = cur.fetchall()
        return results

    def __del__(self):
        self.conn.close()


class LagouThread(threading.Thread):  # 爬取线程类
    def __init__(self, city, job_num):
        super().__init__()
        self.city = city
        self.job_num = job_num

    def run(self):
        with webdriver.Chrome() as browser:  # 模拟谷歌浏览器访问
            # 请求指定城市的拉勾网
            url = f'https://www.lagou.com/jobs/list_python工程师?city={self.city}'
            browser.get(url)
            time.sleep(5)

            # 点击阻拦页面的红包弹框
            interrupt_bnt = browser.find_element_by_xpath('//*[@class="body-btn"]')
            if interrupt_bnt:
                interrupt_bnt.click()

            while 1:  # 循环，直到取到100个职位信息为止
                # 爬取职位信息
                job_info_ele_list = browser.find_elements_by_xpath(
                    '//*[@class="position"]'
                )
                for ele in job_info_ele_list:
                    # 职位名称
                    job_name = ele.find_element_by_xpath('./div/a/h3').text
                    # 地区
                    area = ele.find_element_by_xpath('./div/a/span/em').text
                    # 薪资
                    salary = ele.find_element_by_xpath('./div[2]/div/span').text
                    # 存入汇总字典中
                    job_info.add((self.city, job_name, area, salary))
                    # 若获取了指定数量的职位信息，则直接退出
                    self.job_num -= 1
                    if self.job_num == 0:
                        return
                time.sleep(1)
                
                # 点击下一页
                browser.find_element_by_xpath(
                    '//*[@class="pager_container"]/span[@action="next"]'
                ).click()
                time.sleep(2)


if __name__ == "__main__":
    city_name_list = ['北京', '上海', '广州', '深圳']  # 城市列表
    job_info = set()  # 最后的职位汇总信息, 集合用于去重
    lagou_threads = []  # 爬取线程的列表
    for c in city_name_list:
        t = LagouThread(c, 100)
        t.start()
        lagou_threads.append(t)

    # 阻塞主进程
    for t in lagou_threads:
        t.join()

    # 将数据存入到数据库中
    conn_info = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': '123qqq...A',
        'database': 'test',
        'charset': 'utf8mb4'
    }
    print(job_info)
    sql = 'insert into jobs (city, name, area, salary) values (%s, %s, %s, %s)'
    conn = ConnDB(conn_info)
    conn.insert_many(sql, job_info)