# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from elasticsearch import Elasticsearch

# es = connections.create_connection(ArticleType._doc_type.using)

def get_price(value):
    ls = value.split("￥")
    if len(ls) == 1:
        return 0
    else:
        return ls[1]
 
def get_icon(value):
    icon = value.replace('\\', '')
    return icon

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
    icon = scrapy.Field(
        input_processor=MapCompose(get_price)
    )
    publisher = scrapy.Field()
    country = scrapy.Field()
    genre = scrapy.Field()
<<<<<<< HEAD
    price= scrapy.Field(
        input_processor=MapCompose(get_price)
    )
    releaseTime = scrapy.Field()
=======
    price= scrapy.Field()
    releaseTime= scrapy.Field()
>>>>>>> 3799fbc4abf287e45352812957705dc057da7e26

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

<<<<<<< HEAD
        return insert_sql, params

# {
# 	"appInfo": {
# 		"appId": "1396506145",
# 		"appName": "1233北京赛车PK10、二分时时彩彩票网~足彩在线比分直播",
# 		"icon": "https:\/\/is5-ssl.mzstatic.com\/image\/thumb\/Purple115\/v4\/f0\/81\/04\/f081041d-e48b-ea52-6225-1fd8e575272b\/AppIcon-1x_U007emarketing-85-220-2.png\/180x180bb.png",
# 		"publisher": "Junhao Feng",
# 		"country": "cn"
# 	},
# 	"genre": "生活",
# 	"price": "免费",
# 	"releaseTime": "2018-07-08"
# }
=======
        return insert_sql, params
>>>>>>> 3799fbc4abf287e45352812957705dc057da7e26
