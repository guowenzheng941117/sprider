# -*- coding: utf-8 -*-
import psycopg2
from Bs.settings import pgsql_database, pgsql_host, pgsql_password, pgsql_port, pgsql_user
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class BsPipeline(object):
    def __init__(self):
        self.database = pgsql_database
        self.host = pgsql_host
        self.port = pgsql_port
        self.user = pgsql_user
        self.password = pgsql_password

    def process_item(self, item, spider):
        self.cur.execute(
            "INSERT INTO test(org_name,notice_title,time,sub_title,prcm_mode_name)VALUES(%s,%s,%s,%s,%s)",
            (item['org_name'], item['notice_title'], item['time'],
             item['sub_title'], item['prcm_mode_name']))
        return item

    def open_spider(self, spider):
        # 创建连接对象
        self.conn = psycopg2.connect(database=self.database,
                                     user=self.user,
                                     password=self.password,
                                     host=self.host,
                                     port=self.port)
        self.cur = self.conn.cursor()  # 创建指针对象

    def close_spider(self, spider):
        self.conn.commit()
        self.cur.close()
        self.conn.close()
