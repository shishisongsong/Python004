# -*- coding: utf-8 -*-
import scrapy
from maoyanspider.items import MaoyanspiderItem
from bs4 import BeautifulSoup
from scrapy.selector import Selector


class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films']

    def parse(self, response):
        try:
            bs_info = BeautifulSoup(response.text, 'html.parser')
            for tags in bs_info.find_all('div', attrs={'class': 'movie-item film-channel'}, limit=10):
                item = MaoyanspiderItem()
                movie_info = Selector(text=str(tags)).xpath('//*[@class="movie-item-hover"]')
                item['film_name'] = movie_info.xpath('./a/div/div[1]/span/text()').extract_first()
                item['film_type'] = movie_info.xpath('./a/div/div[2]/text()').extract()[1].strip()
                item['film_date'] = movie_info.xpath('./a/div/div[4]/text()').extract()[1].strip()
                yield item
        except Exception as e:
            print(e)
