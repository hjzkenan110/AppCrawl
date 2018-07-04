# -*- coding: utf-8 -*-
import datetime
import json
import time

import scrapy
from scrapy.http.cookies import CookieJar

from AppCrawl.items import qimaiItem, qimaiItemLoader
from AppCrawl.utils.qimai_api_get import (GetDynamicAPI, judge_login,
                                          qimai_login)

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
        yield scrapy.Request(url, meta={"nowDate":date})

    def parse(self, response):
        page_info = json.loads(response.text)
        maxPage = int(page_info["maxPage"])
        
        rank_info = page_info["rankInfo"]
        
        for info in rank_info:
            app_info = info["appInfo"]
            item_loader = qimaiItemLoader(item=qimaiItem(), response=response)
            item_loader.add_value("appId", app_info["appId"])
            item_loader.add_value("appName", app_info["appName"])
            item_loader.add_value("icon", app_info["icon"])
            item_loader.add_value("publisher", app_info["publisher"])
            item_loader.add_value("country", app_info["country"])
            item_loader.add_value("genre", info["genre"])
            item_loader.add_value("price", info["price"])
            item_loader.add_value("releaseTime", info["releaseTime"])

            qimai_item = item_loader.load_item()
            yield qimai_item

        if (maxPage > 1):
            login_result = judge_login()
            if login_result == True:
                with open('cook.txt', 'r') as f:
                    cookiejar = f.read()
                cookiejar = eval(cookiejar)

            else:
                qimai_login("15816659260", "qwe123")
                with open('cook.txt', 'r') as f:
                    cookiejar = f.read()
                cookiejar = eval(cookiejar)

            for nowPage in range(2, maxPage + 1):
                url = GetDynamicAPI(page=nowPage, middle_url=1, genre=36).get_url()
                time.sleep(3)
                yield scrapy.Request(url=url, headers=HEADER, cookies=cookiejar, callback=self.parse_detail)
        
    def parse_detail(self, response):
        page_info = json.loads(response.text)
        rank_info = page_info["rankInfo"]
        
        for info in rank_info:
            app_info = info["appInfo"]
            item_loader = qimaiItemLoader(item=qimaiItem(), response=response)
            item_loader.add_value("appId", app_info["appId"])
            item_loader.add_value("appName", app_info["appName"])
            item_loader.add_value("icon", app_info["icon"])
            item_loader.add_value("publisher", app_info["publisher"])
            item_loader.add_value("country", app_info["country"])
            item_loader.add_value("genre", info["genre"])
            item_loader.add_value("price", info["price"])
            item_loader.add_value("releaseTime", info["releaseTime"])

            qimai_item = item_loader.load_item()
            yield qimai_item
