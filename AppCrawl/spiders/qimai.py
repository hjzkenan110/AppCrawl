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
            yield scrapy.Request(url, meta={"nowPage":1, "nowDate":date})

    def parse(self, response):
        app_info = json.loads(response.text)
        maxPage, nowPage = int(app_info["maxPage"]), int(self.response.meta["nowPage"])
        
        if (maxPage > nowPage):
            nowPage += 1
            c1 = GetDynamicAPI(middle_url = "/rank/release", genre = "36", page=nowPage)
            yield scrapy.Request(url = c1.get_url(), meta={"nowPage":nowPage, "nowDate":date})
        
