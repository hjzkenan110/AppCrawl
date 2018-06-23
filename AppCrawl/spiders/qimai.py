# -*- coding: utf-8 -*-
import json

import scrapy
from AppCrawl.utils.qimai_api_get import GetDynamicAPI

class QimaiSpider(scrapy.Spider):
    name = 'qimai'
    url = GetDynamicAPI("2018-06-20", 1).main()
    start_urls = [url]

    def parse(self, response):
        print(response.body)
