# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pandas


class Homework2Pipeline:
    # def process_item(self, item, spider):
    #     return item
    def process_item(self, item, spider):
        maoyan_movie = pandas.DataFrame(data=item['film_info_list'])
        maoyan_movie.to_csv('./maoyan_movie.csv', encoding="utf8", index=False, header=False)
