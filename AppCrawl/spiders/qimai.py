# -*- coding: utf-8 -*-
import json
import datetime  

import scrapy
from scrapy.http.cookies import CookieJar
from AppCrawl.utils.qimai_api_get import GetDynamicAPI, qimai_login, judge_login

AGENT = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
HEADER = {
    "HOST" : "api.qimai.cn",
    "Referer" : "https://www.qimai.cn/rank/release",
    'User-Agent' : AGENT,
    "Accept-Encoding" : "gzip, deflate, br",
    "Accept-Language" : "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
}


class QimaiSpider(scrapy.Spider):
    name = 'qimai'

    def start_requests(self):
        page_time = datetime.datetime.now()
        
        # for _ in range(1,10):
        # page_time = page_time + datetime.timedelta(days=-1)
        date = page_time.strftime('%Y-%m-%d')
        url = GetDynamicAPI(date=date, page=1, middle_url=1, genre=36).get_url()
        yield scrapy.Request(url, meta={"nowPage":1, "nowDate":date})

    def parse(self, response):
        page_info = json.loads(response.text)
        maxPage, nowPage = int(page_info["maxPage"]), response.meta["nowPage"]
        
        rank_info = page_info["rankInfo"]
        for app_info in rank_info:
            

        if (maxPage > nowPage):
            nowPage += 1
            login_result = judge_login()
            if login_result == True:
                with open('cook.txt', 'r') as f:
                    cookiejar = f.read()
                cookiejar = eval(cookiejar)
                yield scrapy.Request(url, meta={"nowPage":1, "nowDate":date})

            else:
                qimai_login("15816659260", "qm15382936271b")
                with open('cook.txt', 'r') as f:
                    cookiejar = f.read()
                cookiejar = eval(cookiejar)
                yield scrapy.Request(url=c1, meta={"nowPage":nowPage, "nowDate":response.meta["nowDate"]}, cookies = cookiejar, callback=self.parse)
        
