# -*- coding: utf-8 -*-

import codecs
import json

from twisted.enterprise import adbapi

import pymysql
# import MySQLdb.cursors


class AppcrawlPipeline(object):
    def process_item(self, item, spider):
        return item

class MysqlPipeline(object):
    #采用同步的机制写入mysql
    def __init__(self):
        self.conn = pymysql.connect('127.0.0.1', 'root', 'rexueyouxi666', 'appdata', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            insert into appinfo(appId, appName, icon, publisher, country, genre, price, releaseTime)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(insert_sql, (item["appId"], item["appName"], item["icon"], item["publisher"], \
                                            item["country"], item["genre"], item["price"], item["releaseTime"],))
        self.conn.commit()

