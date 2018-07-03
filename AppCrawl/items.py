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
