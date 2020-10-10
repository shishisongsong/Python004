# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from maoyanspider.mysql_conn_info import conn_info


class MaoyanspiderPipeline:
    def __init__(self):
        self.conn = pymysql.connect(**conn_info)
        self.cur = self.conn.cursor()
        self.not_commit = False  # 实例销毁时，mysql会执行commit
        self.insert_sql = '''\
            insert into film (name, type, date)
            values (%s, %s, %s)'''

    def process_item(self, item, spider):
        try:
           values = (item['film_name'], item['film_type'], item['film_date'])
           self.cur.execute(self.insert_sql, values)
        except Exception as e:
            print(e)
            self.not_commit = True  # 发生异常，实例销毁时不要提交

    def __del__(self):
        if not self.not_commit:
            self.conn.commit()
        else:
            self.conn.rollback()
        self.cur.close()
        self.conn.close()
        
