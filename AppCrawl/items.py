# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join



class AppcrawlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class qimaiItemLoader(ItemLoader):
    #自定义itemloader
    default_output_processor = TakeFirst()

class qimaiItem(scrapy.Item):
    appId = scrapy.Field()
    appName = scrapy.Field()
    icon = scrapy.Field()
    publisher = scrapy.Field()
    country = scrapy.Field()
    genre = scrapy.Field()
    price= scrapy.Field()
    releaseTime= scrapy.Field()

    def get_insert_sql(self):
        #插入的sql语句
        insert_sql = """
            insert IGNORE into appinfo(appId, appName, icon, publisher, country, genre, price, releaseTime)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            self["appId"], self["appName"], self["icon"], self["publisher"], \
            self["country"], self["genre"], self["price"], self["releaseTime"]
        )

        return insert_sql, params