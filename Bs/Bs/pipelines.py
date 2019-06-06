# -*- coding: utf-8 -*-
from twisted.enterprise import adbapi
import json
import datetime


class BsPipeline(object):
    def __init__(self):
        params = dict(database="zb2019",
                      password="!@password",
                      user="zb",
                      host="bs.letlike.com",
                      port="5432")
        # PostgreSQL PyPgSQL
        self.cp = adbapi.ConnectionPool('psycopg2', **params)

    def process_item(self, item, spider):
        # 使用数据库连接池对象进行数据库操作,自动传递cursor对象到第一个参数
        query = self.cp.runInteraction(self.do_insert, item, spider)
        # query = self.cp.runOperation(self.do_insert, item)
        # 设置出错时的回调方法,自动传递出错消息对象failure到第一个参数
        query.addErrback(self.on_error, spider)
        # 没有return query   self.cp.runOperation不会执行
        return query

    def do_insert(self, cursor, item, spider):
        attachmentlink = [{
            "id": "61",
            "cat": "multi",
            "answer": "ABCD"
        }]
        cursor.execute(
            "INSERT INTO bid_document_detail_copy(hash,link,detail,attachmentlink)VALUES(%s,%s,%s,%s) returning bdid",
            ("1", item['link'], item['detail'], json.dumps(attachmentlink)))
        bdid = (cursor.fetchone())[0]
        timeStamp = int(item['issueTime'])/1000
        dateArray = datetime.datetime.utcfromtimestamp(timeStamp)
        otherStyleTime = dateArray.strftime("%Y-%m-%d %H:%M:%S")
        self.cp.runOperation(
            "INSERT INTO bid_document_copy(bdid,area,title,issueTime,category,stage,type,industry,word,status)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            (bdid, "1234", item['title'], otherStyleTime, "1", "1", "1", '{656}', "'秀':222 '竞争':12A,31 '竞争性':11A,30 '管理':228 '管理咨询':227 '类':9A,28,57,102,179,268,303 '组长':314 '结束':38 '结果':41,204,413 '综合':190,396 '综合楼':395 '编号':62,70 '罗':233 '美景':394 '职务':307 '联系':185,187,253,255,340,357,361,378,381 '联系人':184,252,356,377 '联系方式':186,339 '联系电话':254,360,380 '要求':78 '计':65 '认为':409 '评分':191 '评审':203 '详细':104 '谈判':163,286 '财':63 '财务':320,329 '财务审计':319,328 '责任':375 '质疑':428 '资源':160 '起':401 '过程':312,411 '选定':337 '递交':129,137 '邀请':106,116 '邹':315 '郑文':324 '采':64 '采购':33,44,61,74,121,332,342,365,405,410,421,423 '金额':90,242,248,250 '鉴证':322,331 '限价':92 '霖':336 '项目':34,45,47,75,85 '预算':80,89 '鲁':292", "1")).addErrback(self.on_error, spider)

    def on_error(self, failure, spider):
        spider.logger.error(failure)

    def close_spider(self, spider):
        self.cp.close()
