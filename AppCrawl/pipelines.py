
# -*- coding: utf-8 -*-

import codecs
import json

import pymysql
from elasticsearch_dsl.connections import connections
from twisted.enterprise import adbapi

from AppCrawl.models.es_types import QimaiType

es = connections.create_connection(QimaiType._doc_type.using)

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


class MysqlTwistedPipline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host = settings["MYSQL_HOST"],
            db = settings["MYSQL_DBNAME"],
            user = settings["MYSQL_USER"],
            passwd = settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("pymysql", **dbparms)

        return cls(dbpool)

    def process_item(self, item, spider):
        #使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider) #处理异常

    def handle_error(self, failure, item, spider):
        #处理异步插入的异常
        print (failure)

    def do_insert(self, cursor, item):
        #执行具体的插入
        #根据不同的item 构建不同的sql语句并插入到mysql中
        insert_sql, params = item.get_insert_sql()
        cursor.execute(insert_sql, params)


class ElasticsearchPipeline(object):
    def process_item(self, item, spider):
        # 将item转换为es的数据
        appinfo = QimaiType()
        appinfo.appId = item["appId"]
        appinfo.appName = item["appName"]
        appinfo.icon = item["icon"]
        appinfo.publisher = item["publisher"]
        appinfo.country = item["country"]
        appinfo.genre = item["genre"]
        appinfo.price = item["price"]
        appinfo.releaseTime = item["releaseTime"]

        appinfo.suggest = gen_suggests(QimaiType._doc_type.index,  ((appinfo.appName,10),(appinfo.genre, 7)))
        # article.title_suggest = title_suggest

        appinfo.save()
        return


def gen_suggests(index, info_tuple):
    #根据字符串生成搜索建议数组
    used_words = set()
    suggests = []
    for text, weight in info_tuple:
        if text:
            #调用es的analyze接口分析字符串
            words = es.indices.analyze(index=index, analyzer="ik_max_word", params={'filter':["lowercase"]}, body=text)
            anylyzed_words = set([r["token"] for r in words["tokens"] if len(r["token"])>1])
            new_words = anylyzed_words - used_words
        else:
            new_words = set()

        if new_words:
            suggests.append({"input":list(new_words), "weight":weight})

    return suggests
