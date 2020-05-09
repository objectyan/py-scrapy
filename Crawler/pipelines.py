# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
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
            min=2,
            max=5,
            increment=1,
            threaded=True,
        )
        dbpool = cx_Oracle.SessionPool(**dbparms)
        return cls(dbpool)

    def process_item(self, item, spider):
        connection = self.dbpool.acquire()
        cursor = connection.cursor()
        sql = "insert when (not exists (select 1 from TB_COMMON_NEWS where newtitle = :newtitle and newsource = :newsource)) then into TB_COMMON_NEWS(newtitle, newdetailurl,newcontext,newtime,newsource) select :newtitle, :newdetailurl, :newcontext, :newtime, :newsource from dual"
        param = {'newtitle': item['title'], 'newdetailurl': item['detailurl'],
                 'newcontext': item['context'], 'newtime': item['time'], 'newsource': item['source']}
        cursor.execute(sql, param)
        connection.commit()
        cursor.close()
        return item
