# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from MovieCommentSpider.items import MoviecommentspiderItem


# 爬取《数码宝贝:最后的进化》200条短评
class MoviecommentSpider(scrapy.Spider):
    name = 'moviecomment'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/subject/30482645']

    def start_requests(self):
        for i in range(0, 9):
            url = f'https://movie.douban.com/subject/30482645/comments?start={i*20}&limit=20'
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        comments = Selector(response=response).xpath('//*[@class="comment"]')
        for comment in comments:
            item = MoviecommentspiderItem()
            # 判断是否有评分，有评分则有三个span，没评分则两个span
            i = 3 if comment.xpath('./h3/span[2]/span[3]') else 2
            item['star'] = comment\
                    .xpath('./h3/span[2]/span[2]/@title')\
                    .extract_first() \
                    if i == 3 else ''  # 没有评分，内容则为空
            item['comment_time'] = comment\
                    .xpath(f'./h3/span[2]/span[{i}]/text()')\
                    .extract_first()\
                    .strip()
            item['short'] = comment.xpath('./p/span/text()').extract_first().strip()
            yield item
