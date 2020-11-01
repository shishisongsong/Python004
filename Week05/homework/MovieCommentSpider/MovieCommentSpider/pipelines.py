# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pandas as pd
from scrapy.utils.project import get_project_settings


class MoviecommentspiderPipeline:
    def open_spider(self, spider):
        self.comment_list = []
        settings = get_project_settings()
        self.file_path = settings.get('FILE_PATH')

    def process_item(self, item, spider):
        self.comment_list.append((item['star'], item['comment_time'], item['short']))
        return item

    def close_spider(self, spider):
        df = pd.DataFrame(data=self.comment_list)
        df.to_csv(self.file_path, encoding='utf-8', index=False, header=False)
