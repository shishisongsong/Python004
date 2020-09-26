# -*- coding: utf-8 -*-
import scrapy
from homework2.items import Homework2Item
import lxml.etree
from bs4 import BeautifulSoup as bs


class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films']

    def parse(self, response):
        # 通过返回结果生成bs对象
        bs_info = bs(response.text, "html.parser")
        
        # 构建item对象
        item = Homework2Item()
        film_info_list = []
        item['film_info_list'] = film_info_list

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
            
            film_info_list.append([film_name, film_type, film_date])

        yield item

            
