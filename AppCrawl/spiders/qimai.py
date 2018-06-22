# -*- coding: utf-8 -*-
import scrapy


class QimaiSpider(scrapy.Spider):
    name = 'qimai'
    allowed_domains = ['https://www.qimai.cn/rank/release']
    #start_urls = ['http://https://www.qimai.cn/rank/release/']

    def parse(self, response):
        pass
