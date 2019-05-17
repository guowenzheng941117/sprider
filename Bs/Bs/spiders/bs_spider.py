import scrapy
import json
from Bs.items import BsItem


class BsSpider(scrapy.Spider):
    name = "bs"
    page = 1
    category = 1
    area = "中国.湖南"

    #     other_data = json.loads(response.body.decode("utf-8"))['data']
    #     next_link = other_data['current_page']
    #     if next_link < other_data['last_page']:
    #         next_link += 1
    #         yield scrapy.FormRequest(
    #             'http://www.ccgp-hunan.gov.cn/mvc/getNoticeList4Web.do',
    #             callback=self.parse)

    def start_requests(self):
        yield scrapy.http.FormRequest(
            url='http://www.ccgp-hunan.gov.cn/mvc/getNoticeList4Web.do',
            formdata={
                'pType': '',
                'prcmPrjName': '',
                'prcmItemCode': '',
                'prcmOrgName': '',
                'startDate': '2019-05-16',
                'endDate': '2019-05-16',
                'prcmPlanNo': '',
                'page': str(self.page),
                'pageSize': '3'
            },
            callback=self.parselist,
            dont_filter=True)

    def parselist(self, response):
        main_data = json.loads(response.body.decode('utf-8'))['rows']
        # 处理数据
        for i_item in range(len(main_data)):
            # 初始化item对象
            bs_item = BsItem()
            # 通知id
            bs_item['id'] = main_data[i_item]['NOTICE_ID']
            # 标题
            bs_item['title'] = main_data[i_item]['NOTICE_TITLE']
            # 时间
            bs_item['issueTime'] = main_data[i_item]['NEWWORK_DATE_ALL'][
                'time']
            # 实际链接
            bs_item[
                'link'] = 'http://www.ccgp-hunan.gov.cn/page/notice/notice.jsp?noticeId=' + str(
                    main_data[i_item]['NOTICE_ID'])
            # 按进行方式分类
            bs_item['type'] = self.getTypeByMode(
                main_data[i_item]['PRCM_MODE_NAME'])
            # 进行阶段分类
            bs_item['stage'] = self.getStageByName(
                main_data[i_item]['NOTICE_NAME'])
            # 根据实际链接继续爬
            yield scrapy.Request(bs_item['link'],
                                 callback=self.parseDetail,
                                 meta={'bs_item': bs_item})
        # 如果有数据就继续请求下一页
        # if main_data:
        #     self.page += 1
        #     page = self.page
        #     yield scrapy.http.FormRequest(
        #         url='http://www.ccgp-hunan.gov.cn/mvc/getNoticeList4Web.do',
        #         formdata={
        #             'pType': '',
        #             'prcmPrjName': '',
        #             'prcmItemCode': '',
        #             'prcmOrgName': '',
        #             'startDate': '2019-05-16',
        #             'endDate': '2019-05-16',
        #             'prcmPlanNo': '',
        #             'page': str(page),
        #             'pageSize': '10'
        #         },
        #         callback=self.parselist,
        #         dont_filter=True)

    def parseDetail(self, response):
        bs_item = response.meta['bs_item']
        frameLink = "http://www.ccgp-hunan.gov.cn" + response.xpath(
            "//iframe/@src").get()
        # 根据实际链接继续爬
        yield scrapy.Request(frameLink,
                             callback=self.parseFrame,
                             meta={'bs_item': bs_item})

    def parseFrame(self, response):
        bs_item = response.meta['bs_item']
        yield bs_item

    def getTypeByMode(self, PRCM_MODE_NAME):
        if PRCM_MODE_NAME == '公开招标':
            return 1
        elif PRCM_MODE_NAME == '协议供货':
            return 2
        elif PRCM_MODE_NAME == '定点采购':
            return 3
        elif PRCM_MODE_NAME == '邀请招标':
            return 4
        elif PRCM_MODE_NAME == '竞争性谈判':
            return 5
        elif PRCM_MODE_NAME == '竞争性磋商':
            return 6
        elif PRCM_MODE_NAME == '询价':
            return 7
        elif PRCM_MODE_NAME == '单一来源':
            return 8
        elif PRCM_MODE_NAME == '紧急采购':
            return 9
        else:
            return 0

    def getStageByName(self, NOTICE_NAME):
        if NOTICE_NAME == '采购公告' or NOTICE_NAME == '单一来源公示':
            return 3
        elif NOTICE_NAME == '更正公告':
            return 4
        elif NOTICE_NAME == '成交公告':
            return 5
        elif NOTICE_NAME == '终止公告':
            return 6
        elif NOTICE_NAME == '废标公告':
            return 7
        elif NOTICE_NAME == '合同公告':
            return 8
        else:
            return 0
