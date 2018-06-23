# -*- coding: utf-8 -*-
import json
import datetime  

import scrapy
from AppCrawl.utils.qimai_api_get import GetDynamicAPI

class QimaiSpider(scrapy.Spider):
    name = 'qimai'

    def start_requests(self):
        page_time = datetime.datetime.now()
        
        for _ in range(1,10):
            page_time = page_time + datetime.timedelta(days=-1)
            date = page_time.strftime('%Y-%m-%d')
            url = GetDynamicAPI(date, 1).main()
            page=scrapy.Request(url)
            

    def parse(self, response):
        pass
