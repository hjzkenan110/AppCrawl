# -*- coding: utf-8 -*-
import scrapy


class QimaiSpider(scrapy.Spider):
    name = 'qimai'
    allowed_domains = ['www.qimai.com']
    start_urls = ['http://www.qimai.com/']

    def parse(self, response):
        pass
