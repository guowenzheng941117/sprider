# -*- coding: utf-8 -*-
# import psycopg2
# from Bs.settings import pgsql_database, pgsql_host, pgsql_password, pgsql_port, pgsql_user
from twisted.enterprise import adbapi

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class BsPipeline(object):
    def __init__(self):
        # self.database = pgsql_database
        # self.host = pgsql_host
        # self.port = pgsql_port
        # self.user = pgsql_user
        # self.password = pgsql_password
        params = dict(database="zb2019",
                      password="!@password",
                      user="zb",
                      host="bs.letlike.com",
                      port="5432")
        # PostgreSQL PyPgSQL
        self.cp = adbapi.ConnectionPool('psycopg2', **params)

    def process_item(self, item, spider):
        # self.cur.execute(
        #     "INSERT INTO test(title,issueTime,detail,link)VALUES(%s,%s,%s,%s)",
        #     (item['title'], item['issueTime'], item['detail'], item['link']))
        # return item
        # 使用数据库连接池对象进行数据库操作,自动传递cursor对象到第一个参数
        # query = self.cp.runInteraction(self.do_insert, item)
        # 设置出错时的回调方法,自动传递出错消息对象failure到第一个参数
        # query.addErrback(self.on_error, spider)
        # return的对象会显示到命令行
        # return query
        return self.cp.runOperation(
            "INSERT INTO test(title,issueTime,detail,link)VALUES(%s,%s,%s,%s)",
            (item['title'], item['issueTime'], item['detail'],
             item['link'])).addErrback(self.on_error, spider)

    def do_insert(self, cursor, item):
        cursor.execute(
            "INSERT INTO test(title,issueTime,detail,link)VALUES(%s,%s,%s,%s)",
            (item['title'], item['issueTime'], item['detail'], item['link']))

    def on_error(self, failure, spider):
        spider.logger.error(failure)

    # def open_spider(self, spider):
    # 创建连接对象
    # self.conn = psycopg2.connect(database=self.database,
    #                              user=self.user,
    #                              password=self.password,
    #                              host=self.host,
    #                              port=self.port)
    # self.cur = self.conn.cursor()  # 创建指针对象

    def close_spider(self, spider):
        # self.conn.commit()
        # self.cur.close()
        # self.conn.close()
        self.cp.close()
