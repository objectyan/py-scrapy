# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi
import cx_Oracle


class OracleTwistedPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        # 数据库配置
        dbparms = dict(
            user=settings["ORACLE_USER"],
            password=settings["ORACLE_PASSWORD"],
            dsn=cx_Oracle.makedsn(
                settings["ORACLE_HOST"], settings["ORACLE_PORT"], service_name=settings["ORACLE_SERVICENAME"]),
            encoding='UTF-8',
        )
        dbpool = adbapi.ConnectionPool("cx_Oracle", **dbparms)
        return cls(dbpool)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)

    def do_insert(self, cursor, item):
        insert_sql = "INSERT INTO TB_COMMON_NEWS(newtitle, newdetailurl,newcontext,newtime,newimgurl,newsource) ' \
                    'VALUES (:1, :2, :3, :4, :5, :6)"
        data = (item["title"], item["detailurl"], item["context"],
                item["time"], item["imgurl"], item["source"])
        cursor.execute(insert_sql % data)

    def handle_error(self, failure, item, spider):
        print(failure)
